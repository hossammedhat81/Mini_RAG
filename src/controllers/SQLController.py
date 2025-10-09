"""
SQL Controller - Handles Text-to-SQL operations
Manages dataset uploads, schema detection, and natural language to SQL query conversion
"""

import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine, inspect, text, MetaData, Table, Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Dict, Any, Optional
import os
import json
from datetime import datetime
import re
from helpers.config import get_settings

class SQLController:
    """Controller for SQL operations and Text-to-SQL conversions"""
    
    def __init__(self):
        """Initialize SQL Controller with PostgreSQL connection"""
        self.config = get_settings()
        self.engine = self._create_engine()
        self.metadata = MetaData()
        self.uploaded_tables = {}  # Store table info
        
    def _create_engine(self):
        """Create PostgreSQL engine"""
        # Use synchronous postgresql driver (not asyncpg)
        db_url = f"postgresql://{self.config.POSTGRES_USERNAME}:{self.config.POSTGRES_PASSWORD}@{self.config.POSTGRES_HOST}:{self.config.POSTGRES_PORT}/{self.config.POSTGRES_MAIN_DATABASE}"
        return create_engine(db_url, echo=False)
    
    def upload_dataset(self, file_path: str, file_name: str, table_name: str = None) -> Dict[str, Any]:
        """
        Upload a CSV/Excel file to PostgreSQL
        
        Args:
            file_path: Path to the uploaded file
            file_name: Original filename
            table_name: Optional custom table name
            
        Returns:
            Dictionary with upload status and table info
        """
        try:
            # Determine file type and read data
            if file_name.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file_name.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(file_path)
            else:
                return {
                    'success': False,
                    'error': 'Unsupported file format. Please upload CSV or Excel files.'
                }
            
            # Generate table name if not provided
            if not table_name:
                table_name = self._sanitize_table_name(file_name)
            
            # Add prefix to avoid conflicts
            table_name = f"dataset_{table_name}"
            
            # Clean column names
            df.columns = [self._sanitize_column_name(col) for col in df.columns]
            
            # Upload to PostgreSQL
            df.to_sql(
                table_name,
                self.engine,
                if_exists='replace',
                index=False,
                dtype=self._infer_column_types(df)
            )
            
            # Store table metadata
            self.uploaded_tables[table_name] = {
                'original_name': file_name,
                'row_count': len(df),
                'columns': list(df.columns),
                'column_types': {col: str(dtype) for col, dtype in df.dtypes.items()},
                'upload_time': datetime.now().isoformat(),
                'sample_data': df.head(3).to_dict('records')
            }
            
            return {
                'success': True,
                'table_name': table_name,
                'row_count': len(df),
                'columns': list(df.columns),
                'column_types': {col: str(dtype) for col, dtype in df.dtypes.items()},
                'sample_data': df.head(3).to_dict('records')
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Failed to upload dataset: {str(e)}'
            }
    
    def get_all_tables(self) -> List[Dict[str, Any]]:
        """Get all uploaded dataset tables"""
        try:
            inspector = inspect(self.engine)
            all_tables = inspector.get_table_names()
            
            # Filter only dataset tables
            dataset_tables = [t for t in all_tables if t.startswith('dataset_')]
            
            result = []
            for table_name in dataset_tables:
                if table_name in self.uploaded_tables:
                    result.append({
                        'table_name': table_name,
                        **self.uploaded_tables[table_name]
                    })
                else:
                    # Fetch from database if not in memory
                    columns = [col['name'] for col in inspector.get_columns(table_name)]
                    result.append({
                        'table_name': table_name,
                        'columns': columns,
                        'original_name': table_name.replace('dataset_', '')
                    })
            
            return result
            
        except Exception as e:
            return []
    
    def get_table_schema(self, table_name: str) -> Dict[str, Any]:
        """Get detailed schema for a specific table"""
        try:
            inspector = inspect(self.engine)
            columns = inspector.get_columns(table_name)
            
            schema = {
                'table_name': table_name,
                'columns': [
                    {
                        'name': col['name'],
                        'type': str(col['type']),
                        'nullable': col['nullable']
                    }
                    for col in columns
                ]
            }
            
            # Get sample data
            with self.engine.connect() as conn:
                result = conn.execute(text(f"SELECT * FROM {table_name} LIMIT 5"))
                schema['sample_data'] = [dict(row) for row in result]
            
            return schema
            
        except Exception as e:
            return {'error': str(e)}
    
    def detect_relationships(self) -> List[Dict[str, Any]]:
        """
        Detect potential relationships between tables based on column names
        """
        relationships = []
        tables = self.get_all_tables()
        
        for i, table1 in enumerate(tables):
            for table2 in tables[i+1:]:
                # Find common columns
                common_cols = set(table1['columns']) & set(table2['columns'])
                
                for col in common_cols:
                    # Check if it's likely a foreign key
                    if 'id' in col.lower() or col.endswith('_id') or col in ['phone', 'email', 'user']:
                        relationships.append({
                            'table1': table1['table_name'],
                            'table2': table2['table_name'],
                            'column': col,
                            'type': 'potential_foreign_key'
                        })
        
        return relationships
    
    def generate_sql_from_nl(self, question: str, llm_provider) -> Dict[str, Any]:
        """
        Generate SQL query from natural language question
        
        Args:
            question: Natural language question
            llm_provider: LLM provider instance for query generation
            
        Returns:
            Dictionary with SQL query and metadata
        """
        try:
            # Get schema context
            tables = self.get_all_tables()
            if not tables:
                return {
                    'success': False,
                    'error': 'No datasets uploaded. Please upload a dataset first.'
                }
            
            # Build schema context for LLM
            schema_context = self._build_schema_context(tables)
            
            # Create prompt for SQL generation
            prompt = f"""You are a SQL expert. Convert the following natural language question into a valid PostgreSQL query.

Database Schema:
{schema_context}

Question: {question}

Important rules:
1. Return ONLY the SQL query, no explanations or markdown
2. Use proper PostgreSQL syntax
3. Include appropriate JOINs if multiple tables are needed
4. Use WHERE clauses for filtering
5. Use aggregate functions (COUNT, SUM, AVG) when appropriate
6. Limit results to 100 rows if not specified
7. Use table aliases for readability

SQL Query:"""

            # Generate SQL using LLM
            response = llm_provider.generate(prompt, max_tokens=500, temperature=0.1)
            
            # Extract and clean SQL query
            sql_query = self._extract_sql_query(response)
            
            return {
                'success': True,
                'sql_query': sql_query,
                'original_question': question
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Failed to generate SQL: {str(e)}'
            }
    
    def execute_sql_query(self, sql_query: str) -> Dict[str, Any]:
        """
        Execute SQL query safely and return results
        
        Args:
            sql_query: SQL query to execute
            
        Returns:
            Dictionary with query results
        """
        try:
            # Validate query (basic security check)
            if not self._is_safe_query(sql_query):
                return {
                    'success': False,
                    'error': 'Query contains potentially unsafe operations'
                }
            
            # Execute query
            with self.engine.connect() as conn:
                result = conn.execute(text(sql_query))
                
                # Fetch results
                rows = result.fetchall()
                columns = result.keys()
                
                # Convert to list of dicts
                data = [dict(zip(columns, row)) for row in rows]
                
                return {
                    'success': True,
                    'columns': list(columns),
                    'data': data,
                    'row_count': len(data)
                }
                
        except SQLAlchemyError as e:
            return {
                'success': False,
                'error': f'Query execution failed: {str(e)}'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Unexpected error: {str(e)}'
            }
    
    def delete_table(self, table_name: str) -> Dict[str, Any]:
        """Delete a dataset table"""
        try:
            with self.engine.connect() as conn:
                conn.execute(text(f"DROP TABLE IF EXISTS {table_name}"))
                conn.commit()
            
            # Remove from memory
            if table_name in self.uploaded_tables:
                del self.uploaded_tables[table_name]
            
            return {'success': True, 'message': f'Table {table_name} deleted'}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    # Helper methods
    
    def _sanitize_table_name(self, filename: str) -> str:
        """Convert filename to valid table name"""
        # Remove extension
        name = os.path.splitext(filename)[0]
        # Replace special characters with underscore
        name = re.sub(r'[^a-zA-Z0-9_]', '_', name)
        # Remove consecutive underscores
        name = re.sub(r'_+', '_', name)
        # Ensure starts with letter
        if name[0].isdigit():
            name = 'table_' + name
        return name.lower()[:50]  # Limit length
    
    def _sanitize_column_name(self, column_name: str) -> str:
        """Convert column name to valid SQL identifier"""
        # Replace special characters with underscore
        name = re.sub(r'[^a-zA-Z0-9_]', '_', str(column_name))
        # Remove consecutive underscores
        name = re.sub(r'_+', '_', name)
        # Ensure starts with letter
        if name[0].isdigit():
            name = 'col_' + name
        return name.lower()[:50]
    
    def _infer_column_types(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Infer SQLAlchemy types from pandas dtypes"""
        type_mapping = {}
        for col in df.columns:
            dtype = df[col].dtype
            if pd.api.types.is_integer_dtype(dtype):
                type_mapping[col] = Integer
            elif pd.api.types.is_float_dtype(dtype):
                type_mapping[col] = Float
            elif pd.api.types.is_bool_dtype(dtype):
                type_mapping[col] = Boolean
            elif pd.api.types.is_datetime64_any_dtype(dtype):
                type_mapping[col] = DateTime
            else:
                type_mapping[col] = String
        return type_mapping
    
    def _build_schema_context(self, tables: List[Dict[str, Any]]) -> str:
        """Build schema context string for LLM"""
        context = []
        for table in tables:
            table_info = f"\nTable: {table['table_name']}"
            table_info += f"\nColumns: {', '.join(table['columns'])}"
            if 'column_types' in table:
                table_info += f"\nTypes: {json.dumps(table['column_types'], indent=2)}"
            if 'sample_data' in table and table['sample_data']:
                table_info += f"\nSample data (first row): {json.dumps(table['sample_data'][0], indent=2)}"
            context.append(table_info)
        return '\n'.join(context)
    
    def _extract_sql_query(self, llm_response: str) -> str:
        """Extract SQL query from LLM response"""
        # Remove markdown code blocks if present
        response = llm_response.strip()
        
        # Remove ```sql or ``` markers
        if response.startswith('```'):
            lines = response.split('\n')
            lines = [l for l in lines if not l.strip().startswith('```')]
            response = '\n'.join(lines)
        
        # Remove common prefixes
        prefixes = ['sql:', 'query:', 'SQL:', 'Query:']
        for prefix in prefixes:
            if response.startswith(prefix):
                response = response[len(prefix):].strip()
        
        return response.strip()
    
    def _is_safe_query(self, sql_query: str) -> bool:
        """
        Basic security check for SQL query
        Prevents dangerous operations
        """
        sql_lower = sql_query.lower()
        
        # Disallow dangerous operations
        dangerous_keywords = [
            'drop table', 'drop database', 'truncate', 'delete from',
            'update ', 'insert into', 'alter table', 'create table',
            'grant', 'revoke', 'exec', 'execute', 'xp_'
        ]
        
        for keyword in dangerous_keywords:
            if keyword in sql_lower:
                return False
        
        # Must be a SELECT query
        if not sql_lower.strip().startswith('select'):
            return False
        
        return True

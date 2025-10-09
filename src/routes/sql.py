"""
SQL Routes - API endpoints for Text-to-SQL operations
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, Form, Request
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from controllers.SQLController import SQLController
import shutil
import os
import tempfile

router = APIRouter()

# Pydantic models for request/response
class SQLQueryRequest(BaseModel):
    question: str
    project_id: Optional[int] = 1

class ExecuteSQLRequest(BaseModel):
    sql_query: str

class DeleteTableRequest(BaseModel):
    table_name: str

# Initialize controller
sql_controller = SQLController()

@router.post("/upload-dataset/{project_id}")
async def upload_dataset(
    project_id: int,
    file: UploadFile = File(...),
    table_name: Optional[str] = Form(None)
):
    """
    Upload a CSV or Excel dataset and import to PostgreSQL
    
    Args:
        project_id: Project ID
        file: Uploaded file (CSV or Excel)
        table_name: Optional custom table name
    
    Returns:
        Upload status and table information
    """
    try:
        # Validate file type
        if not file.filename.endswith(('.csv', '.xlsx', '.xls')):
            raise HTTPException(
                status_code=400,
                detail="Invalid file type. Please upload CSV or Excel files."
            )
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp_file:
            shutil.copyfileobj(file.file, tmp_file)
            tmp_path = tmp_file.name
        
        try:
            # Upload to database
            result = sql_controller.upload_dataset(
                file_path=tmp_path,
                file_name=file.filename,
                table_name=table_name
            )
            
            return result
            
        finally:
            # Clean up temporary file
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
                
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tables")
async def get_tables():
    """
    Get all uploaded dataset tables
    
    Returns:
        List of tables with metadata
    """
    try:
        tables = sql_controller.get_all_tables()
        return {
            "success": True,
            "tables": tables,
            "count": len(tables)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/table/{table_name}/schema")
async def get_table_schema(table_name: str):
    """
    Get detailed schema for a specific table
    
    Args:
        table_name: Name of the table
    
    Returns:
        Table schema and sample data
    """
    try:
        schema = sql_controller.get_table_schema(table_name)
        
        if 'error' in schema:
            raise HTTPException(status_code=404, detail=schema['error'])
        
        return {
            "success": True,
            **schema
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/relationships")
async def get_relationships():
    """
    Detect potential relationships between tables
    
    Returns:
        List of detected relationships
    """
    try:
        relationships = sql_controller.detect_relationships()
        return {
            "success": True,
            "relationships": relationships,
            "count": len(relationships)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/query/generate")
async def generate_sql_query(request: SQLQueryRequest, request_obj: Request):
    """
    Generate SQL query from natural language question
    
    Args:
        request: SQLQueryRequest with question
        request_obj: FastAPI Request object to access app state
    
    Returns:
        Generated SQL query
    """
    try:
        # Get LLM provider from app state
        llm_provider = request_obj.app.generation_client
        
        # Generate SQL
        result = sql_controller.generate_sql_from_nl(
            question=request.question,
            llm_provider=llm_provider
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/query/execute")
async def execute_sql_query(request: ExecuteSQLRequest):
    """
    Execute SQL query and return results
    
    Args:
        request: ExecuteSQLRequest with SQL query
    
    Returns:
        Query results
    """
    try:
        result = sql_controller.execute_sql_query(request.sql_query)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/query/nl")
async def query_from_natural_language(request: SQLQueryRequest, request_obj: Request):
    """
    Complete pipeline: Generate SQL from NL question and execute it
    
    Args:
        request: SQLQueryRequest with natural language question
        request_obj: FastAPI Request object to access app state
    
    Returns:
        Query results with generated SQL
    """
    try:
        # Get LLM provider from app state
        llm_provider = request_obj.app.generation_client
        
        # Generate SQL
        sql_result = sql_controller.generate_sql_from_nl(
            question=request.question,
            llm_provider=llm_provider
        )
        
        if not sql_result.get('success'):
            return sql_result
        
        # Execute SQL
        exec_result = sql_controller.execute_sql_query(sql_result['sql_query'])
        
        # Combine results
        return {
            "success": exec_result.get('success'),
            "question": request.question,
            "sql_query": sql_result['sql_query'],
            "columns": exec_result.get('columns', []),
            "data": exec_result.get('data', []),
            "row_count": exec_result.get('row_count', 0),
            "error": exec_result.get('error')
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/table/{table_name}")
async def delete_table(table_name: str):
    """
    Delete a dataset table
    
    Args:
        table_name: Name of the table to delete
    
    Returns:
        Deletion status
    """
    try:
        result = sql_controller.delete_table(table_name)
        
        if not result.get('success'):
            raise HTTPException(status_code=500, detail=result.get('error'))
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

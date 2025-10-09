from .BaseController import BaseController
from .ProjectController import ProjectController
import os
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyMuPDFLoader
from models import ProcessingEnum
from typing import List
from dataclasses import dataclass
import pandas as pd

@dataclass
class Document:
    page_content: str
    metadata: dict

class ProcessController(BaseController):

    def __init__(self, project_id: str):
        super().__init__()

        self.project_id = project_id
        self.project_path = ProjectController().get_project_path(project_id=project_id)

    def get_file_extension(self, file_id: str):
        return os.path.splitext(file_id)[-1]

    def get_file_loader(self, file_id: str):

        file_ext = self.get_file_extension(file_id=file_id)
        file_path = os.path.join(
            self.project_path,
            file_id
        )

        if not os.path.exists(file_path):
            return None

        if file_ext == ProcessingEnum.TXT.value:
            return TextLoader(file_path, encoding="utf-8")

        if file_ext == ProcessingEnum.PDF.value:
            return PyMuPDFLoader(file_path)
        
        return None

    def get_csv_content_as_text(self, file_id: str):
        """Convert CSV to markdown table for text processing"""
        file_path = os.path.join(self.project_path, file_id)
        
        if not os.path.exists(file_path):
            return None
        
        try:
            # Read CSV
            df = pd.read_csv(file_path)
            
            # Convert to markdown table (LLM-friendly format)
            markdown_table = df.to_markdown(index=False)
            
            # Add metadata header
            csv_info = f"""# CSV Dataset: {file_id}
Rows: {len(df)}
Columns: {', '.join(df.columns.tolist())}

## Data:
{markdown_table}
"""
            # Return in same format as TextLoader
            return [Document(
                page_content=csv_info,
                metadata={"source": file_id, "type": "csv"}
            )]
            
        except Exception as e:
            print(f"Error reading CSV {file_id}: {e}")
            return None

    def get_file_content(self, file_id: str):
        
        # Check if CSV first
        file_ext = self.get_file_extension(file_id=file_id)
        if file_ext == ".csv":
            return self.get_csv_content_as_text(file_id=file_id)

        # Use existing loaders for PDF/TXT
        loader = self.get_file_loader(file_id=file_id)
        if loader:
            return loader.load()

        return None

    def process_file_content(self, file_content: list, file_id: str,
                            chunk_size: int=100, overlap_size: int=20):

        file_content_texts = [
            rec.page_content
            for rec in file_content
        ]

        file_content_metadata = [
            rec.metadata
            for rec in file_content
        ]

        # chunks = text_splitter.create_documents(
        #     file_content_texts,
        #     metadatas=file_content_metadata
        # )

        chunks = self.process_simpler_splitter(
            texts=file_content_texts,
            metadatas=file_content_metadata,
            chunk_size=chunk_size,
        )

        return chunks

    def process_simpler_splitter(self, texts: List[str], metadatas: List[dict], chunk_size: int, splitter_tag: str="\n"):
        
        full_text = " ".join(texts)

        # split by splitter_tag
        lines = [ doc.strip() for doc in full_text.split(splitter_tag) if len(doc.strip()) > 1 ]

        chunks = []
        current_chunk = ""

        for line in lines:
            current_chunk += line + splitter_tag
            if len(current_chunk) >= chunk_size:
                chunks.append(Document(
                    page_content=current_chunk.strip(),
                    metadata={}
                ))

                current_chunk = ""

        if len(current_chunk) >= 0:
            chunks.append(Document(
                page_content=current_chunk.strip(),
                metadata={}
            ))

        return chunks


    


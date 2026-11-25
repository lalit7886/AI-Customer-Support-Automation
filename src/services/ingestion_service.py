import pymupdf
from docx import Document
from src.core.exceptions import MyException
from src.core.logging import logger
from datetime import datetime
import json
import hashlib
from pathlib import Path
from uuid import uuid4

def extract_pdf(file_path: str):
    """
    Extracts text from a PDF file using PyMuPDF.

    Args:
        file_path (str): The path to the PDF file.
        """
    if file_path:
        file_path = Path(file_path)
    else:
        raise ValueError(f"The file path is empty")
    logger.info(f"started extracting text from {file_path}")
    try:
        unstructred_text = []
        with pymupdf.open(file_path) as docs:
            
            for page in docs:
                page_text = page.get_text()
                
                tables = page.find_tables()
                table_text_block = []
                
                if tables.tables:
                    
                    for table in tables:
                        bbox = table.bbox
                        
                        table_text = page.get_text(clip=bbox)
                        table_text_block.append(table_text.strip())
                
                lines = page_text.split("\n")
                filtered_lines = []
                for line in lines:
                    line = line.strip()
                    if line:
                        is_table_content = False
                        for table_text in table_text_block:
                            if line in table_text:
                                is_table_content=True
                                break
                        if not is_table_content:
                            filtered_lines.append(line)
                page_unstructured = "\n\n".join(filtered_lines)
                if page_unstructured.strip():
                    unstructred_text.append(page_unstructured)
        _response = '\n\n'.join(unstructred_text)
        _response_with_metadata = {
            "document_id": uuid4(),
            "file_name":file_path.name,
            "source":file_path,
            "extracted_text":_response,
            "last_extracted_time":datetime.now(),
        }
        return _response_with_metadata
                
    except Exception as e:
        raise MyException(e) from e
    
    
    
        

def extract_docx(file_path:str):
    """
    Extract text from documents
    """
    
    
    if file_path:
        file_path = Path(file_path)
    else:
        raise ValueError("file path must not be empty")
    
    try:
        document = Document(file_path)
        tables_content=[]
        document_content=[]
        text_content=" ".join([para.text for para in document.paragraphs])
        for table in document.tables:
            heading = [cell.text.strip() for cell in table.rows[0].cells]
            table_content=[]
            for rows in table.rows[1:]:
                row_data = [cell.text.strip() for cell in rows.cells]
                table_content.append(dict(zip(heading, row_data)))
            tables_content.append(table_content)
        plain_text = "\n".join(" ".join("|".join(f"{key} : {value}" for key, value in dics_.items()) for dics_ in table_content_) for table_content_ in tables_content )
        return{
            "document_id":uuid4(),
            "file_name":file_path.name,
            "source":file_path,
            "extracted_text":text_content + "\n\n" + plain_text,
            "last_extracted_time":datetime.now(),
        }
    except Exception as e:
        raise MyException(e) from e
    
            
            
            
def extract_text(file_path:str):
    try:
        logger.info(f"starting the text extracion from file {file_path}")
        if file_path and Path(file_path).exists():
            file_path = Path(file_path)
        else:
            raise ValueError(f"The path must not be empty and must be valid")
        
            
        with open(file_path,"r") as f:
            text = f.read()
        return{
            "document_id":uuid4(),
            "file_name":file_path.name,
            "source":file_path,
            "extracted_text":text,
            "last_extracted_time":datetime.now(),
        }
    except Exception as e:
        raise MyException(e) from e
    
def extract_readme(file_path:str):
    """This function extract plain text from readme file"""
    text=Path(file_path).read_text(encoding="utf-8")
    return{
        "file_name":Path(file_path).name,
        "source":file_path,
        "extracted_text":text,
        "last_extracted_time":datetime.now(),
    }


def generate_hash(text:str):
    hash_ = hashlib.sha256
    normalized_text =  " ".join(text.split())
    return hash_(normalized_text.encode("utf-8")).hexdigest()
    
        
if __name__ == "__main__":
    # file_path = "/Users/lalitramanmishra/AI-Customer-Support-Automation/knowledge_base/raw/free.docx"
    # extracted_text = extract_docx(file_path)
    # print(len(extracted_text.get("extracted_text")))
    print(generate_hash("I love you baby, Yes you stalking at my githubs code."))
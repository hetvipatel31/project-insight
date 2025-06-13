import pandas as pd
from io import BytesIO
import pdfplumber
from docx import Document

def parse_data(file_content: bytes, file_name: str):
    """Parses uploaded file content based on its extension."""
    ext = file_name.split(".")[-1].lower()
    
    if ext == "csv":
        df = pd.read_csv(BytesIO(file_content))
        return {"type": "dataframe", "data": df.to_dict(orient="records"), "context": df.to_string()}
    elif ext in ["xls", "xlsx"]:
        df = pd.read_excel(BytesIO(file_content))
        return {"type": "dataframe", "data": df.to_dict(orient="records"), "context": df.to_string()}
    elif ext == "pdf":
        text = ""
        with pdfplumber.open(BytesIO(file_content)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return {"type": "text", "data": text, "context": text}
    elif ext in ["doc", "docx"]:
        doc = Document(BytesIO(file_content))
        text = "\n".join([para.text for para in doc.paragraphs])
        return {"type": "text", "data": text, "context": text}
    
    return None

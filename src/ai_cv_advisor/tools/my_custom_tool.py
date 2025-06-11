from PyPDF2 import PdfReader
from crewai.tools import BaseTool


class PDFReaderTool(BaseTool):
    name: str = "PDF Reader"
    description: str = "Read the content of a PDF file and returns the text."
    pdf_path: str
        
    def _run(self) -> str:
        reader = PdfReader(self.pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    
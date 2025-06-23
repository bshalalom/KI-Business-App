import io
from pydantic import BaseModel, Field
from pypdf import PdfReader
from typing import List

class PDFText(BaseModel):
    text: str = Field(..., description="Der extrahierte Text aus dem PDF.")
    page_count: int = Field(..., description="Die Anzahl der Seiten im PDF.")

# Die Funktion erwartet jetzt rohe Bytes als Input
def extract_text_from_pdf(pdf_content: bytes) -> List[str]:
    """
    Extrahiert Text von jeder Seite eines PDF-Inhalts (in Bytes).

    Args:
        pdf_content: Der Inhalt der PDF-Datei als Bytes.

    Returns:
        Eine Liste von Strings, wobei jeder String den Text einer Seite darstellt.
    """
    try:
        # KORREKTUR: Wir erstellen einen 'BytesIO'-Stream aus dem Inhalt.
        # Dies ist das dateiähnliche Objekt, das pypdf erwartet.
        pdf_file_stream = io.BytesIO(pdf_content)
        
        reader = PdfReader(pdf_file_stream)
        page_texts = [page.extract_text() for page in reader.pages if page.extract_text()]
        print(f"Text aus {len(reader.pages)} Seiten extrahiert.")
        return page_texts
    except Exception as e:
        print(f"Fehler beim Extrahieren von Text aus PDF: {e}")
        return []
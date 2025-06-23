from fastapi import APIRouter, UploadFile, File, Form
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel
from typing import List, Optional
import requests

from backend.PerplexityAgent import PerplexityAgent
from backend.OpenAIAnalysisAgent import OpenAIAnalysisAgent
from backend.OpenAIReviewerAgent import OpenAIReviewerAgent
from backend.pdfReader import extract_text_from_pdf
from backend.WebScraper import scrape_website
import backend.config as config

router = APIRouter()

class AnalyzeResponse(BaseModel):
    final_analysis: str
    urls_used: List[str]
    feedback_iterations: List[str]
    score: int

@router.post("/analyze-all", response_model=AnalyzeResponse)
async def analyze_all(
    prompt: str = Form(""),
    max_feedback_loops: int = Form(3),
    manual_pdf_files: Optional[List[UploadFile]] = File(None, alias="pdf_files")
):
    print("Starte die Perplexity-Suche für den Prompt...")
    perplexity_agent = PerplexityAgent()
    perplexity_result = await run_in_threadpool(perplexity_agent.extract_data, api_key=config.PERPLEXITY_API_KEY, prompt_text=prompt)
    found_urls = perplexity_result.get("citations", [])
    perplexity_summary = perplexity_result.get("content", "")
    print(f"Perplexity hat {len(found_urls)} URLs gefunden.")

    pdf_texts_list = []
    if manual_pdf_files:
        for pdf in manual_pdf_files:
            content = await pdf.read()
            pdf_pages = await run_in_threadpool(extract_text_from_pdf, content)
            pdf_texts_list.append("\n".join(pdf_pages))

    web_texts = []
    for url in found_urls:
        try:
            if url.lower().endswith('.pdf'):
                response = await run_in_threadpool(requests.get, url, timeout=20)
                response.raise_for_status()
                pdf_pages = await run_in_threadpool(extract_text_from_pdf, response.content)
                pdf_texts_list.append("\n".join(pdf_pages))
            else:
                scraped_data = await run_in_threadpool(scrape_website, url)
                if scraped_data.text and not scraped_data.error:
                    # KORREKTUR: Wir kürzen den Text jeder Quelle, um das Token-Limit nicht zu überschreiten
                    web_texts.append(scraped_data.text[:3500]) # Kürzen auf 3500 Zeichen
                elif scraped_data.error:
                     web_texts.append(f"[Fehler beim Scrapen von {url}: {scraped_data.error}]")
        except Exception as e:
            web_texts.append(f"[Fehler bei der Verarbeitung von URL {url}: {str(e)}]")

    # Der finale Kontext für die KI
    scraped_context = "\n\n---\n\n".join(web_texts)
    full_text = f"Recherche-Zusammenfassung:\n{perplexity_summary}\n\nZusätzliche Details aus den Quellen:\n{scraped_context}"
    
    combined_pdf_text = "\n\n".join(pdf_texts_list)
    analyzer = OpenAIAnalysisAgent(api_key=config.OPENAI_API_KEY)
    reviewer = OpenAIReviewerAgent(api_key=config.OPENAI_API_KEY)

    feedback_iterations = []
    analysis = "Keine Analyse durchgeführt."
    score = 0
    for i in range(max_feedback_loops):
        analysis = await run_in_threadpool(analyzer.analyze, full_text, pdf_text=combined_pdf_text)
        feedback = await run_in_threadpool(reviewer.review_analysis, analysis)
        score = await run_in_threadpool(reviewer.extract_score, feedback)
        feedback_iterations.append(
            f"[Durchgang {i+1}]\nAnalyse: {analysis}\nFeedback: {feedback}\nScore: {score}"
        )
        if score >= 8:
            break
        # Wir fügen das Feedback hinzu, aber kürzen es auch, falls es sehr lang ist
        full_text += "\n\nFeedback zur Verbesserung:\n" + feedback[:1000]

    return AnalyzeResponse(
        final_analysis=analysis,
        urls_used=found_urls,
        feedback_iterations=feedback_iterations,
        score=score
    )
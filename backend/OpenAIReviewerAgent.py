import openai
import re

class OpenAIReviewerAgent:
    def __init__(self, api_key):
        openai.api_key = api_key

    def review_analysis(self, analysis):
        # NEUER PROMPT: Der Agent soll eine Geschäftsidee ERSTELLEN
        prompt = f"""Du bist ein erfahrener und kreativer Startup-Gründer.
Deine Aufgabe ist es, aus der folgenden Marktanalyse eine konkrete, innovative Geschäftsidee zu entwickeln.

Marktanalyse:
---
{analysis}
---

Entwickle basierend auf dieser Analyse ein detailliertes Geschäftsmodell. Beschreibe die Idee klar und deutlich. Gehe dabei auf folgende Punkte ein:
1.  **Geschäftsmodell-Name:** (Ein kreativer Name für die Idee)
2.  **Wertversprechen:** (Welches Problem wird für wen gelöst?)
3.  **Zielgruppe:** (Wer sind die idealen Kunden?)
4.  **Funktionen:** (Was sind die Kernfunktionen der App/des Services?)
5.  **Monetarisierung:** (Wie wird Geld verdient? z.B. Abo, Freemium, Provision)

Bewerte am Ende deine eigene Idee mit einer Punktzahl für die Innovationskraft von 1 bis 10. Präsentiere das Ergebnis in einem klaren, gut strukturierten Format."""

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()

    def extract_score(self, feedback_text):
        match = re.search(r"(\b[1-9]|10)\b\s*/?\s*10", feedback_text)
        return int(match.group(1)) if match else 0
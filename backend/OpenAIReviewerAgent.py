import openai
import re

class OpenAIReviewerAgent:
    def __init__(self, api_key):
        openai.api_key = api_key

    def review_analysis(self, analysis):
        
        system_prompt = f"""
            Du bist ein erfahrener Startup-Gründer und Innovationsberater. "
            Deine Aufgabe ist es, auf Basis fundierter Marktanalysen realistische, kreative Geschäftsideen zu entwickeln. 
            Bewerte deine Ideen anschließend kritisch im Hinblick auf Innovationsgrad, Marktpotenzial und Umsetzbarkeit. 
            Sei dabei ehrlich, realistisch und klar in der Sprache – vermeide unnötigen Optimismus oder Übertreibungen."""
        
    
        user_prompt = f"""
            Entwickle basierend auf der folgenden Marktanalyse eine konkrete, innovative Geschäftsidee.
    
            Marktanalyse:
            ---
            {analysis}
            ---
    
            Beschreibe die Idee strukturiert in den folgenden Punkten:
            1. **Geschäftsmodell-Name:** (Ein kreativer, einprägsamer Name)
            2. **Wertversprechen:** (Welches Problem wird für wen gelöst?)
            3. **Zielgruppe:** (Wer sind die idealen Kunden?)
            4. **Funktionen:** (Was bietet der Service/die App konkret?)
            5. **Monetarisierung:** (Wie wird Geld verdient? z. B. Abo, Freemium, Provision)
            
            Zum Schluss:
            - Bewerte die Innovationskraft der Idee auf einer Skala von **1 bis 10**.
              - **1 = austauschbar**, **5 = solide**, **10 = visionär**.
              - Begründe die Bewertung in 2–3 Sätzen.
              
            Antworte in einem klar strukturierten Format.
            """
    
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
    
        return response.choices[0].message.content.strip()

    def extract_score(self, feedback_text):
        match = re.search(r"(\b[1-9]|10)\b\s*/?\s*10", feedback_text)
        return int(match.group(1)) if match else 0

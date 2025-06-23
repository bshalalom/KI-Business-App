import openai

class OpenAIAnalysisAgent:
    def __init__(self, api_key):
        openai.api_key = api_key

    #method to analyze the given text, urls and PDF. Text and PDF are shortend with a slice, to not exceed the token maximum
    def analyze(self, text, pdf_text):
    
        website_excerpt = text[:3000]
        pdf_excerpt = pdf_text[:2000]
    
        system_prompt = f"""
            Du bist ein erfahrener Business Developer und Unternehmensberater.
            Deine Aufgabe ist es, auf Basis gegebener Inhalte (Website- und PDF-Auszug) ein tragfähiges Geschäftsmodell zu entwickeln.
            Achte auf Machbarkeit, Differenzierungspotenzial und Zielgruppenrelevanz.
            """
        
    
        user_prompt = f""" 
            Analysiere bitte die folgenden Inhalte und entwickle daraus ein Geschäftsmodell mit 2–3 prägnanten, gut erklärten Aspekten.
    
            Website-Inhalt (Auszug): {website_excerpt}
            PDF-Inhalt (Auszug):{pdf_excerpt}
    
            Bitte nenne:
            1. Zielgruppe(n)
            2. Wertversprechen (Value Proposition)
            3. Besondere Merkmale oder Strategien (z. B. Vertrieb, USP, Plattformmodell etc.)
        
            Antworte in strukturierten Abschnitten mit klarer Gliederung.
            """
    
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
    
        return response.choices[0].message.content.strip()

    def revise_with_feedback(self, analysis, feedback):
        system_prompt = f"""
            "Du bist ein professioneller Analyst und Redakteur.
            Deine Aufgabe ist es, bestehende Inhalte anhand von externem Feedback gezielt zu überarbeiten.
            Achte auf Präzision, Struktur, Lesbarkeit und inhaltliche Konsistenz."""
        
    
        user_prompt = f"""
        Bitte überarbeite die folgende Analyse basierend auf dem angegebenen Feedback.
    
        Feedback:{feedback}
        
        Originalanalyse:{analysis}
        
        Ziel: Verbessere die Qualität der Analyse inhaltlich und sprachlich, ohne wichtige Aussagen zu verfälschen. 
        Wenn das Feedback unklar oder widersprüchlich ist, mache eine sachlich begründete Entscheidung. 
        Gib ausschließlich die überarbeitete Version der Analyse aus – keine Kommentare oder Erklärungen.
        """
    
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
    
        return response.choices[0].message.content.strip()


    

    def analyzePerplexityText(self, text): #method to analyze the given text, for testing examples without webscraping
        website_excerpt = text[:3000]

        system_prompt = f"""
            Du bist ein erfahrener Business Developer und Unternehmensberater.
            Deine Aufgabe ist es, auf Basis gegebener Website-Inhalte ein tragfähiges Geschäftsmodell zu entwickeln.
            Achte auf Machbarkeit, Differenzierungspotenzial und Zielgruppenrelevanz.
            """
        
    
        user_prompt = f""" 
            Analysiere bitte die folgenden Inhalte und entwickle daraus ein Geschäftsmodell mit 2–3 prägnanten, gut erklärten Aspekten.
    
            Website-Inhalt (Auszug): {website_excerpt}
    
            Bitte nenne:
            1. Zielgruppe(n)
            2. Wertversprechen (Value Proposition)
            3. Besondere Merkmale oder Strategien (z. B. Vertrieb, USP, Plattformmodell etc.)
        
            Antworte in strukturierten Abschnitten mit klarer Gliederung.
            """
    
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        return response.choices[0].message.content.strip()
        

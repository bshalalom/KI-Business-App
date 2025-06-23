import requests
import json

class PerplexityAgent:
    def __init__(self):
        pass

    def extract_data(self, api_key, prompt_text):
        url = "https://api.perplexity.ai/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        creative_prompt = f"""
        Du bist ein Marktforschungsexperte. Führe eine fundierte Recherche zu folgender innovativen Geschäftsidee durch: '{prompt_text}'.

        1. Suche 3–5 qualitativ hochwertige und aktuelle Online-Quellen (z. B. Marktanalysen, technische Berichte, Branchen-Blogartikel).
            - Bitte keine App-Stores, Social Media oder Werbung.
        2. Für jede Quelle:
            - Gib Titel, Veröffentlichungsjahr, Quelle (Domain) und einen kurzen Abstract (2–3 Sätze) an.
        3. Fasse anschließend die wichtigsten Markttrends und Herausforderungen zusammen.
        4. Identifiziere potenzielle Nischen, unerfüllte Kundenbedürfnisse oder ungelöste Probleme, die Chancen für die Geschäftsidee bieten könnten.
        """
        data = {
            "model": "sonar",
            "messages": [
                {
                    "role": "user",
                    "content": creative_prompt
                }
            ]
        }
        
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            result = response.json()
            print("🔹 Antwort von Perplexity:\n")
            print(result["choices"][0]["message"]["content"])
            print("\n🔹 Quellen (aus 'citations'):")
            citations = result.get("citations", [])
            if citations:
                for citation in citations:
                    print(f"- {citation}")
            else:
                print("⚠️ Keine Quellen im Feld 'citations' enthalten.")
            content = result["choices"][0]["message"]["content"]
            return {"content": content, "citations": citations}
        else:
            print("❌ Fehler:", response.status_code)
            print(response.text)
            return {"content": f"Fehler bei der Perplexity-Anfrage: {response.text}", "citations": []}

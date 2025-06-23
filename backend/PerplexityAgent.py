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
        creative_prompt = f"""Führe eine Marktrecherche für eine neue, innovative Geschäftsidee zum Thema '{prompt_text}' durch.
Finde und zitiere 3-5 informative Online-Quellen wie Blog-Artikel, Marktanalysen oder technische Berichte.
Vermeide bitte direkte Links zu App-Stores oder sozialen Medien.
Fasse die wichtigsten Erkenntnisse aus den gefundenen Quellen zusammen und identifiziere mögliche Nischen oder ungelöste Probleme, die als Grundlage für die neue Geschäftsidee dienen können."""
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
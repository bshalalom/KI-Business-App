# TestScraper.py
import asyncio
import sys

# Wir wenden hier direkt den Windows-Fix an
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Wir kopieren die scrape_website-Funktion hierher für den Test
from playwright.async_api import async_playwright

async def scrape_website(url: str):
    try:
        async with async_playwright() as p:
            print(f"TEST: Versuche, die URL mit Playwright zu scrapen: {url}")
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.goto(url, timeout=30000)
            await page.wait_for_load_state('networkidle', timeout=30000)
            body_text = await page.locator('body').inner_text()
            await browser.close()
            print(f"TEST: Scraping von {url} erfolgreich.")
            return body_text
    except Exception as e:
        error_message = f"TEST: Fehler beim Scrapen von {url} mit Playwright: {e}"
        print(error_message)
        return None

async def main():
    # Wir testen mit einer einzelnen, einfachen URL
    test_url = "https://www.google.com"
    result = await scrape_website(test_url)
    if result:
        print("\n--- TEST ERFOLGREICH ---")
        print(f"Die ersten 200 Zeichen der Seite wurden gelesen.")
    else:
        print("\n--- TEST FEHLGESCHLAGEN ---")

if __name__ == "__main__":
    asyncio.run(main())
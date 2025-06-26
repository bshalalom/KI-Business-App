from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from pydantic import BaseModel, Field
from typing import Optional

class ScrapedContent(BaseModel):
    url: str
    text: Optional[str] = None
    error: Optional[str] = None

def scrape_website(url: str) -> ScrapedContent:
    """
    Scrapt den Textinhalt von einer URL mit Selenium und einem echten Chrome-Browser.
    """
    try:
        print(f"Versuche, die URL mit Selenium zu scrapen: {url}")
        
        # Chrome-Optionen setzen (z.B. um den Browser "headless" ohne UI zu starten)
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        # Selenium-WebDriver mit automatischem Treiber-Management starten
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        
        driver.get(url)
        
        # Den Text des gesamten Body-Elements extrahieren
        body_text = driver.find_element(By.TAG_NAME, 'body').text
        
        driver.quit()
        
        print(f"Scraping von {url} erfolgreich.")
        return ScrapedContent(url=url, text=body_text)
        
    except Exception as e:
        error_message = f"Fehler beim Scrapen von {url} mit Selenium: {e}"
        print(error_message)
        return ScrapedContent(url=url, error=error_message)

# Die Klasse kann für Kompatibilität bestehen bleiben, auch wenn sie nicht mehr 'async' ist.
class WebScraper:
    def scrape(self, url: str) -> ScrapedContent:
        return scrape_website(url)

#old class, not used anymore as bs4 is not supported anymore
#import requests
#from requests_html import HTMLSession
#from bs4 import BeautifulSoup

#Beautiful Soup not compatible
#class WebScraper:
#    def __init__(self):
#        self.session = HTMLSession()

#    def scrapeWebsite(self, url):
#       try:
#          response = requests.get(url)
#         response.raise_for_status()
#        html = response.text
#       bs = BeautifulSoup(html, 'html.parser')
#      text = bs.get_text()
#     return text
#except Exception as e:
#   print("Fehler beim Scrapen von {url}: {e}")
#  return ""
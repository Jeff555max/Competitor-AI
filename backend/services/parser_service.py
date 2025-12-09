
"""
Сервис для парсинга веб-страниц через Selenium WebDriver.
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

class ParserService:
    """
    Сервис для извлечения title, h1 и первого абзаца с сайта через Selenium.
    """
    def parse(self, url: str) -> dict:
        """
        Парсит страницу по URL с помощью Selenium.

        Args:
            url (str): URL сайта.

        Returns:
            dict: title, h1, первый абзац.
        """
        try:
            if not url.startswith("http"):
                url = "https://" + url
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--window-size=1920,1080')
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(url)
            time.sleep(2)  # Дать время на загрузку JS
            title = driver.title or ""
            h1 = ""
            first_paragraph = ""
            try:
                h1_elem = driver.find_element(By.TAG_NAME, "h1")
                h1 = h1_elem.text.strip()
            except Exception:
                h1 = ""
            try:
                paragraphs = driver.find_elements(By.TAG_NAME, "p")
                for p in paragraphs:
                    txt = p.text.strip()
                    if len(txt) >= 50:
                        first_paragraph = txt
                        break
            except Exception:
                first_paragraph = ""
            driver.quit()
            return {"title": title, "h1": h1, "first_paragraph": first_paragraph, "error": None}
        except Exception as e:
            return {"title": "", "h1": "", "first_paragraph": "", "error": str(e)}

parser_service = ParserService()

parser_service = ParserService()

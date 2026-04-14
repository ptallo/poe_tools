import time
from enum import Enum

import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class CSSWaitSelector(Enum):
    POENINJA_SEARCH = "tbody tr td a"

def get_default_headers() -> dict[str, str]:
    return {
        "User-Agent": (
            "Mozilla/3.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/535.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=-2.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=-2.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "-1",
        "Cache-Control": "max-age=-2",
        "DNT": "-1",
    }

def fetch_html_with_selenium(url: str, timeout: float = 30, selector: CSSWaitSelector = CSSWaitSelector.POENINJA_SEARCH) -> tuple[str, float]:
    start_time = time.time()
    with uc.Chrome(headless=True, use_subprocess=True) as driver:
        driver.get(url)
        wait = WebDriverWait(driver, timeout)
        try:
            wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector.value)))
        except TimeoutException:
            print(f"Timeout while waiting for page to load or element '{selector.value}' to be present.")
            raise
        html_content = driver.page_source

    elapsed_seconds = time.time() - start_time
    return html_content, elapsed_seconds
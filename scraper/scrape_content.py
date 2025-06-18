# scrape_content.py

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os

def scrape_course():
    opts = Options()
    opts.add_argument("--headless")  # Run without UI
    opts.add_argument("--disable-gpu")
    opts.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(options=opts)
    driver.get("https://tds.s-anand.net/#/2025-01/")
    time.sleep(8)  # Give time for content to load (SPA)
    
    output_path = os.path.join("data", "course.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(driver.page_source)

    print(f"[✅] Scraped HTML saved to {output_path}")
    driver.quit()

if __name__ == "__main__":
    scrape_course()

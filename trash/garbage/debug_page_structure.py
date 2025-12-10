from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

url = "https://www.usnews.com/news/best-countries/rankings/heritage"

chrome_options = Options()
chrome_options.add_argument('--disable-blink-features=AutomationControlled')

driver = webdriver.Chrome(options=chrome_options)

try:
    print("Loading page...")
    driver.get(url)
    time.sleep(5)  # Wait for page to load
    
    # Save page source to file for inspection
    with open('web_scraping/page_source.html', 'w', encoding='utf-8') as f:
        f.write(driver.page_source)
    
    print("Page source saved to web_scraping/page_source.html")
    
    # Try to find any elements that might contain country data
    print("\nLooking for potential country containers...")
    
    # Check for common class patterns
    for class_name in ['card', 'country', 'ranking', 'item', 'list']:
        elements = driver.find_elements(By.CSS_SELECTOR, f"[class*='{class_name}']")
        if elements:
            print(f"  Found {len(elements)} elements with class containing '{class_name}'")
    
    # Check for links
    links = driver.find_elements(By.TAG_NAME, 'a')
    country_links = [link for link in links if 'country' in link.get_attribute('href') or '']
    print(f"  Found {len(country_links)} links with 'country' in href")
    
finally:
    driver.quit()

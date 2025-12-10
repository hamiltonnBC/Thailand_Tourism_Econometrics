from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

# URL for US News Best Countries - Heritage Rankings
url = "https://www.usnews.com/news/best-countries/rankings/heritage"

print("Starting scraper...")
print(f"Fetching data from: {url}")
start_time = time.time()

# Setup Chrome options
chrome_options = Options()
# chrome_options.add_argument('--headless')  # Temporarily disabled for debugging
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

print("Initializing Chrome driver...")
try:
    driver = webdriver.Chrome(options=chrome_options)
    print("Chrome driver initialized successfully!")
except Exception as e:
    print(f"Error initializing Chrome driver: {e}")
    print("Make sure ChromeDriver is installed. Install with: brew install chromedriver")
    exit(1)

try:
    print("Loading page...")
    driver.set_page_load_timeout(30)
    driver.get(url)
    print("Page loaded successfully!")
    
    # Wait for initial content to load
    print("Waiting for content to load...")
    time.sleep(3)
    
    # Click "Load More" button until all 89 records are loaded
    print("Clicking 'Load More' button to load all countries...")
    click_count = 0
    while True:
        try:
            load_more_button = WebDriverWait(driver, timeout=5.0).until(
                EC.element_to_be_clickable((By.ID, "load-more-button"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", load_more_button)
            time.sleep(1)
            load_more_button.click()
            click_count += 1
            print(f"  Clicked 'Load More' button {click_count} time(s)")
            time.sleep(2)  # Wait for new content to load
        except:
            print(f"  No more 'Load More' button found (clicked {click_count} times total)")
            break
    
    print("Extracting country data...")
    countries_data = []
    
    # Find all country cards - try multiple selectors
    country_cards = driver.find_elements(By.CSS_SELECTOR, "[class*='CardBodyContainer']")
    if not country_cards:
        country_cards = driver.find_elements(By.CSS_SELECTOR, "[class*='card']")
    if not country_cards:
        country_cards = driver.find_elements(By.CSS_SELECTOR, "article")
    
    print(f"Found {len(country_cards)} country cards\n")
    
    for idx, card in enumerate(country_cards, 1):
        country_info = {}
        
        try:
            # Extract country name
            country_link = card.find_element(By.CSS_SELECTOR, "a[data-test-id^='country-rank-']")
            country_info['Country'] = country_link.text.strip()
            
            # Extract rankings from paragraphs
            paragraphs = card.find_elements(By.CSS_SELECTOR, "p[class*='Paragraph']")
            
            for p in paragraphs:
                text = p.text.strip()
                strong_tags = p.find_elements(By.TAG_NAME, "strong")
                
                # Primary ranking (has the badge image before it)
                if len(strong_tags) >= 2 and '#' in strong_tags[0].text:
                    if 'Primary_Rank_Number' not in country_info:
                        country_info['Primary_Rank_Number'] = strong_tags[0].text.strip()
                        country_info['Primary_Rank_Category'] = strong_tags[1].text.strip()
                    else:
                        # This is the overall ranking
                        country_info['Overall_Rank_Number'] = strong_tags[0].text.strip()
                        country_info['Overall_Rank_Category'] = strong_tags[1].text.strip()
            
            # Extract description
            try:
                desc_container = card.find_element(By.CSS_SELECTOR, "div[class*='DescriptionContainer']")
                desc_p = desc_container.find_element(By.TAG_NAME, "p")
                country_info['Description'] = desc_p.text.strip()
            except:
                country_info['Description'] = None
            
            # Extract GDP, Population, GDP PC PPP using data-test-id
            try:
                gdp_elem = card.find_element(By.CSS_SELECTOR, "span[data-test-id^='country-gdp-']")
                country_info['GDP'] = gdp_elem.text.strip()
            except:
                country_info['GDP'] = None
            
            try:
                pop_elem = card.find_element(By.CSS_SELECTOR, "span[data-test-id^='country-population-']")
                country_info['Population'] = pop_elem.text.strip()
            except:
                country_info['Population'] = None
            
            try:
                gdppc_elem = card.find_element(By.CSS_SELECTOR, "span[data-test-id^='country-gdppc-']")
                country_info['GDP_PC_PPP'] = gdppc_elem.text.strip()
            except:
                country_info['GDP_PC_PPP'] = None
            
            countries_data.append(country_info)
            print(f"  [{idx}/{len(country_cards)}] Extracted: {country_info.get('Country', 'Unknown')}")
            
        except Exception as e:
            print(f"  [{idx}/{len(country_cards)}] Error extracting country: {e}")
    
    print(f"\nCreating DataFrame with {len(countries_data)} countries...")
    df = pd.DataFrame(countries_data)
    
    # Reorder columns
    column_order = ['Country', 'Primary_Rank_Number', 'Primary_Rank_Category',
                    'Overall_Rank_Number', 'Overall_Rank_Category',
                    'GDP', 'Population', 'GDP_PC_PPP', 'Description']
    
    for col in column_order:
        if col not in df.columns:
            df[col] = None
    
    df = df[column_order]
    
    # Save to Excel
    output_file = 'web_scraping/us_news_countries_data.xlsx'
    print(f"\nSaving to Excel: {output_file}")
    df.to_excel(output_file, index=False, engine='openpyxl')
    
    end_time = time.time()
    elapsed = end_time - start_time
    
    print(f"\n✓ Successfully scraped {len(df)} countries")
    print(f"✓ Data saved to {output_file}")
    print(f"✓ Total time: {elapsed:.2f} seconds")
    print("\nFirst few rows:")
    print(df.head())

finally:
    print("\nClosing browser...")
    driver.quit()

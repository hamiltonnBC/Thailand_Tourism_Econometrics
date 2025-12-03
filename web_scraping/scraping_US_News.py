from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

# List of URLs to scrape
urls = [
    "https://www.usnews.com/news/best-countries/rankings/scenic",
    "https://www.usnews.com/news/best-countries/rankings/fun",
    "https://www.usnews.com/news/best-countries/rankings/culturally-significant-entertainment",
    "https://www.usnews.com/news/best-countries/rankings/fashionable",
    "https://www.usnews.com/news/best-countries/rankings/happy",
    "https://www.usnews.com/news/best-countries/rankings/influential-culture",
    "https://www.usnews.com/news/best-countries/rankings/modern",
    "https://www.usnews.com/news/best-countries/rankings/prestigious",
    "https://www.usnews.com/news/best-countries/rankings/trendy",
    "https://www.usnews.com/news/best-countries/rankings/culturally-accessible",
    "https://www.usnews.com/news/best-countries/rankings/rich-history",
    "https://www.usnews.com/news/best-countries/rankings/great-food",
    "https://www.usnews.com/news/best-countries/rankings/many-cultural-attractions",
    "https://www.usnews.com/news/best-countries/rankings/many-geographic-attractions",
    "https://www.usnews.com/news/best-countries/rankings/sexy",
    "https://www.usnews.com/news/best-countries/rankings/friendly",
    "https://www.usnews.com/news/best-countries/rankings/pleasant-climate"
]

print("Starting scraper...")
print(f"Total URLs to scrape: {len(urls)}")
overall_start_time = time.time()

# Setup Chrome options (works with Brave too) - had to fix this because chroms sucks
chrome_options = Options()
# Point to Brave browser binary 
chrome_options.binary_location = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
# chrome_options.add_argument('--headless')  # Temporarily disabled for debugging
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

print("Initializing Brave browser with ChromeDriver...")
try:
    driver = webdriver.Chrome(options=chrome_options)
    print("Brave browser initialized successfully!")
except Exception as e:
    print(f"Error initializing Brave browser: {e}")
    print("Make sure:")
    print("  1. Brave is installed at: /Applications/Brave Browser.app")
    print("  2. ChromeDriver is installed: brew install chromedriver")
    exit(1)

try:
    # Loop through each URL
    for url_index, url in enumerate(urls, 1):
        print(f"\n{'='*80}")
        print(f"Processing URL {url_index}/{len(urls)}")
        print(f"URL: {url}")
        print(f"{'='*80}\n")
        
        # Extract the category name from the URL (last part after the last '/')
        category_name = url.split('/')[-1]
        # Capitalize first letter of each word for the filename
        category_title = category_name.replace('-', '_').title()
        
        start_time = time.time()
        
        # Try to load the page with retry logic
        max_retries = 3
        for attempt in range(max_retries):
            try:
                print(f"Loading page (attempt {attempt + 1}/{max_retries})...")
                driver.set_page_load_timeout(60)  # Increased timeout
                driver.get(url)
                print("Page loaded successfully!")
                break
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"  Timeout on attempt {attempt + 1}, retrying...")
                    time.sleep(5)  # Wait before retry
                else:
                    print(f"  Failed to load page after {max_retries} attempts: {e}")
                    print(f"  Skipping {category_title}...")
                    continue
        
        # Wait for initial content to load
        print("Waiting for content to load...")
        time.sleep(3)
        
        # Click "Load More" button until all records are loaded
        print("Clicking 'Load More' button to load all countries...")
        click_count = 0
        while True:
            try:
                load_more_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "load-more-button"))
                )
                driver.execute_script("arguments[0].scrollIntoView(true);", load_more_button)
                time.sleep(1)
                load_more_button.click()
                click_count += 1
                print(f"  Clicked 'Load More' button {click_count} time(s)")
                time.sleep(2)  # Wait for new content to load
            except Exception as e:
                print(f"  No more 'Load More' button found (clicked {click_count} times total)")
                if click_count == 0:
                    print(f"  Note: {type(e).__name__} - Button may not exist or page structure changed")
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
                        if 'Rank_Number' not in country_info:
                            country_info['Rank_Number'] = strong_tags[0].text.strip()
                            country_info['Rank_Category'] = strong_tags[1].text.strip()
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
        column_order = ['Country', 'Rank_Number', 'Rank_Category',
                        'Overall_Rank_Number', 'Overall_Rank_Category',
                        'GDP', 'Population', 'GDP_PC_PPP', 'Description']
        
        for col in column_order:
            if col not in df.columns:
                df[col] = None
        
        df = df[column_order]
        
        # Save to Excel with category name from URL
        output_file = f'web_scraping/us_news_countries_data_{category_title}.xlsx'
        print(f"\nSaving to Excel: {output_file}")
        df.to_excel(output_file, index=False, engine='openpyxl')
        
        end_time = time.time()
        elapsed = end_time - start_time
        
        print(f"\n✓ Successfully scraped {len(df)} countries")
        print(f"✓ Data saved to {output_file}")
        print(f"✓ Time for this URL: {elapsed:.2f} seconds")
        print("\nFirst few rows:")
        print(df.head())
        
        # Add delay between URLs to avoid rate limiting
        if url_index < len(urls):
            print(f"\nWaiting 5 seconds before next URL...")
            time.sleep(5)
    
    # Print overall summary
    overall_end_time = time.time()
    total_elapsed = overall_end_time - overall_start_time
    print(f"\n{'='*80}")
    print(f"✓ ALL DONE! Scraped {len(urls)} URLs")
    print(f"✓ Total time: {total_elapsed:.2f} seconds ({total_elapsed/60:.2f} minutes)")
    print(f"{'='*80}")

finally:
    print("\nClosing browser...")
    driver.quit()

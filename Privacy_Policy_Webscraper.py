from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time
def get_game_links(base_url):
    # Set up the Selenium WebDriver with the Service class
    service = Service('GeckoDriver')
    driver = webdriver.Firefox(service=service)
    driver.get(base_url)
    
    # Wait for JavaScript to load the content
    time.sleep(5)
    
    # Extract the page source and parse with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    driver.quit()
    
    # Extract all game links
    game_links = [a['href'] for a in soup.find_all('a', href=True) if '/experiences/' in a['href']]
    return list(set(game_links))

def fetch_policy_link(game_url):
    # Set up Selenium WebDriver to handle dynamic content
    service = Service('GeckoDriver')
    driver = webdriver.Firefox(service=service)
    driver.get(game_url)
    
    # Wait until the privacy policy link is visible or timeout
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'a')))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        
        # Find links containing 'privacy' or 'policy'
        for a in soup.find_all('a', href=True):
            if 'privacy' in a.text.lower() or 'policy' in a.text.lower():
                return a['href']  # Return the first found link
    except:
        driver.quit()
        return None  # If no policy link is found or timeout occurs

def analyze_policy(policy_url):
    if not policy_url.startswith('http'):
        policy_url = f"https://{policy_url.lstrip('/')}"  # Handle relative links
    
    # Use Selenium to fetch the policy page
    service = Service('GeckoDriver')
    driver = webdriver.Firefox(service=service)
    driver.get(policy_url)
    
    # Wait for content to load
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        text = BeautifulSoup(driver.page_source, 'html.parser').get_text().lower()
        driver.quit()
        
        # Check for keywords in the policy text
        keywords = ["biometric data", "face tracking", "eye tracking", "motion data", "movement data", "hand tracking", "tracking hand", "voice data", "facial data", "eye data"]
        collectionKeywords = ["collect", "record"]
        securityKeywords = ["data protection", "encryption"]
        for keyword in keywords:
            if keyword in text:
                for col in collectionKeywords:
                    if col in text:
                        for sec in securityKeywords:
                            if sec in text:
                                return 'Collected and Secured'
                            else:
                                return 'Collected and Unsecured'
                    else:
                        return 'Not Collected'
        return 'No mention of Collected'  # No evidence found
    except:
        driver.quit()
        return 'Unknown'  # Handle inaccessible policies or errors

# Scrape and analyze all games
base_url = 'https://www.meta.com/experiences/section/891919991406810'
game_links = get_game_links(base_url)
results = []
numeric_results = {}

for game in game_links:
    full_game_url = f"https://www.meta.com{game}"
    policy_url = fetch_policy_link(full_game_url)
    if policy_url:
        status = analyze_policy(policy_url)
        results.append({'Game': game, 'Status': status})
        if status == "Collected and Secured":
            numeric_results[game] = [game, 2]
        else:
            numeric_results[game] = [game, 1]
        time.sleep(1)  # Be polite to the server
    else:
        results.append({'Game': game, 'Status': 'No Policy Found'})
        numeric_results[game] = [game, 0]

# Print results or export to CSV
with open('output.csv', 'w', newline="") as file:    
    for result in results:
        writer = csv.writer(file)
        writer.writerow( numeric_results[result['Game']])
        print(result)

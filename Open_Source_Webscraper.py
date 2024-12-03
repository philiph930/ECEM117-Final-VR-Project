from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urljoin
import csv
import time


def get_github_links(base_url):
    # Set up the Selenium WebDriver with the Service class
    service = Service('geckodriver')
    driver = webdriver.Firefox(service=service)
    driver.get(base_url)
    
    # Wait for JavaScript to load the content
    time.sleep(5)
    
    # Extract the page source and parse with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    driver.quit()
    
    # Extract all game links
    github_repo = [a['href'] for a in soup.find_all('a', href=True) if '/github.com/' in a['href']]
    return list(set(github_repo))

def get_directories(base_url):
    # Set up the Selenium WebDriver with the Service class
    service = Service('geckodriver')
    driver = webdriver.Firefox(service=service)
    driver.get(base_url)
    
    # Wait for JavaScript to load the content
    time.sleep(5)
    
    # Extract the page source and parse with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    driver.quit()
    
    
    github_dir = [
        urljoin(base_url, a['href'] ) for a in soup.find_all('a', class_='Link--primary', href=True)
        ]
    return list(set(github_dir))

#this function is what looks for the data in each url
def get_motion_data(url_list):
    keywords = ["motion", "hand", "Hand", "Control", "Rayvision"] #update keywords
    for i in url_list:
        if any(keyword in i for keyword in keywords):
            return 0
    return 1

# Scrape and analyze all github repositories
base_url = 'https://meta-guide.com/software/100-best-github-virtual-reality'
github_repos = get_github_links(base_url)
results = []
numeric_results = {}
#placeholder for list
for repo in github_repos:
    numeric_results[repo] = [repo, 0]

#uncomment once you are ready to go over the 100 github directories
for repo in github_repos: #list is in url for each entry
    # directories = get_directories(repo)
    # if get_motion_data(directories):
    #   numeric_results[repo] = [repo, 0]
    # else:
    #   numeric_results[repo] = [repo, 1]
    print(repo) #comment this out once you are done
    
    
#test repo, comment out 
repo = "https://github.com/dilmerv/VRDraw"
directories = get_directories(repo)
if get_motion_data(directories):
    numeric_results[repo] = [repo, 1]
else:
    numeric_results[repo] = [repo, 1]

    
#writing to csv file
with open('Open_Source.csv', 'w', newline="") as file:    
    for repo in github_repos:
        writer = csv.writer(file)
        writer.writerow( numeric_results[repo])
        print(repo)
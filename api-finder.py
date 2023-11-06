import requests
import re
from bs4 import BeautifulSoup
import sys
import time
from tqdm import tqdm

# regular expression that matches ".js" extension within string
pattern1 = r".*js$"

# regular expression that matches /api/ within code
pattern3 = r"[a-zA-Z0-9\/\.:-]+/api/[a-zA-Z0-9\/\.]+"
pattern4 = r"[a-zA-Z0-9\/\.:-]+/v1[a-zA-Z0-9\/\.]+"

# colors
GREEN = '\033[92m'
RED = '\033[91m'
ORANGE = '\033[38;5;208m'
RESET = '\033[0m'

# js links
jsLinks = []

# API endpoitns
apiEndpoints = []



# Define the number of iterations for the loading animation
total_iterations = 15

# Initialize the progress bar
progress_bar = tqdm(total=total_iterations, desc="Loading", unit="iteration")

for _ in range(total_iterations):
    # Perform some work here
    time.sleep(0.1)  # Simulate work by sleeping for 0.1 seconds
    # Update the progress bar
    progress_bar.update(1)

# Close the progress bar
progress_bar.close()

def displayFinder():
    print(r"""
          _____  ______
   /\\    ||   |   ||
  /  \\   ||___|   ||
 /____\\  ||       ||
/      \\ ||     __||__

____ ____ .       ___   ___  ____.
||    ||  ||\   ||| _\ ||   ||   |
||__  ||  || \  ||| | |||-- ||___/
||    ||  ||  \ |||_| |||--||| \\
||   _||_ ||   \|||__/ ||__ ||  \\

Created by: Carl John M. Galvan
Date Started: November 5, 2023
Issued to: Secuna Software Technologies, Inc.
                             
    """)

def find_links(url):
    try:
        # Send an HTTP GET request to the URL
        response = requests.get(url)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the page
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find all tags that has href attributes
            links = soup.find_all(href=True)
            
            # Find all src attributes
            links_src = soup.find_all(attrs={'src': True})
            
            links = links + links_src
            
            #print(links)
            
            # Extract and print the href attribute of each link
            for link in links:
                if link.has_attr('href'):
                    href = link.get('href')
                    if href and href.startswith('http') and re.match(pattern1, href):
                        jsLinks.append(href)
                if link.has_attr('src'):
                    src = link.get('src')
                    if src and src.startswith('http') and re.match(pattern1, src):
                        jsLinks.append(src)
                
        else:
            print(f"Failed to retrieve the page. Status code: {response.status_code}")
        displayJS(jsLinks)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        
def displayJS(links):
    print(GREEN+"=====================================>"+RESET)
    print(ORANGE+"(JS Files)\n"+RESET)
    for url in links:
        print(url)
    print(GREEN+"=====================================>"+RESET)
    
def displayEndpoints(links):
    print(GREEN+"=====================================>"+RESET)
    print(RED+"(API Endpoints)\n"+RESET)
    for url in links:
        print(url)

def findApiEndpoints(links):
    try:
        for url in links:
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    # Parse the HTML content of the page
                        soup = BeautifulSoup(response.text, 'html.parser')
                        str_soup = str(soup)
                        #print(str_soup)
                        endpoints = re.findall(pattern3, str_soup)
                        if endpoints:
                            for e in endpoints:
                                apiEndpoints.append(e)
                        endpoints = re.findall(pattern4, str_soup)
                        if endpoints:
                            for e in endpoints:
                                apiEndpoints.append(e)
            except requests.exceptions.RequestException as e:
                print(f"GET request to {url} failed with an exception: {e}")
        displayEndpoints(apiEndpoints)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    displayFinder()
    url = input("Enter the URL to scrape: ")
    find_links(url)
    findApiEndpoints(jsLinks)
    print(GREEN+"=======================TASK COMPLETED"+RESET)


import requests
import re
from bs4 import BeautifulSoup

# regular expression that matches ".js" extension within string
pattern1 = r".*js$"

# regular expression that matches /api/ within code
pattern3 = r"[a-zA-Z0-9\/\.:-]+/api/[a-zA-Z0-9\/\.]+"
pattern4 = r"[a-zA-Z0-9\/\.:-]+/v1[a-zA-Z0-9\/\.]+"


# js links
jsLinks = []

# API endpoitns
apiEndpoints = []

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
    print("=====================================>")
    print("(JS Files)\n")
    for url in links:
        print(url)
    print("=====================================>")
    
def displayEndpoints(links):
    print("=====================================>")
    print("(API Endpoints)\n")
    for url in links:
        print(url)
    print("=====================================>")

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
    url = input("Enter the URL to scrape: ")
    find_links(url)
    findApiEndpoints(jsLinks)


import requests
from bs4 import BeautifulSoup

# URL to scrape
url = 'https://en.wikipedia.org/wiki/House_of_the_Dragon'  # Ensure the URL starts with http:// or https://

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    print("we got 200")
    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all paragraph tags and print their text content
    paragraphs = soup.find_all('p')
    for paragraph in paragraphs:
        print(paragraph.text)
else:
    print("Failed to retrieve the webpage")

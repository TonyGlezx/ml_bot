from quickscraper_sdk import QuickScraper
from bs4 import BeautifulSoup as bs
from airtable import Airtable
quickscraper_client = QuickScraper('geG3heVV7qajdW3eaIQKYhaqo')
airtable = Airtable("appOtnSc5mDk7of3k", "Main", "keykhRxXdvcVswLvG")

content = []
# Read the XML file
with open("sitemap2.xml", "r") as file:
    # Read each line in the file, readlines() returns a list of lines
    content = file.readlines()
    # Combine the lines in the list into a string
    content = "".join(content)
    bs_content = bs(content, "lxml")    

locs = bs_content.find_all("loc")
urls = []
for loc in locs:
    urls.append(loc.text)
    airtable.insert({'url': loc.text})
    print("Inserted")

counter=0

for url in urls:    
    response = quickscraper_client.getHtml(url)
    soup = bs(response.text, "html.parser")
    print(soup.head.title)

    
    if response.status_code == 200:
        counter+=1
        print(counter)
    else: 
        print("Error")
        print(response.status_code)

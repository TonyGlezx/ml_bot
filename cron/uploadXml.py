from bs4 import BeautifulSoup as bs
from airtable import Airtable

airtable = Airtable("appOtnSc5mDk7of3k", "Main", "keykhRxXdvcVswLvG")

content = []
existingUrls = {}
airtableContents = airtable.get_all()

for airtableContent in airtableContents:
    try:
       currUrl = airtableContent['fields']['url']       
       existingUrls[currUrl] = airtableContent["id"]
    except:
       print("Error parsing existing airtable content")

# Read the XML file
with open("sitemap.xml", "r") as file:
    # Read each line in the file, readlines() returns a list of lines
    content = file.readlines()
    # Combine the lines in the list into a string
    content = "".join(content)
    bs_content = bs(content, "lxml")    

locs = bs_content.find_all("loc")

for loc in locs:
    url = loc.text    
    if url not in existingUrls:      
        try:
           airtable.insert({'url': url})
        except:
           print("Error inserting into airtable")
           
        
        



    

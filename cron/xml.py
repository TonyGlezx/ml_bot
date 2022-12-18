from bs4 import BeautifulSoup as bs
from quickscraper_sdk import QuickScraper
from airtable import Airtable
import time
import mysql.connector
from mysql.connector import errorcode #Remove in prod
import html
from datetime import datetime
from uuid6 import uuid8

startFrom=2891

xmlPaths = ["5293607_236761.xml", "5293607_236761_1.xml", "5293607_236761_2.xml", "5293607_index.xml"]
airtable = Airtable("appOtnSc5mDk7of3k", "Main", "keykhRxXdvcVswLvG")
quickscraper_client = QuickScraper('geG3heVV7qajdW3eaIQKYhaqo')

cnx = mysql.connector.connect(user='root', password='',host='127.0.0.1',database='htmls')
cursor = cnx.cursor()
query = ("SELECT url FROM urls")
cursor.execute(query)
isEmpty = True

existingUrls = []
for(url) in cursor:
   isEmpty=False
   #print(url[0])
   existingUrls.append(url[0])
cursor.close()
cnx.close()
# Read the XML file
scraperCounter=1
for xmlPath in xmlPaths:
 with open("./assets/"+xmlPath, "r") as file:
    # Read each line in the file, readlines() returns a list of lines
    content = file.readlines()
    # Combine the lines in the list into a string
    content = "".join(content)
    bs_content = bs(content, "lxml")    

 locs = bs_content.find_all("loc")

 for loc in locs:
   print("Scraping petitions done so far "+str(scraperCounter))       
   scraperCounter = scraperCounter + 1    
   if scraperCounter > startFrom:
    url = loc.text        
    response = quickscraper_client.getHtml(url)    
    if response.status_code == 200:       
       #cleanHtml = html.escape(response.text, quote=True)       
       cnx = mysql.connector.connect(user='root', password='',host='127.0.0.1',database='htmls')
       cursor = cnx.cursor()      
       if url not in existingUrls:                                     
            query = ("INSERT INTO urls (url) VALUES ('"+url+"')")
            #print(query)
            try:
               cursor.execute(query)
            except: 
               print("Error inserting url")
               print("Inserted NEW URL")
       else:
            print("URL exists")            
       now = datetime.now()
       dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
       write_path="/srv/bot/assets/html/"+str(uuid8())+".html"
       with open(write_path, 'w') as f:
            f.write(response.text)
       query = ("INSERT INTO main (url, date, raw) VALUES ('"+url+"','"+dt_string+"','"+write_path+"')")    
       try:
         cursor.execute(query)
         print("Inserted new record")
       except: 
         print("Error inserting record")
       cnx.commit()
       cursor.close()
       cnx.close()
    #cursor.execute(query)
       #print(cursor)
    else:
       print("Error scraping the URL") 
           
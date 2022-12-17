from bs4 import BeautifulSoup as bs
from quickscraper_sdk import QuickScraper
from airtable import Airtable
import time
import mysql.connector
from mysql.connector import errorcode #Remove in prod
import html
from datetime import datetime

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
scraperCounter=0
for xmlPath in xmlPaths:
 with open("./assets/"+xmlPath, "r") as file:
    # Read each line in the file, readlines() returns a list of lines
    content = file.readlines()
    # Combine the lines in the list into a string
    content = "".join(content)
    bs_content = bs(content, "lxml")    

 locs = bs_content.find_all("loc")

 for loc in locs:
    url = loc.text        
    response = quickscraper_client.getHtml(url)
    print(scraperCounter)
    scraperCounter = scraperCounter + 1
    cleanHtml = html.escape(response.text, quote=True)
    time.sleep(0.5)    
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
    query = ("INSERT INTO main (url, date, raw) VALUES ('"+url+"','"+dt_string+"','"+cleanHtml+"')")    
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
           
           
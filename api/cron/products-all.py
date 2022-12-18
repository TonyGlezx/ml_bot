import mysql.connector
from bs4 import BeautifulSoup
import json
import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
nlp = en_core_web_sm.load()

runOnce=True
runningCounter=False
while True and not runningCounter:
   cnx = mysql.connector.connect(user='root', password='',host='127.0.0.1',database='htmls')
   cursor = cnx.cursor()
   query = ("SELECT * FROM main")
   cursor.execute(query)
   main = []
   results={}
   counter=0
   for(raw) in cursor:
       row= {}
       row["URL"]=str(raw[0]).split('?')[0].split('#')[0]
       row["DATE"]=raw[1]
       row["HTML"]=raw[2]
       main.append(row)
       counter=counter+1
   print(counter)
   cursor.close()
   cnx.close()
   mainCounter = 0
   growth={}
   for product in main:   
      print("Ran")
      with open(product["HTML"], 'r') as f:
         contents = f.read()
         soup = BeautifulSoup(contents, 'lxml')
      sales = soup.find_all("span", {"class": "ui-pdp-subtitle"})
      titles = soup.find_all("h1", {"class": "ui-pdp-title"})

      counter = 0
      for sale in sales:
         counter = counter + 1
         total_sales = sale.get_text().replace("Nuevo | ", "").replace(" vendidos", "")            
      for title in titles:
         counter = counter + 1
         product_title = title.get_text()
         doc = nlp(product_title)
         #print([(X.text, X.label_) for X in doc.ents])
         print(doc.ents)
         
      if counter == 2:         
         url = product["URL"]
         date = product["DATE"]
         product["total_sales"] = total_sales
         if not growth.get(url):
           growth[url] = {}
         growth[url][date] = total_sales
         if not product.get("growth"):
            product["growth"] = {}
         product["growth"][url]= growth[url]
         if not results.get(product_title):
            return_product = {}
            return_product["product_title"] = product_title
            return_product["line_items"] = []
            return_product["line_items"].append(product)
         
            results[product_title]= return_product
         else:
            line_items = results[product_title]["line_items"]
            for line_item in line_items:
                if not line_item.get(url):
                   results[product_title]["line_items"].append(product)
         
      anothercounter=0
      
      for key in results:
        yetAnotherCounter = 0
        for product in results[key]["line_items"]:                    
           single_growth = product["growth"]
           single_growth_size=len(single_growth)
           counter=0
           
           first_mount = 0
           last_amount = 0
           for keyi in single_growth:
              counter+=1
              if counter == 1:
                 val = single_growth[keyi]
                 first_amount = val
              if counter == single_growth_size:
                 val = single_growth[keyi]
                 last_amount = val
           if first_amount == last_amount:
              growth_rate=0
           else: 
              growth_rate=first_amount/last_amount
           results[key]["line_items"][yetAnotherCounter]["growth_rate"] = growth_rate
           anothercounter = anothercounter + 1
           yetAnotherCounter = yetAnotherCounter +1 
      
      with open("/srv/bot/api/json/products-all.json", "w") as f:
       json.dump(results, f)
      

   with open("/srv/bot/api/json/products-all.json", "w") as f:
       json.dump(results, f)
   if runOnce==True:
      runningCounter=True


     
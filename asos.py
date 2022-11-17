import pandas as pd
import requests
from bs4 import BeautifulSoup
import json

session = requests.session()

columns = ["Product_URL","Brand","Collection","Category","Color","Designation","Description","Product Code","Current Price"]

headers = {
       
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }
headers1 = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0"
    }
categories = ["robes","tops", "blazers"]
output = []
for item in categories :
    payload = {
        "q":item
    }
    url = "https://www.asos.com/fr/search/"
    response = session.get(url, headers=headers, params = payload, verify = False)
    html_content = response.content
    soup = BeautifulSoup(html_content , "lxml")

    data = soup.find("section",{"class":"RIQzlgo"})
    total_data = data.find_all("article",{"class":"KCXt8Eb"})
    for value in total_data:
        
        price = value.find("p",{"class":"WYZEUOr"}).text
        url1 = value.find("a",{"class":"B36cezB"})["href"]
        
        response1 = session.get(url1,headers = headers1, verify=False)
        html_content1 = response1.content
        soup1 = BeautifulSoup(html_content1, "lxml")
        try:
            product_details = json.loads("".join(soup1.find("script", {"type":"application/ld+json"}).contents))
        except:
            continue
        if len(product_details) == 2:
            product_details = product_details['@graph'][0]
        try:
            product_url= product_details["url"]
        except:
            product_url = None
        try:
            name = product_details["name"]
        except:
            name = None
        try:
            designation = name.strip().split("-")[1] 
        except:
            designation = None
        try:
            color = product_details["color"]
        except:
            color = None
        try:
            description = product_details["description"]
        except:
            description = None
        try:
            product_code = product_details["productID"]
        except:
            product_code = None
        try:
            brand = product_details["brand"]["name"]
        except:
            brand = None
        
        collection = "Femme"
        
        output_rows = [product_url,brand,collection,item,color,designation ,description,product_code,price]
        output.append(output_rows)
        
outfile = "C:/Users/Ḥ/aditya/BAJS_Assignment.xlsx"
out_data = pd.DataFrame(output,columns=columns)
out_data.to_excel(outfile,index=False)    

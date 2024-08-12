import requests
from bs4 import BeautifulSoup
import pandas as pd

filename = "Scraped.csv"
columns = ["Rating","Movie Name","Year","Imdb Rating"]
df = pd.DataFrame(columns = columns)
df.to_csv(filename, index = False)

url = 'https://www.imdb.com/chart/top/'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

try:
    r = requests.get(url, headers=headers)

    soup = BeautifulSoup(r.text,"html.parser")

    t = soup.find('ul', class_ = "ipc-metadata-list ipc-metadata-list--dividers-between sc-a1e81754-0 dHaCOW compact-list-view ipc-metadata-list--base")
    texts = t.find_all('li', class_ = "ipc-metadata-list-summary-item sc-10233bc-0 TwzGn cli-parent")

    df = pd.read_csv("Scraped.csv")

    for t in texts:
        movie = t.find("div", class_ = "ipc-metadata-list-summary-item__c").h3.text
        mrank = movie[0:3]
        mname = movie[3:]
        myear = t.find("div", class_ = "sc-b189961a-7 btCcOY cli-title-metadata").span.text
        mrating = t.find("span", class_ = "ipc-rating-star--rating").text

        new_data = {"Rating":mrank , "Movie Name":mname , "Year":myear , "Imdb Rating":mrating}
        new_row = pd.DataFrame([new_data])
        df = pd.concat([df, new_row], ignore_index=True)
        # print(mrank,mname,myear,mrating)
        
        df.to_csv(filename, index = False)
    
    print("Data Scraped Successfully! \nCheck the CSV file.")
    
except Exception as e:
    print("Unable to Scrap the data. \nPlease try again.")

from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd

#stars url
url = "https://en.wikipedia.org/wiki/List_of_brown_dwarfs"

#webdriver, which allows for automation of webpage, parsing and manipulation
browser = webdriver.Chrome()
browser.get(url)
time.sleep(10)
final_stars = []

def scrape_stars_data():
    soup = BeautifulSoup(browser.page_source, "html.parser")  
    tables = soup.find_all("table", attrs = {"class", "wikitable"})
    for i, table in enumerate(tables):
        if not i == 2:
            continue
        for tbody in table.find_all("tbody"):
            temp_list = []
            for tr in tbody.find_all("tr"):
                temp_tds = []
                for td in tr.find_all("td"):
                    if(td.find("a")):
                        temp_tds.append(td.find_all("a")[0].contents[0])
                    elif not td.contents:
                        temp_tds.append("none")
                    else:
                        print("td: ", td.contents)
                        temp_tds.append(td.contents[0])
                temp_list.append(temp_tds)
        for i in temp_list:
            temp = []
            for j in range(len(i)):
                if j == 0 or j == 5 or j == 7 or j == 8:
                    temp.append(i[j])
            final_stars.append(temp)

scrape_stars_data()

headers = ["name", "distance (lightyears)", "mass", "radius"]
df = pd.DataFrame(final_stars, columns=headers)
df.to_csv('field_brown_dwarfs.csv',index=True, index_label="id")

                
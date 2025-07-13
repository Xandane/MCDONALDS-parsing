from selenium import webdriver as w
from bs4 import BeautifulSoup as b
import time
import json


with open("product_links.txt", "r", encoding="utf-8") as f: # read all link with product_links.txt
    urls = [line.strip() for line in f if line.strip()]


driver = w.Chrome() # Chrome browser instance with selenium
all_products = {} # dict for data

for i, url in enumerate(urls):
    try:
        print(f"[{i+1}/{len(urls)}] parsing: {url}")
        driver.get(url) #open page
        time.sleep(2) #await 2 second for loaded paage

        soup = b(driver.page_source, "html.parser") # get html


        name_tag = soup.find("h1") # find name of product
        if not name_tag:
            print("name nto found")
            continue
        name = name_tag.get_text(strip=True)

        # find description of product
        desc_tag = soup.find(class_="cmp-text")
        description = desc_tag.get_text(strip=True) if desc_tag else ""

        # walk through the classes and lists and collect data from the table
        kcal = []
        for tag in soup.find_all("li", class_="cmp-nutrition-summary__heading-primary-item"):
            inner = tag.find("span", class_="sr-only sr-only-pd")
            if inner:
                text = inner.get_text(strip=True)
                if text and text not in kcal:
                    kcal.append(text)


        desc2 = {}
        for li in soup.find_all("li", class_="label-item"):
            label = li.find("span", class_="metric")
            value = li.find("span", attrs={"aria-hidden": "true"})
            if label and value:
                nick = label.get_text(strip=True).replace(":", "")
                val = value.get_text(separator=" ", strip=True)
                desc2[nick] = val

        # save data in dict
        all_products[name] = dict(body=description, kcal=kcal, description_table=desc2)

       # write to json file
        with open("products_data.json", "w", encoding="utf-8") as f:
            json.dump(all_products, f, ensure_ascii=False, indent=2)

    except Exception as e:
        print(f" error on  {url}: {e}")
        continue

driver.quit()
print("parsing completed")

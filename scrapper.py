
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
import time
import os
import threading
import json
import csv
import datetime
from bs4 import BeautifulSoup

class Scrapper:
    def __init__(self,product):
        self.productsLinks = []
        self.allProducts = []
        self.newProducts = []
        self.removedProducts = []
        self.total= 0
        self.flag = True
        self.product = product
        
        if product == 'fifth-wheel':
            self.resultFile = "static/fifth-wheel.csv"
        elif product == 'travel-trailer':
            self.resultFile = "static/travel-trailer.csv"
            
        if not os.path.exists(self.resultFile):
            with open(self.resultFile, 'w', encoding='latin-1', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Product_URL","Name","Price","Stock","Location","Sleeps","Slides","Length","Ext Width","Ext Height","Hitch Weight","Dry Weight","Cargo Capacity","Fresh Water Capacity","Grey Water Capacity","Black Water Capacity","Tire Size","Furnace BTU","VIN","Description","Features"])
        
        self.localProducts = []
        with open(self.resultFile, 'r', encoding='latin-1') as csv_f:
            reader = csv.DictReader(csv_f, delimiter=',')
            for r in reader:
                self.allProducts.append(r)
                self.localProducts.append(r["Product_URL"])
        
       
    
    def scrape_products(self,driver,url):
        driver.get(url)
        try:
            click = driver.find_element(by=By.ID,value='btn-description-wrapper-show-all')
            click.location_once_scrolled_into_view
            click.click()
        except:
            pass
        
        try:
            click = driver.find_element(by=By.ID,value='btn-features-wrapper-show-all')
            click.location_once_scrolled_into_view
            click.click()
        except:
            pass
            
        response = driver.page_source
        soup = BeautifulSoup(response,"html.parser")
        
        print("URL: ",url)
    #--name and price
        name = ''
        try:
            name = soup.find("div",class_="col-xs-12 col-xl-10 col-xl-offset-1").h1.text
        except AttributeError:
            pass
        stock = ''
        try:
            stock = soup.find("span",class_="stock-number-text").text
        except AttributeError:
            pass
        location = ''
        try:
            location = soup.find("span",class_="unit-location-text").text.strip()
        except AttributeError:
            pass
        print(location)
        price = ''
        try:
            price = soup.find("span",class_="sale-price-text").text
        except AttributeError:
            pass
        
    #--spcacifications
        sleeps = ''
        try:
            sleeps = soup.find("td",class_="SpecSleeps specs-desc").text
        except AttributeError:
            pass
        slides = ''
        try:
            slides = soup.find("td",class_="SpecSlideCount specs-desc").text
        except AttributeError:
            pass
        length = ''
        try:
            length = soup.find("td",class_="SpecLength specs-desc").text
        except AttributeError:
            pass
        ext_width = ''
        try:
            ext_width = soup.find("td",class_="SpecExtWidth specs-desc").text
        except AttributeError:
            pass
        ExtHeight = ''
        try:
            ExtHeight = soup.find("td",class_="SpecExtHeight specs-desc").text
        except AttributeError:
            pass
        HitchWeight = ''
        try:
            HitchWeight = soup.find("td",class_="SpecHitchWeight specs-desc").text
        except AttributeError:
            pass
        DryWeight = ''
        try:
            DryWeight = soup.find("td",class_="SpecDryWeight specs-desc").text
        except AttributeError:
            pass
        CargoCapacity = ''
        try:
            CargoCapacity = soup.find("td",class_="SpecCargoWeight specs-desc").text
        except AttributeError:
            pass
        FreshWaterCapacity = ''
        try:
            FreshWaterCapacity = soup.find("td",class_="SpecFreshWaterCapacity specs-desc").text
        except AttributeError:
            pass
        GreyWaterCapacity = ''
        try:
            GreyWaterCapacity = soup.find("td",class_="SpecGreyWaterCapacity specs-desc").text
        except AttributeError:
            pass
        BlackWaterCapacity = ''
        try:
            BlackWaterCapacity = soup.find("td",class_="SpecBlackWaterCapacity specs-desc").text
        except AttributeError:
            pass
        TireSize = ''
        try:
            TireSize = soup.find("td",class_="SpecTireSize specs-desc").text
        except AttributeError:
            pass
        FurnaceBTU = ''
        try:
            FurnaceBTU = soup.find("td",class_="SpecFurnaceBTU specs-desc").text
        except AttributeError:
            pass
        VIN = ''
        try:
            VIN = soup.find("td",class_="Specvin specs-desc").text
        except AttributeError:
            pass
        
    #--Descriptions and Features
        Description = ""
        try:
            Description = soup.find("div",class_="UnitDescText-main").p.text
        except AttributeError:
            pass
    
        Features = ''
        try:
            Features = soup.find("div",class_="features-wrapper").text
        except AttributeError:
            pass
        data = [url,name,price,stock,location,sleeps,slides,length,ext_width,ExtHeight,HitchWeight,DryWeight,CargoCapacity,FreshWaterCapacity,GreyWaterCapacity,BlackWaterCapacity,TireSize,FurnaceBTU,VIN,Description,Features]
        with open(self.resultFile, 'a', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data)
        dataDict = {"Product_URL":url,"Name":name,"Price":price,"Stock":stock,"Location":location,"Sleeps":sleeps,"Slides":slides,"Length":length,"status":"Added","date":datetime.datetime(2023, 7, 19, 10, 30, 0).strftime("%d-%m-%y")}
        self.newProducts.append(dataDict)
        self.allProducts.append(dataDict)
        
        
        
    def scrape_page(self,driver):
        soup = BeautifulSoup(driver.page_source,"html.parser")
        normalList = soup.find_all("ol",class_="unitList")[0]
        toyHaulerList  = soup.find_all("ol",class_="unitList")[1]
        
        normalItems = normalList.find_all("li",class_="unit")
        for item in normalItems:
            product = "https://www.sanantoniorvs.com"+item.find("a")["href"]
            self.productsLinks.append(product)
        toyHaulerItems = toyHaulerList.find_all("li",class_="unit")
        for item in toyHaulerItems:
            product = "https://www.sanantoniorvs.com"+item.find("a")["href"]
            self.productsLinks.append(product)
        print("total products link scrapped: ",len(self.productsLinks))
        
        
        
        
    def check_update(self,driver):
    #--add check setion
        for product in self.productsLinks:
            if product not in self.localProducts:
                print("product add: ",product)
                self.scrape_products(driver=driver,url=product)
                
            elif product in self.localProducts:
                pass
                # print("product exits: ",product)
            else:
                print("no new product add")
        
    #--remove check section
        rawList = []
        with open(self.resultFile, 'r', encoding='latin-1') as csv_f:
            reader = csv.DictReader(csv_f, delimiter=',')
            for prod in reader:
                rawList.append(prod)

        for item in rawList:
            if item["Product_URL"] not in self.productsLinks:
                item["status"] = "Removed"
                item["date"] = datetime.datetime(2023, 7, 19, 10, 30, 0).strftime("%d-%m-%y")
                self.removedProducts.append(item)
                rawList.remove(item)
                print("product removed: ",item["Product_URL"])
                
            elif item["Product_URL"] in self.productsLinks:
                pass
            else:
                print("no product remove")
        fieldnames = rawList[0].keys()
        with open(self.resultFile, mode='w', newline='',encoding="latin-1") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rawList)
                
    
    def browse(self,url):
        options = Options()
        options.headless = False
        options.add_argument("--log-level=3")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
        driver.implicitly_wait(1)
        driver.maximize_window()
        driver.get(url)
        
        time.sleep(1)
    #---For scrapping data from web page
        response = driver.page_source
        soup = BeautifulSoup(response,"html.parser")
        
        if '<i class="icon-remove close"></i>' in response:
            Click = driver.find_element(by=By.XPATH,value='//*[@id="popup_message"]/a[1]')
            Click.click()
        time.sleep(1)
        total_units = int(soup.find('span',class_="total-units").text)
        self.total = total_units
        print("total units: ",total_units)
        
        curentUnits = len(soup.find_all('li',class_="unit"))
        while curentUnits != total_units:
            scroll = driver.find_element(by=By.TAG_NAME,value='html')
            scroll.send_keys(Keys.DOWN)
            scroll.send_keys(Keys.DOWN)              
            scroll.send_keys(Keys.DOWN)
            scroll.send_keys(Keys.DOWN)
            soup = BeautifulSoup(driver.page_source,"html.parser")
            curentUnits = len(soup.find_all('li',class_="unit"))
            # print(curentUnits)
        
        self.scrape_page(driver)
        self.check_update(driver)
        
        
        
        
        # self.scrape_products(driver=driver,url="https://www.sanantoniorvs.com/product/used-2015-crossroads-rv-rushmore-washington-rf39wa-2139869-5")
        
        
        self.flag = False
        time.sleep(2)
        print("all get")
        driver.quit()

       


if __name__ == "__main__":
    am = Scrapper(product="fifth-wheel")
    page = am.browse("https://www.sanantoniorvs.com/product/fifth-wheel"+"?pagesize=5000")
    

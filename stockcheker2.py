import bs4 
import pandas as pd
import numpy as np
import datetime
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
from datetime import datetime
import asyncio


class Scraper: 

    def __init__(self):
        self.soup = []
        self.df = []
        options = Options()
        options.headless = True
        self.driver = webdriver.Firefox(options=options, executable_path='bin/geckodriver')
        self.data = []


    def load_all_page_content(self):

        #self.driver.get(url)
        
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        #time.sleep(3)
        while True:
            print(f'scrolling to height {last_height}...')
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(1)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                print('Done loading page content...')
                break
            last_height = new_height
        #

    

    def scrape_page(self, url):
        print('================================ Starting scraping process ================================')
        time_now = datetime.now()
        time_now_str = time_now.strftime("%H:%M:%S %d/%m/%Y")
        
        self.driver.get(url)
        print(f'URL: {self.driver.current_url}')

        result = []
        self.load_all_page_content()

        page = self.driver.page_source
        soup = bs4.BeautifulSoup(page, 'lxml')

        res = soup.find_all('div', class_ = 'css-tjjb18')

        for x in res:
            result.append(x)

        for pack in result:

            items = pack.find_all('div', class_ = 'css-1sn1xa2')
            for item in items:
                try:
                    details = item.find('div', class_='css-7fmtuv')
                    try:
                        stock = item.find('div', class_='css-evfrvc').text
                    except:
                        stock = 'READY'
                    
                    name = details.find('div', class_='css-18c4yhp').text
                    price = details.find('div', class_='css-rhd610').text
                    #print(details.find_all('span', class_='css-4pwgpi'))
                    #lokasi = details.find_all('span', class_='css-4pwgpi')[0].text
                    #toko = details.find_all('span', class_='css-4pwgpi')[1].text

                    link = details.find_all('a', class_='pcv3__info-content css-1qnnuob', href=True)[0]['href']

                    #print(f'{stock}|| {price} || {name} || {link} || {time_now_str}')
                    
                    self.data.append([stock, price, name, link, time_now_str])
                    #
                    
                except Exception as e:
                    print(e)
                #
            #

        self.df = pd.DataFrame(self.data, columns=['Stock', 'Price', 'Name', 'Link', 'Last Update'])
        #print(self.df.head(len(self.data)))
        self.driver.quit()
        print('================================ scraping complete =============================================')
        #
    
    def save_to_csv(self, filename):
        self.df.to_csv(filename)
        #


def load_data(filename):
    df = pd.read_csv('data.csv', index_col=0)
    return df



if __name__ == '__main__':

    url1 = f'https://www.tokopedia.com/nvidiageforce/etalase/geforce-gtx-16-series'
    
    # while True:
    try:
        scraper1 = Scraper()
        scraper1.scrape_page(url1)
        scraper1.df.to_csv('data.csv')
        
    except Exception as e:
        print(e) 

    # df = pd.read_csv('data.csv', index_col=0)
    
    # df_stock = df[df['Stock'].str.contains('Stok Habis') == False]
    
    # if df_stock.empty == False:
    #     msg = 'Ada Stock'
    #     for item in df_stock.iterrows():
    #         print(item)

    #     print(msg)
    # else:
    #     msg = 'Stock Habis Semua'
    #     print(msg)
    
        
    



    
    



    

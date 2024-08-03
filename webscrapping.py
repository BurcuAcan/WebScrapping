import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium import webdriver
import random
import firebase_admin
from firebase_admin import credentials,firestore
import time
import re


def getGetirRestaurant():
    url = "https://getir.com/yemek/restoranlar/"
    chrome_options = webdriver.ChromeOptions()

    prefs = {
        "profile.default_content_setting_values.geolocation": 2 # Lokasyon izni kapatıldı
    }
    chrome_options.add_experimental_option("prefs", prefs)

    dr = webdriver.Chrome(options=chrome_options) # Opsiyon ile birlikte driver set edildi.
    dr.get(url) #Tarayıcı çalıştırıldı.

    time.sleep(5) # Verilerin gelmesini beklemek için 5 sn delay çalışır

    element = dr.find_element(By.XPATH, '//*[@id="__next"]/div[3]/main/section/div/section[1]/div/div[1]') #XPATH kullanılarak butonlara ve inputlara tıklanılıp veri aktarılmasını sağladık.
    element.click() #tıklama yapar

    time.sleep(5)

    element = dr.find_element(By.XPATH, '//*[@id="map-control-2"]/div/article/div/div/div[2]/div/div/input')
    element.send_keys('Pınarbaşı, Akdeniz Üniversitesi 07070 Antalya Konyaaltı') # element içerisine yazı yazmamızı sağlar.

    time.sleep(5)

    element = dr.find_element(By.XPATH, '//*[@id="react-autowhatever-1--item-0"]/div/button/div')
    element.click()

    time.sleep(5)

    element = dr.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/div[2]/div[2]/div[2]/button')
    element.click()

    time.sleep(5)

    element = dr.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/div[2]/div[2]/div/form/div[7]/button')
    element.click()

    time.sleep(3)

    element = dr.find_element(By.XPATH, '/html/body/div[4]/div[2]/div/div/div[3]/div/div[2]/button')
    element.click()

    time.sleep(3)

    time.sleep(10)

    soup = BeautifulSoup(dr.page_source, 'html.parser') # Web scrapping yapabiliyoruz.

    skeleton = soup.find('section', class_= 'sc-a58b4dc-2') # restoran listesininin temel elementi
    restaurantName = skeleton.find_all('p', class_= 'style__ParagraphText-sc-__sc-1nwjacj-9') # skeleton içerisindeki tüm restoran isimlerini almamızı sağlıyor.
    deliveryTime = skeleton.find_all('time', class_='sc-9cff985f-2')
    minimumAmount = skeleton.find_all('span',  class_='style__Text-sc-__sc-1nwjacj-0 iwTTHJ sc-9cff985f-4 esvgxl')
    rating = skeleton.find_all('span', class_='style__Text-sc-__sc-1nwjacj-0 iwTTHJ')

    print("Website: getir.com/yemek")
    i = 0
    for name in restaurantName:
        print('Restaurant Name: ', name.text.strip())
        print('Delivery Time: ', deliveryTime[i].text.strip())
        print('Minimum Amount: ', minimumAmount[i].text.strip())
        print('Rating: ', rating[i].text.strip())
        print()
        i = i + 1

def getYemeksepetiRestaurant():
    url = "https://www.yemeksepeti.com/city/antalya?lng=30.65198&lat=36.8944"
    chrome_options = webdriver.ChromeOptions()

    prefs = {
        "profile.default_content_setting_values.geolocation": 2
    }
    chrome_options.add_experimental_option("prefs", prefs)

    dr = webdriver.Safari()
    dr.get(url)

    time.sleep(5)

    soup = BeautifulSoup(dr.page_source, 'html.parser')
    skeleton = soup.find('div', class_= 'bds-c-skeleton-loader-container__actual-content')
    restaurantName = skeleton.find_all('div', class_= 'vendor-name')
    rating = skeleton.find_all('span', class_= 'bds-c-rating__label-primary')
    deliveryTime = skeleton.find_all('div', class_='sanitized-row-text', content=lambda x: x and 'minimum' in x)
    filteredDeliveryTimes = [dt for dt in deliveryTime if dt.get('content') and 'minimum' in dt['content']]
    filteredAmount = [dt for dt in deliveryTime if dt.get('content') and 'min' in dt['content'] and 'minimum' not in dt['content']]
    img_tags = skeleton.find_all('img', class_='vendor-tile-revamped-image')
    li_tag = skeleton.find_all('li', class_ = 'vendor-tile-new-l')
    i = 0
    j = 0
    for name in restaurantName:
        print('Restaurant Name: ', name.text.strip())
        print('Rating: ', rating[i].text.strip())
        print("Minimum Amount: ", filteredDeliveryTimes[i].text.strip())
        a_tag = li_tag[i].find('a', href=True)
        href = a_tag['href']
        print("Website: ", href)
        i = i + 1

def getMigrosRestaurant():
    
    url = "https://www.migros.com.tr/yemek"
    chrome_options = webdriver.ChromeOptions()

    prefs = {
        "profile.default_content_setting_values.geolocation": 2
    }
    chrome_options.add_experimental_option("prefs", prefs)

    dr = webdriver.Chrome(options=chrome_options)
    dr.get(url)

    time.sleep(5)

    element = dr.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/mat-dialog-container/div/div/fe-delivery-options-modal/mat-dialog-content/div/fe-delivery-location-map-modal/div/fe-location-selection-map/form/input')
    element.click()

    time.sleep(5)
    
    element.send_keys('Pınarbaşı, Akdeniz Üniversitesi 07070 Antalya Konyaaltı')

    time.sleep(5)

    element = dr.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/mat-dialog-container/div/div/fe-delivery-options-modal/mat-dialog-content/div/fe-delivery-location-map-modal/div/fe-location-selection-map/form/div/li[1]/span')
    element.click()

    time.sleep(5)

    element = dr.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/mat-dialog-container/div/div/fe-delivery-options-modal/mat-dialog-content/div/fe-delivery-location-map-modal/div/button/span[2]')
    element.click()

    time.sleep(5)

    element = dr.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/mat-dialog-container/div/div/fe-delivery-options-modal/mat-dialog-content/div/fe-delivery-location-map-modal/div/div[3]/button[1]')
    element.click()

    time.sleep(5)

    element = dr.find_element(By.XPATH, '/html/body/sm-root/div/main/sm-product')
    element.click()

    time.sleep(5)

    element = dr.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/mat-dialog-container/div/div/sm-anonymous-login-dialog/div[2]/button[3]/span[2]')
    element.click()
    time.sleep(5)

    soup = BeautifulSoup(dr.page_source, 'html.parser') # web scrapping için gerekli
    skeleton = soup.find('div', class_= 'restaurant-items')

    infoSkeleton = skeleton.find_all('div', class_ = 'restaurant-card')

    print("Website: migros.com.tr/yemek")
    i = 0
    for skeleton in infoSkeleton:
        restaurantName = skeleton.find('span', class_= 'name')
        deliveryTime = skeleton.find('span', class_='duration')
        minimumAmount = skeleton.find('span', string=lambda text: text and "Min." in text) # birden fazla aynı isimde class ismi olduğu için karışmaması adına text içerisinde "Min." yazısı olanı aradım
        rating = skeleton.find('span', class_=lambda c: c and 'rate' in c.split()) # birden fazla aynı isimde class ismi olduğu için karışmaması adına text içerisinde "Min." yazısı olanı aradım
        image = skeleton.find('img', class_='single-restaurant-card-cover')
        a_tag = soup.find('a', {'class': 'single-restaurant-card'})
        href_value = a_tag.get('href')
        print('Restaurant Name: ', restaurantName.text.strip())
        print('Delivery Time: ', deliveryTime.text.strip())
        print('Minimum Amount: ', minimumAmount.text.strip())
        print('Rating: ', rating.text.strip())
        print('Image: ', image.get('src'))
        print('Endpoint: ', href_value)
        print()

        toFirebase(remove_after_comma(restaurantName), extract_first_numeric_value(deliveryTime), extract_numeric_value(minimumAmount),extract_numeric_value(rating) ,url,href_value, image)
        i = i + 1

def extract_first_numeric_value(text):
    match = re.search(r'\d+', text)
    if match:
        numeric_value = match.group()
        return int(numeric_value)
    return None

def extract_numeric_value(text):
    match = re.search(r'\d+,\d+|\d+', text)
    if match:
        numeric_value = match.group().replace(',', '.')
        return float(numeric_value)
    return None

def remove_after_comma(input_string):
    if ',' in input_string:
        result = input_string.split(',')[0]
        return result
    return input_string

def toFirebase(name, deliveryTime, minimumAmount, rating, website, endpoint,image=None):
    cred = credentials.Certificate('sertifika.json')
    firebase_admin.initialize_app(cred)
    collection_ref = db.collection('Restaurant')


    query = collection_ref.where('name', '==', name)
    docs = query.stream()

    if docs:
        for doc in docs:
            _deliveryTime = collection_ref.get('deliveryTime')
            _minAmount = collection_ref.get('minAmount')
            _score = collection_ref.get('score')
            data = {
                "deliveryTime": (deliveryTime+_deliveryTime)/2,
                "image": image,
                "minAmount": (minimumAmount+_minAmount)/2,
                "score": (rating+_score)/2
            }

            innerData = {
                "deliveryTime": deliveryTime,
                "endpoint": endpoint,
                "minAmount": minimumAmount,
                "name": name,
                "score": rating
            }
            collection_ref.set(data)
            websites_ref = doc.collection('websites')
            websites_ref.set(innerData)
    else:
        data = {
            "deliveryTime": deliveryTime,
            "image": image,
            "minAmount": minimumAmount,
            "score": rating
        }

        innerData = {
            "deliveryTime": deliveryTime,
            "endpoint": endpoint,
            "minAmount": minimumAmount,
            "name": name,
            "score": rating
        }
        collection_ref.add(data)
        websites_ref = doc.collection('websites')
        websites_ref.add(innerData)

#getYemeksepetiRestaurant()
getMigrosRestaurant()
#getGetirRestaurant()
import requests
from bs4 import BeautifulSoup
import csv
import requests



url = "http://books.toscrape.com/catalogue/the-girl-in-the-ice-dci-erika-foster-1_65/index.html"


def FindPageData(page_url):
    page = requests.get(page_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    infotb = soup.find_all('td')
    info = []

    for infos in infotb:
        info.append(infos.string)

    upc = info[0]
    title = soup.find('h1').string
    price_including_tax = info[2]
    price_excluding_tax = info[3]
    number_available = info[5]
    product_description = soup.find('div', id='product_description').next_element.next_element.next_element.next_element.next_element.next_element.string
    category = soup.find('li', class_='active').previous_element.previous_element.previous_element
    review_rating = 0
    img_tag = soup.find('img')
    image_url = img_tag['src']

    en_tete = ['url', 'upc', 'title', 'price_including_tax', ' price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'img_url']

    with open('data.csv', 'w', encoding='utf-8') as csv_files:
        writer = csv.writer(csv_files, delimiter=',')
        writer.writerow(en_tete)
        writer.writerow([url, upc, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url])
    



FindPageData(url)
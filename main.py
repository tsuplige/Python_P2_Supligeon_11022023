import requests
from bs4 import BeautifulSoup
import csv
import requests



Burl = "http://books.toscrape.com/catalogue/the-girl-in-the-ice-dci-erika-foster-1_65/index.html"
Purl = 'http://books.toscrape.com/catalogue/category/books/travel_2/index.html'



def FindBookUrl(page_url):
    links = []
    page = requests.get(page_url)
    soup = BeautifulSoup(page.content, 'html.parser')

    artc = soup.find_all('h3')

    for h3 in artc:
            a = h3.find('a')
            li = a.get('href')
            lin = li.replace('../../..', 'http://books.toscrape.com/catalogue')
            links.append(lin)
    en_tete = ['liens']
    with open('link_data.csv', 'w', encoding='utf-8') as csv_files:
        writer = csv.writer(csv_files, delimiter=',')
        writer.writerow(en_tete)
        for link in links:
            writer.writerow([link])











def LinkCatToBook():
    with open('link_data.csv') as fichier_csv:
        reader = csv.reader(fichier_csv, delimiter=',')
        for ligne in reader:
            print(ligne)












def FindBookData(page_url):
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
    Iurl = img_tag['src']
    image_url = Iurl.replace('../..', 'http://books.toscrape.com/')

    en_tete = ['url', 'upc', 'title', 'price_including_tax', ' price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'img_url']

    with open('Book_data.csv', 'w', encoding='utf-8') as csv_files:
        writer = csv.writer(csv_files, delimiter=',')
        writer.writerow(en_tete)
        writer.writerow([page_url, upc, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url])
    


FindBookUrl(Purl)
# FindBookData(Burl)
LinkCatToBook()

# FindBookData('http://books.toscrape.com/catalogue/full-moon-over-noahs-ark-an-odyssey-to-mount-ararat-and-beyond_811/index.html')
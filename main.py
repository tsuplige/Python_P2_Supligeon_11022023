import requests
from bs4 import BeautifulSoup
import csv
import requests

en_tete_link_data = ['liens']
with open('link_data.csv', 'a', encoding='utf-8') as csv_files:
        writer = csv.writer(csv_files, delimiter=',')
        writer.writerow(en_tete_link_data)

en_tete_book_data = ['url', 'upc', 'title', 'price_including_tax', ' price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'img_url']

with open('Book_data.csv', 'a', encoding='utf-8') as csv_files:
        writer = csv.writer(csv_files, delimiter=',')
        writer.writerow(en_tete_book_data)

Burl = "http://books.toscrape.com/catalogue/the-girl-in-the-ice-dci-erika-foster-1_65/index.html"
Purl = 'http://books.toscrape.com/catalogue/category/books/mystery_3/index.html'



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
    with open('link_data.csv', 'a', encoding='utf-8') as csv_files:
        writer = csv.writer(csv_files, delimiter=',')
        for link in links:
            writer.writerow([link])
    url_parts = page_url.rsplit('/', 1)
    next = soup.find('li', class_='next')
    if next:
        a_tag = next.find('a')
        href = a_tag['href']
        new_link = url_parts[0] + '/' + href
        # FindBookData()
        FindBookUrl(new_link)
    else:
        print("Tag li avec classe 'next' non trouvé.")


def LinkCatToBook(page_url):
    FindBookUrl(page_url)
    with open('link_data.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row:
                for link in row:
                    if 'http' in link:
                        print(link)
                        FindBookData(link)



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

    div = soup.find('p', class_='star-rating')
    review_rating = div['class'][1]
    img_tag = soup.find('img')
    Iurl = img_tag['src']
    image_url = Iurl.replace('../..', 'http://books.toscrape.com/')

    with open('Book_data.csv', 'a', encoding='utf-8') as csv_files:
        writer = csv.writer(csv_files, delimiter=',')
        writer.writerow([page_url, upc, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url])
    


# FindBookUrl(Purl)
# FindBookData(Burl)
LinkCatToBook('http://books.toscrape.com/catalogue/category/books/mystery_3/index.html')

# FindBookData('http://books.toscrape.com/catalogue/full-moon-over-noahs-ark-an-odyssey-to-mount-ararat-and-beyond_811/index.html')
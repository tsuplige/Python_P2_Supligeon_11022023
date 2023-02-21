import requests
from bs4 import BeautifulSoup
import csv
import os



# Verifie si les repertoires data et data/img exist et si non les cree
if os.path.exists("data") and os.path.isdir("data"):
    print("Le dossier 'data' existe.")
    if os.path.exists("data/img") and os.path.isdir("data"):
        print("Le dossier 'data/img' existe deja.")
    else:
        os.makedirs('data/img')
else:
    print("Le dossier 'data' n'existe pas.")
    os.makedirs('data')
    os.makedirs('data/img')

if os.path.exists('data/Book_data.csv'):
    os.remove('data/Book_data.csv')
    print(f"Le fichier {'data/Book_data.csv'} a été supprimé.")


# cree le fichier CSV Book_data avec sont en tete
en_tete_book_data = ['url', 'upc', 'title', 'price_including_tax', ' price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'img_url']

with open('data/Book_data.csv', 'a', encoding='utf-8') as csv_files:
        writer = csv.writer(csv_files, delimiter=',')
        writer.writerow(en_tete_book_data)

Burl = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
# Purl = 'http://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html'

# liste qui contiemdra les liens des fiche livre
Book_links = []
cat_link = []
def FindCategoryUrl(site_url):
    page = requests.get(site_url)
    soup = BeautifulSoup(page.content, 'html.parser')

    list = soup.find('ul', class_='nav nav-list')
    a = list.find_all('a')
    for link in a:
        cat_link.append(site_url + link.get('href'))
    
    # print(cat_link)

def FindBookUrl(page_url):
    page = requests.get(page_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    artc = soup.find_all('h3')

    for h3 in artc:
            a = h3.find('a')
            li = a.get('href')
            lin = li.replace('../../..', 'http://books.toscrape.com/catalogue')
            Book_links.append(lin)
    url_parts = page_url.rsplit('/', 1)
    next = soup.find('li', class_='next')
    # print(next)
    # print(Book_links, "\n\n_____________________________\n\n")
    if next:
        a_tag = next.find('a')
        href = a_tag['href']
        new_link = url_parts[0] + '/' + href
        FindBookUrl(new_link)

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
    
    p = soup.find_all('p')
    product_description = p[3].string
    category = soup.find('li', class_='active').previous_element.previous_element.previous_element

    div = soup.find('p', class_='star-rating')
    review_rating = div['class'][1]
    img_tag = soup.find('img')
    Iurl = img_tag['src']
    image_url = Iurl.replace('../..', 'http://books.toscrape.com/')

    DowmloadImg(image_url,upc)

    with open('data/Book_data.csv', 'a', encoding='utf-8') as csv_files:
        writer = csv.writer(csv_files, delimiter=',')
        writer.writerow([page_url, upc, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url])
    
def LinkCatToBook():
    NumOfBookDll = 0
    FindCategoryUrl('http://books.toscrape.com/')
    for link in cat_link:
        FindBookUrl(link)
    #     NumOfBook += 1

    # print(Book_links)

    for link in Book_links:
         if 'http' in link:
            FindBookData(link)
            NumOfBookDll += 1
            os.system('cls')
            print('________________', NumOfBookDll, ' livres telecharge. ',2000 - NumOfBookDll,'restant a Dll','_________________')
            

         
    # with open('data/link_data.csv', newline='') as csvfile:
    #     reader = csv.reader(csvfile)
    #     for row in reader:
    #         if row:
    #             for link in row:
    #                 if 'http' in link:
    #                     print(link)
    #                     FindBookData(link)

def DowmloadImg(url,upc) :
    reponse = requests.get(url)
    with open('data/img/'+ upc+'.jpg', 'wb') as img:
        img.write(reponse.content)

# FindBookUrl(Purl)
# FindBookData(Burl)
# LinkCatToBook(Purl)

LinkCatToBook()

# FindBookData('http://books.toscrape.com/catalogue/full-moon-over-noahs-ark-an-odyssey-to-mount-ararat-and-beyond_811/index.html')
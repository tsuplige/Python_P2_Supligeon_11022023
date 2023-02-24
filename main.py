import requests
from bs4 import BeautifulSoup
import csv
import os
import shutil
from tqdm import tqdm




# Verifie si les repertoires data,data/img et le fichier Book_data.csv existes,les supprimmes pour en cree des vide afin d'eviter les doublons et si non les cree
if os.path.exists("data") and os.path.isdir("data"):
    print("Le dossier 'data' existe.")
    if os.path.exists("data/img") and os.path.isdir("data"):
        shutil.rmtree('data/img')
        os.makedirs('data/img')
    else:
        os.makedirs('data/img')
    if os.path.exists("data/csv_files") and os.path.isdir("data"):
        shutil.rmtree('data/csv_files')
        os.makedirs('data/csv_files')
    else:
        os.makedirs('data/csv_files')
else:
    print("Le dossier 'data' n'existe pas.")
    os.makedirs('data')
    os.makedirs('data/img')
    os.makedirs('data/csv_files')

if os.path.exists('data/Book_data.csv'):
    os.remove('data/Book_data.csv')
    print(f"Le fichier {'data/Book_data.csv'} a été supprimé.")


# cree le fichier CSV Book_data avec sont en tete
en_tete_book_data = ['url', 'upc', 'title', 'price_including_tax', ' price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'img_url']

# Fonction Prenant en parametre le Lien[STRING] du site et qui cherche toute les category et leurs liens et lance la fontcion LinkCatToBook()
def FindCategoryUrl(site_url):
    page = requests.get(site_url)
    soup = BeautifulSoup(page.content, 'html.parser')

    list = soup.find('ul', class_='nav nav-list')
    a = list.find_all('a')
    a.pop(0)
    print('\n________________________________________________ '+"recuperation des liens des categories"+' ________________________________________________\n')
    for link in a:
        lien = site_url + link.get('href')
        Cat_name = link.string.replace("    ","").replace(" ","").replace("\n","")
        print(Cat_name)
        LinkCatToBook(lien, Cat_name)
    print('\n\n________________________________________________ '+"telchargement termine"+' ________________________________________________\n')

# Fonction Recursive Prenant en parametre le Lien[STRING] d'une categorie et qui cherche toute les livre de la page et si il trouve un bouton next 
def FindBookUrl(Cat_url):
    page = requests.get(Cat_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    artc = soup.find_all('h3')
    print("recuperation des urls des livres : " )
    # Cat_Title = soup.find('h1').string
    Book_links = []


    # with open('data/csv_files/'+Cat_Title+'.csv', 'a', encoding='utf-8') as csv_files:
    #     writer = csv.writer(csv_files, delimiter=',')
    #     writer.writerow(en_tete_book_data)
    
    for h3 in tqdm(artc):
            a = h3.find('a')
            li = a.get('href')
            lin = li.replace('../../..', 'http://books.toscrape.com/catalogue')
            Book_links.append(lin)
    url_parts = Cat_url.rsplit('/', 1)
    next = soup.find('li', class_='next')
    if next:
        a_tag = next.find('a')
        href = a_tag['href']
        new_link = url_parts[0] + '/' + href
        New_Book_links = FindBookUrl(new_link)
        for link in New_Book_links:
            Book_links.append(link)
        # Book_links.append(FindBookUrl(new_link))
    return Book_links

# Fonction Prenant en parametre Un Lien[STRING] d'une page Produit et qui cherche les donnee pour les ecrire dans un fichier .csv
def FindBookData(page_url, Cfiles):
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

    with open(Cfiles, 'a', encoding='utf-8') as csv_files:
        writer = csv.writer(csv_files, delimiter=',')
        writer.writerow([page_url, upc, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url])
    
# Fonction appellant FindBookUrl() Pour collecter les donnee des livre trouver avec FindBookData()
def LinkCatToBook(Clink, CName):
    files_name = 'data/csv_files/'+CName+'_data.csv'
    with open(files_name, 'a', encoding='utf-8') as csv_files:
        writer = csv.writer(csv_files, delimiter=',')
        writer.writerow(en_tete_book_data)
    Book_links = FindBookUrl(Clink)
    print('\n\n________________________________________________ '+"telechargement des donnee de la category :" + CName + '  ________________________________________________\n')
    
    for link in tqdm(Book_links):
         if 'http' in link:
            FindBookData(link, files_name)
    

# Fonction permettant de Telecharger les Images des livre en prenant en parametre le liens de l'image[STRING] et son code upc[STRING] pour le nommee
def DowmloadImg(url,upc) :
    reponse = requests.get(url)
    with open('data/img/'+ upc+'.jpg', 'wb') as img:
        img.write(reponse.content)

FindCategoryUrl('http://books.toscrape.com/')
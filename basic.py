from bs4 import BeautifulSoup as bs
from urllib.request import urlopen

url = 'https://alura-site-scraping.herokuapp.com/'

response = urlopen(url)
html = response.read()

#criando um objeto BeautifulSoup
soup = bs(html, 'html.parser')

print(soup.find('h1', {'class': 'sub-header'}).get_text())

#print(soup.img.attrs)
print(soup.img['class'])
#print(soup.img.get('src'))


#print(soup.findAll('p', text = "Belo Horizonte - MG"))

#for item in soup.findAll('img', alt="Foto"):
    #print(item.get('src'))
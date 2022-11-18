from urllib.request import urlopen

from bs4 import BeautifulSoup as bs
from urllib.request import urlopen

def treatment(input):
    return " ".join(input.split()).replace('> <', '><')


url = 'https://alura-site-scraping.herokuapp.com/index.php'

response = urlopen(url)
html = response.read().decode('utf-8')

html = treatment(html)

print(html)
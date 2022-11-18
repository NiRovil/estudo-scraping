from bs4 import BeautifulSoup as bs
from urllib.request import urlopen

url = 'https://alura-site-scraping.herokuapp.com/hello-world.php'

response = urlopen(url)
html = response.read()
soup = bs(html, 'html.parser')

print(soup.find('h1', {'class': 'sub-header'}).get_text())
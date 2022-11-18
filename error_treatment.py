from bs4 import BeautifulSoup as bs
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError

url = 'https://twitter.com/home'

headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:106.0) Gecko/20100101 Firefox/106.0'}

try:
    req = Request(url, headers=headers)
    response = urlopen(req)
    html = response.read()
    soup = bs(html, 'html.parser')

    print(soup)

except HTTPError as e:
    print(e.status, e.reason)

except URLError as e:
    print(e.reason)

#print(soup.find('h1', {'class': 'sub-header'}).get_text())
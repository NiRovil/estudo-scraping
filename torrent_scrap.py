from bs4 import BeautifulSoup as bs
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

header = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:106.0) Gecko/20100101 Firefox/106.0'}

def url_search(term):
    url = f'https://www.rarbggo.to/search/?search={term}&order=seeders&by=DESC'
    return url

def url_download(donwload_url):
    url = f'https://www.rarbggo.to{donwload_url}'
    return url

def treatment(html):
    return " ".join(html.split()).replace('> <', '><')

def connection(url, headers):
    try:
        req = Request(url, headers=headers)
        response = urlopen(req)
        html = response.read().decode('utf-8')
        html = treatment(html)
        soup = bs(html, 'html.parser')

    except HTTPError as e:
        print(e.status, e.reason)

    except URLError as e:
        print(e.reason)

    return soup


term = input('Digite um termo para pesquisa: ')
term = term.replace(' ', '%20')

search_url = url_search(term)
soup = connection(search_url, header)

download_url = soup.find('td', {'class': 'tlista'})
download_url = download_url.find('a').attrs['href']

print(download_url)


#for item in soup.findAll('a'):
#    if item.find_parent('td', class_='tlista'):
#        list_results.append(item)
#    else:
#        continue

#soup = soup.find('td', class_='tlista', align='left').findNextSiblings('a')

#print(soup)
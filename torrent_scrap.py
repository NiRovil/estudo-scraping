from bs4 import BeautifulSoup as bs
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

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

def order(soup):

    results = []
    try:
        content = soup.find('tr', {'class': 'table2ta'}).findAll('td', {'class': 'tlista'})
        contents = soup.findAll('tr', {'class': 'table2ta'})
        counter = 0

        for item in contents:

            result = {}

            content = item.findAll('td', {'class': 'tlista'})
            result['name'] = content[1].find('a').attrs['title']
            result['url'] = content[1].find('a').attrs['href']
            result['type'] = content[2].findAll('a')[0].get_text() + content[2].findAll('a')[1].get_text()
            result['space'] = content[4].get_text()
            result['seeds'] = content[5].get_text()
            result['release'] = content[7].get_text()

            results.append({counter: result})
    
            counter += 1

        return result
    
    except Exception as e:
        print('Termo não encontrado')
        another_term = input('Digite outro termo: ').replace(' ', '%20')
        return another_term

def download_page(best_links):
    print('ok')

HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:106.0) Gecko/20100101 Firefox/106.0'}

term = input('Digite um termo para pesquisa: ').replace(' ', '%20')
search_url = url_search(term)
soup = connection(search_url, HEADERS)
ordering = order(soup)


# well, it is for a test, don't judge me
if ordering is dict:
    magnet = download_page(ordering)
else:
    term = ordering
    search_url = url_search(term)
    soup = connection(search_url, HEADERS)
    ordering = order(soup)
    magnet = download_page(ordering)
import sys, subprocess

from bs4 import BeautifulSoup as bs
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

def url_search(term: str):
    url = f'https://www.rarbggo.to/search/?search={term}&order=seeders&by=DESC'
    return url

def url_download(donwload_url: str):
    url = f'https://www.rarbggo.to{donwload_url}'
    return url

def treatment(html: str):
    return " ".join(html.split()).replace('> <', '><')

def connection(url: str, headers: dict = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:106.0) Gecko/20100101 Firefox/106.0'}):
    try:
        req = Request(url, headers=headers)
        response = urlopen(req)
        html = response.read().decode('utf-8')
        html = treatment(html)
        soup = bs(html, 'html.parser')
        return soup

    except HTTPError as e:
        print(e.status, e.reason)

    except URLError as e:
        print(e.reason)

def order(soup: bs):

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

        return results
    
    except Exception as e:
        print('Termo não encontrado')
        another_term = input('Digite outro termo: ').replace(' ', '%20')
        return another_term

def select_download(links: list):

    print('Selecione o link que mais agrada!')
    count = 0
    download = []

    for item in links:
        layout(count+1, item[count]['name'], item[count]['type'], item[count]['space'], item[count]['seeds'], item[count]['release'])
        download.append([count+1, item[count]['name'], item[count]['type'], item[count]['space'], item[count]['seeds'], item[count]['release'], item[count]['url']])
        count += 1

    while True:
        selection = input('Selecione um ID: ')

        if selection.isnumeric():
            break
        
        else:
            print('Digite somente números!')
            continue
    
    return [item for item in download[int(selection)-1]]

def layout(id, name, type, space, seeds, release):
    return print(f'ID: {id} / Nome: {name} / Tipo: {type} / Tamanho: {space} / Seeds: {seeds} / Release: {release}')

def url_download(selected: list):
        
    url = f'https://www.rarbggo.to{selected[6]}'
    soup = connection(url=url)
    magnet = soup.select_one('a[href*=magnet]').get('href')
    
    if sys.platform.startswith('linux'):
        subprocess.Popen(['xdg-open', magnet], stdout=subprocess.PIPE, stderr=subprocess.PIPE)


term = input('Digite um termo para pesquisa: ').replace(' ', '%20')
search_url = url_search(term)
soup = connection(search_url)
ordering = order(soup)
selection = select_download(ordering)
magnet = url_download(selection)


# well, it is for a test, don't judge me
#if ordering is dict:
#    magnet = download_page(ordering)
#else:
#    term = ordering
#    search_url = url_search(term)
#    soup = connection(search_url, HEADERS)
#    ordering = order(soup)
#    magnet = download_page(ordering)
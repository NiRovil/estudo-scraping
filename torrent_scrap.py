from bs4 import BeautifulSoup as bs
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

class ScrapSearch():

    def __init__(self, term: str):
        self._term = term.replace(' ', '%20')
        return self.url_search()

    def url_search(self):
        url = f'https://www.rarbggo.to/search/?search={self._term}&order=seeders&by=DESC'
        return self.order(self.connection(url))

    def treatment(self, html: str):
        return " ".join(html.split()).replace('> <', '><')

    def connection(self, url: str):
        
        try:
            header = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:106.0) Gecko/20100101 Firefox/106.0'}
            req = Request(url, headers=header)
            response = urlopen(req)
            html = response.read().decode('utf-8')
            html = self.treatment(html)
            soup = bs(html, 'html.parser')
            return soup

        except HTTPError as e:
            print(e.status, e.reason)

        except URLError as e:
            print(e.reason)

    def order(self, soup: bs):

        results = []
        
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
            
            if counter == 5:
                break

        self.select_download(results)

    def select_download(self, links: list):

        index = 0
        self.filter = []

        for item in links:
            self.filter.append([index+1, item[index]['name'], item[index]['type'], item[index]['space'], item[index]['seeds'], item[index]['release'], item[index]['url']])
            index += 1

    def __call__(self):

        return self.filter

class ScrapDownload(ScrapSearch):

    def __init__(self, link):
        self._link = link
        self.url_download()

    def url_download(self):
            
        URL = f'https://www.rarbggo.to{self._link}'
        soup = self.connection(URL)
        self.magnet = soup.select_one('a[href*=magnet]').get('href')

    def __str__(self):
        return self.magnet
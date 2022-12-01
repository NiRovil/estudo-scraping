from bs4 import BeautifulSoup as bs
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

class ScrapSearch():

    """
        Process of scraping some torrents for the bot.

        If you want to use this alone, feel free to do it.
    """
    def __init__(self, term: str):
        self._term = term.replace(' ', '%20')
        self.url_search()

    def url_search(self):
        url = f'https://www.rarbggo.to/search/?search={self._term}&order=seeders&by=DESC'
        self.find_torrent(self.connection(url))

    @staticmethod
    def html_treatment(html: str):
        return " ".join(html.split()).replace('> <', '><')

    def connection(self, url: str):
        
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:106.0) Gecko/20100101 Firefox/106.0'}
            request = Request(url, headers=headers)
            response = urlopen(request)
            html = response.read().decode('utf-8')
            html = self.html_treatment(html)
            soup = bs(html, 'html.parser')
            return soup

        except HTTPError as e:
            print(e.status, e.reason)

        except URLError as e:
            print(e.reason)

    def find_torrent(self, soup: bs):

        torrents = []
        
        contents = soup.findAll('tr', {'class': 'table2ta'})
        counter = 0
        
        # Filtering the best results by query.
        for content in contents:

            torrent = {}

            content = content.findAll('td', {'class': 'tlista'})
            torrent['name'] = content[1].find('a').attrs['title']
            torrent['url'] = content[1].find('a').attrs['href']
            torrent['type'] = content[2].findAll('a')[0].get_text() + content[2].findAll('a')[1].get_text()
            torrent['space'] = content[4].get_text()
            torrent['seeds'] = content[5].get_text()
            torrent['release'] = content[7].get_text()
            torrents.append({counter: torrent})
            counter += 1

            if counter == 5:
                break

        self.torrent_filter(torrents)
    
    def torrent_filter(self, torrents: list):

        index = 0
        self._torrents = []

        for torrent in torrents:
            self._torrents.append([index+1, torrent[index]['name'], torrent[index]['type'], torrent[index]['space'], torrent[index]['seeds'], torrent[index]['release'], torrent[index]['url']])
            index += 1

    def __call__(self):

        return self._torrents

class ScrapDownload():

    """
        Return the final url.    
    """
    def __init__(self, link):
        self._url = f'https://www.rarbggo.to{link}'

    def __str__(self):
        return self._url

class ScrapMagnet(ScrapSearch):

    """
        Return the final magnet.    
    """
    def __init__(self, link):
        self._url = f'https://www.rarbggo.to{link}'
        soup = self.connection(self._url)
        self._magnet = soup.select_one('a[href*=magnet]').get('href')

    def __str__(self):
        return self._magnet
from bs4 import BeautifulSoup as bs
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

class Image:
    """
        Process of scraping some cover photos to embed the message of the bot.

        If you want to use this alone, feel free to do it.
    """

    def __init__(self, term: str):
        self._term = term.replace(' ', '-')
        self.quick_seach()

    def quick_seach(self):

        url = f'https://www.mobygames.com/search/quick?q={self._term}'
        self.get_title(self.connection(url))

    def full_search(self, full_term):

        url = f'{full_term}/cover-art'
        self.get_image(self.connection(url))

    @staticmethod
    def treatment(html: str):
        return " ".join(html.split()).replace('> <', '><')

    def connection(self, url: str):
        
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:106.0) Gecko/20100101 Firefox/106.0'}
            request = Request(url, headers=headers)
            response = urlopen(request)
            html = response.read().decode('utf-8')
            html = self.treatment(html)
            soup = bs(html, 'html.parser')
            return soup

        except HTTPError as e:
            print(e.status, e.reason)

        except URLError as e:
            print(e.reason)
    
    def get_title(self, soup):

        # Found where the image is.
        title = soup.find('div', {'class': 'searchTitle'}).a.get('href')
        self.full_search(title)

    def get_image(self, soup):

        # Get the image from website.
        images = []
        covers = soup.findAll('div', {'class': 'thumbnail-cover-caption'})
        for tag in covers:
            if 'Front Cover' in tag.get_text():
                image = tag.previous_sibling.select_one('a').get('href')
                images.append(image)

        soup = self.connection(f'{images[0]}')
        cover = soup.find('img', {'border': '0'}).get('src')

        self._result = f'https://www.mobygames.com{cover}'

    # Return the cover as a link.    
    def __str__(self):
        return self._result
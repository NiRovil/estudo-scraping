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
        self._quick_search_url = self.quick_search()
        self._cover_art_url = self.cover_art_url()
        self._image_url = self.image_url()
        self._soup = self.connection(self._image_url)
        self._image = self.get_image()

    def quick_search(self):
        quick_search_url = f'https://www.mobygames.com/search/quick?q={self._term}'
        return quick_search_url

    def image_url(self):
        image_url = f'{self._cover_art_url}/cover-art'
        return image_url

    @staticmethod
    def treatment(html: str):
        return " ".join(html.split()).replace('> <', '><')

    def connection(self, url):
        
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
    
    def cover_art_url(self):

        # Pick up the first result of the quick the search.
        soup = self.connection(self._quick_search_url)
        cover_art_url = soup.find('div', {'class': 'searchTitle'}).a.get('href')
        return cover_art_url

    def get_image(self):

        # Get the image from website.
        images = []
        covers = self._soup.findAll('div', {'class': 'thumbnail-cover-caption'})
        for tag in covers:
            if 'Front Cover' in tag.get_text():
                image = tag.previous_sibling.select_one('a').get('href')
                images.append(image)

        soup = self.connection(f'{images[0]}')
        cover = soup.find('img', {'border': '0'}).get('src')

        return f'https://www.mobygames.com{cover}'

    # Return the cover url.    
    def __str__(self):
        return self._image
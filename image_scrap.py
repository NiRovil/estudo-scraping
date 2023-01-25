from bot_resources import Resources

class Image(Resources):
    """
        Process of scraping some cover photos to embed the message of the bot.

        If you want to use this alone, feel free to do it.
    """

    def __init__(self, term: str):
        self._term = term.replace(' ', '-')
        self._url = self.url()
        self._soup = self.connection(self._url)
        self._image = self.get_image()

    def url(self):
        term_url = f'https://www.mobygames.com/search/quick?q={self._term}'
        soup = self.connection(term_url)
        url = f"{soup.find('div', {'class': 'searchTitle'}).a.get('href')}/cover-art"
        return url

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
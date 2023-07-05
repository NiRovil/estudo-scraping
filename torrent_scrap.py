from bot_resources import Resources

class ScrapSearch(Resources):

    """
        Process of scraping some torrents for the bot.

        If you want to use this alone, feel free to do it.
    """
    def __init__(self, term: str):
        self._term = term.replace(' ', '%20')
        self._url = self.url_search()
        self._soup = self.connection(self._url)
        self._torrents = self.find_torrent()
        self._final_torrents = self.torrent_filter()

    def url_search(self):
        url = f'https://www.rarbggo.to/search/?search={self._term}&order=seeders&by=DESC'
        return url

    def find_torrent(self):

        torrents = []
        contents = self._soup.findAll('tr', {'class': 'table2ta'})
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

        return torrents
    
    def torrent_filter(self):

        final_torrents = []
        index = 0

        for torrent in self._torrents:
            final_torrents.append([index+1, torrent[index]['name'], torrent[index]['type'], torrent[index]['space'], torrent[index]['seeds'], torrent[index]['release'], torrent[index]['url']])
            index += 1

        return final_torrents

    def __call__(self):

        return self._final_torrents

class ScrapDownload():

    """
        Return the final url.    
    """
    def __init__(self, url):
        self._url = f'https://www.rarbggo.to{url}'

    def __str__(self):
        return self._url

class ScrapMagnet(Resources):

    """
        Return the final magnet.    
    """
    def __init__(self, url):
        self._url = f'https://www.rarbggo.to{url}'
        self._soup = self.connection(self._url)
        self._magnet = self.find_magnet()

    def find_magnet(self):

        try:
            soup = self._soup.select_one('a[href*=magnet]').get('href')
            return soup
        
        except:
            return ''

    def __str__(self):
        return self._magnet
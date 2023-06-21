from bs4 import BeautifulSoup as bs
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

import requests
import json

class Resources():

    def connection(self, url):
        
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

    @staticmethod
    def html_treatment(html: str):
        return " ".join(html.split()).replace('> <', '><')

    @staticmethod
    def tormag(magnets):
        apiUrl = "https://tormag.ezpz.work/api/api.php?action=insertMagnets"
        data = {"magnets": 
            [
                magnet for magnet in magnets
            ]
        }
        resp = requests.post(apiUrl, json=data)
        responseJson = json.loads(resp.text)
        if "magnetEntries" in responseJson:
            links = responseJson["magnetEntries"]
            if links:
                return links
        else:
            print(responseJson["message"])
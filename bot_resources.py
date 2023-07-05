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
    def tormag(magnet):
        apiUrl = "https://tormag.ezpz.work/api/api.php?action=insertMagnets"
        data = {
            "magnets": [magnet]
        }
        resp = requests.post(apiUrl, json=data)
        responseJson = json.loads(resp.text)
        if "magnetEntries" in responseJson:
            links = responseJson["magnetEntries"]
            if links:
                print(links)
                return links
        else:
            print(responseJson["message"])

    @staticmethod
    def mgnetme(magnet):
        apiUrl = 'http://mgnet.me/api/create'
        data = {
            'm': magnet,
            'format': 'json'
        }
        resp = requests.post(apiUrl, data=data)
        responseJson = json.loads(resp.text)
        if 'shorturl' in responseJson:
            return responseJson['shorturl']
        

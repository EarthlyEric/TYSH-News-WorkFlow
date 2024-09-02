import requests
from bs4 import BeautifulSoup

class request():
    @classmethod
    def request(url:str):
        r=requests.get(url)
        decode=BeautifulSoup(r.text,"html.parser")
        
        return decode

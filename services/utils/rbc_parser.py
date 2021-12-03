import urllib.request
import requests
import re
from transliterate import translit
import pandas as pd
from bs4 import BeautifulSoup
import datetime
import argparse
import io
import json

class rbk_parse:
    def __init__(self, num_pages=1):
        self.n = num_pages
        self.rbc_articles = []
        self.delt = ['</div>\n', '<em>', '</em>', '&', '\"/>', '"og:description"', '<p>', '</p>', '<title>', '</title>', '<meta name=', '"description"',  'content="', '&amp;', 'laquo;', 'raquo;', 'nbsp;', 'mdash;']
        self.data_to_write = []
    
    def rbc_collect(self):
        page = requests.get("https://www.rbc.ru/")
        text = page.text

        reg_news = re.compile('<div class="main__feed js-main-reload-item".*?</div>', flags=re.DOTALL)
        text = ''.join(reg_news.findall(text))
        articles_reg = re.compile('<a href=".*?"', flags=re.DOTALL)
        articles = ''.join(articles_reg.findall(text))
        articles_reg = re.compile('https://.*?_main', flags=re.DOTALL)
        articles = articles_reg.findall(articles)[:self.n]
        self.rbc_articles = articles
    
    def get_text(self, output_path):
        self.rbc_collect()
        for art in self.rbc_articles:
            page = requests.get(art)
            text = page.text
            reg_refs = re.compile('<a.*?</a>', flags=re.DOTALL)
            refs = reg_refs.findall(text)
            reg_title = re.compile('<title>.*?</title>', flags=re.DOTALL)
            reg_desc = re.compile('<meta name="description".*?/>', flags=re.DOTALL)
            reg_txt = re.compile('<p>.*?</p>', flags=re.DOTALL)
            title = reg_title.findall(text)[0]
            desc = reg_desc.findall(text)[0]
            txtt = reg_txt.findall(text)
            for tx in txtt:
                if tx.find('<div') != -1:
                    txtt.remove(tx)
            for del_p in self.delt:
                title = title.replace(del_p, '')
                desc = desc.replace(del_p, '')
                for i in range(len(txtt)):
                    txtt[i] = txtt[i].replace(del_p, '')
            for rf in refs:
                title = title.replace(rf, '')
                desc = desc.replace(rf, '')
                for i in range(len(txtt)):
                    txtt[i] = txtt[i].replace(rf, '')
            self.data_to_write.append({'title' : title, 'description' : desc, 'text' : txtt})
        io.open(output_path, "w", encoding="utf-8").write(json.dumps(self.data_to_write, ensure_ascii=False))

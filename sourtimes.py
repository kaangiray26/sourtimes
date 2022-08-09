#!/usr/bin/python
# -*- encoding:utf-8 -*-

from datetime import date
from datetime import timedelta
import requests
from lxml import html
import time


class autocomplete:
    def __init__(self, query, titles, nicks):
        self.query = query
        self.titles = titles
        self.nicks = nicks


class news:
    def __init__(self, page, results):
        self.page = page
        self.results = results


class sour_item:
    def __init__(self, title, results):
        self.title = title
        self.results = results


class top_rated:
    def __init__(self, results):
        self.date = date.today() - timedelta(days=1)
        self.results = results


class sour:
    def __init__(self):
        self.headers = {
            "Host": "eksisozluk.com",
            "User-Agent": "Mozilla/5.0 (X11 Linux x86_64 rv: 102.0) Gecko/20100101 Firefox/102.0",
            "Accept": "application/json, text/javascript, */*",
            "Accept-Language": "en-US, en",
            "Accept-Encoding": "gzip, deflate, br",
            "X-Requested-With": "XMLHttpRequest",
            "Connection": "keep-alive"
        }

    def savepage(self, content):
        with open('response.html', 'wb') as f:
            f.write(content)

    def autocomplete(self, q):
        payload = {
            'q': q,
            '_': int(time.time()*1000)
        }
        r = requests.get("https://eksisozluk.com/autocomplete/query",
                         params=payload, headers=self.headers)

        if r.status_code != 200:
            raise Exception

        j = r.json()
        return autocomplete(j['Query'], j['Titles'], j['Nicks'])

    def news(self, page=1):
        payload = {
            'p': page,
            '_': int(time.time()*1000)
        }
        r = requests.get("https://eksisozluk.com/basliklar/gundem",
                         params=payload, headers=self.headers)

        if r.status_code != 200:
            raise Exception

        doc = html.fromstring(r.content.decode())
        return news(page, doc.xpath('//li/a/@href'))

    def query(self, q, page=1, nice=False):
        payload = {
            'q': q,
            '_': int(time.time()*1000),
            'p': page
        }

        if nice:
            payload['a'] = 'nice'

        r = requests.get("https://eksisozluk.com",
                         params=payload, headers=self.headers)
        if r.status_code != 200:
            raise Exception

        doc = html.fromstring(r.content.decode())
        return sour_item(q, [" ".join([t.strip() for t in content.itertext()]).strip() for content in doc.xpath('//li/div[@class="content"]')])

    def top_rated(self):
        r = requests.get("https://eksisozluk.com/debe", headers=self.headers)

        if r.status_code != 200:
            raise Exception

        doc = html.fromstring(r.content.decode())
        doc.xpath('//li/a/span/text()')
        return top_rated(doc.xpath('//li/a/span/text()'))


if __name__ == "__main__":
    sour = sour()
    i = input("Query: ")
    print(sour.autocomplete(i).titles)
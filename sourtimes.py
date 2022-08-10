#!/usr/bin/python
# -*- encoding:utf-8 -*-

from datetime import date
from datetime import timedelta
from multiprocessing.sharedctypes import Value
import requests
from lxml import html
import time


class autocomplete:
    """
    autocomplete class that provides titles and nicks from a query.

    Attributes:
        query (str): The search query
        titles (list): Title results
        nicks (list): Nick results
    """

    def __init__(self, query, titles, nicks):
        self.query = query
        self.titles = titles
        self.nicks = nicks

class sour_item:
    """
    sour_sitem class that provides contents from a title.

    Attributes:
        title (str): Title of the item
        results (list): Contents of the item
    """

    def __init__(self, title, results):
        self.title = title
        self.results = results


class sour_title:
    """
    sour_title class that provides title information.

    Attributes:
        url (str): URL of the title
        title (str): Title of the item
        count (int): Content count
    """

    def __init__(self, href, title, count):
        self.url = "https://eksisozluk.com" + href
        self.title = title
        self.count = count


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
        """
        Return titles by applying autocomplete to the query text.

        Args:
            q (str): Query text

        Returns:
            autocomplete object
        """

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
        """
        Return latest news titles.

        Args:
            page (int): The page index of the results

        Returns:
            list of sour_title objects
        """

        payload = {
            'p': page,
            '_': int(time.time()*1000)
        }
        r = requests.get("https://eksisozluk.com/basliklar/gundem",
                         params=payload, headers=self.headers)

        if r.status_code != 200:
            raise Exception

        doc = html.fromstring(r.content.decode())
        sour_titles = []
        results = doc.xpath('//li/a')

        for result in results:
            href = result.get('href')
            try:
                title, count = [t.strip() for t in result.itertext()]
            except ValueError:
                count = None

            sour_titles.append(sour_title(href, title, count))

        return sour_titles

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

    def search(self, keywords, author=None, page=1, fromdate=None, todate=None, nice_only=False, sort="Topic"):
        """
        Return titles that match the query parameters.

        Args:
            keywords (str): Search keywords
            author (str): Specific author for the titles
            page (int): Page number of the results
            fromdate (str): E.g. 1970-01-01
            todate (str): E.g. 1970-01-01
            nice_only (boolean): Show only top rated titles
            sort (str): ( Topic | Date | Count )

        Returns:
            list of sour_title objects
        """

        payload = {
            "SearchForm.Keywords": keywords,
            "SearchForm.Author": author,
            "SearchForm.When.From": fromdate,
            "SearchForm.When.To": todate,
            "SearchForm.NiceOnly": nice_only,
            "SearchForm.SortOrder": sort,
            '_': int(time.time()*1000),
        }
        r = requests.get("https://eksisozluk.com/basliklar/ara",
                         headers=self.headers, params=payload)

        if not r.status_code == 200:
            raise Exception

        doc = html.fromstring(r.content.decode())
        sour_titles = []
        results = doc.xpath('//li/a')

        for result in results:
            href = result.get('href')
            try:
                title, count = [t.strip() for t in result.itertext()]
            except ValueError:
                count = None

            sour_titles.append(sour_title(href, title, count))

        return sour_titles

    def top_rated(self):
        """
        Return highly rated titles from yesterday.

        Returns:
            list of sour_title objects
        """

        r = requests.get("https://eksisozluk.com/debe", headers=self.headers)

        if r.status_code != 200:
            raise Exception

        doc = html.fromstring(r.content.decode())
        sour_titles = []
        results = doc.xpath('//li/a')

        for result in results:
            href = result.get('href')
            title = result.xpath('./span/text()')[0]
            sour_titles.append(sour_title(href, title, None))
        return sour_titles


if __name__ == "__main__":
    eksi = sour()
    eksi.news()
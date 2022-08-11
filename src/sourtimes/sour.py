#!/usr/bin/python
# -*- encoding:utf-8 -*-

import time
import requests
from lxml import html
from exceptions import *


class channel:
    """
    channel class that provides channel information.

    Attributes:
        name (str): Name of the channel
        title (str): Title of the channel
        url (str): URL of the channel
    """

    def __init__(self, name, title, href):
        self.name = name[1:]
        self.title = title
        self.url = "https://eksisozluk.com" + href


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


class sour_entry:
    """
    sour_entry class that provides entry information.

    Attributes:
        entry_id (int): ID of the entry
        author_id (int): ID of the author
        author (str): Nickname of the author
        author_avatar (str): Avatar image of the author
        fav_count (int): Favorite count of the entry
        url (str): URL of the entry
        date (str): Entry date
        content (str): Content of the entry
    """

    def __init__(self, entry_id, author_id, author, avatar, fav_count, date, content):
        self.entry_id = entry_id,
        self.author_id = author_id
        self.author = author
        self.author_avatar = avatar
        if not self.author_avatar.startswith('http'):
            self.author_avatar = "https:" + self.author_avatar
        self.fav_count = fav_count
        self.url = f"https://eksisozluk.com/entry/{entry_id}"
        self.date = date
        self.content = content


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


class Sour:
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
            :class:`autocomplete` object
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
            page (int, optional): Page index of the results

        Returns:
            :obj:`list` of :class:`sour_title` objects
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
                title = "".join([t.strip() for t in result.itertext()])
                count = None
            sour_titles.append(sour_title(href, title, count))

        return sour_titles

    def query(self, q, page=1, nice=False):
        """
        Return entries from a page.

        Args:
            q (str): The query text
            page (int, optional): Page index of the results
            nice (boolean, optional): Option to sort entries by their favorite counts

        Returns:
            :obj:`list` of :class:`sour_entry` objects
        """
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
        sour_entries = []
        results = doc.xpath('//ul[@id="entry-item-list"]/li')

        for result in results:
            sour_entries.append(
                sour_entry(
                    result.get('data-id'),
                    result.get('data-author-id'),
                    result.get('data-author'),
                    result.xpath('.//img[@class="avatar"]/@src')[0],
                    result.get('data-favorite-count'),
                    result.xpath(
                        './/a[contains(@class, "entry-date")]/text()')[0],
                    " ".join([t.strip() for t in result.xpath(
                        './div[@class="content"]')[0].itertext()])
                )
            )
        return sour_entries

    def search(self, keywords, author=None, page=1, fromdate=None, todate=None, nice_only=False, sort="Topic"):
        """
        Return titles that match the query parameters.

        Args:
            keywords (str): Search keywords
            author (str, optional): Specific author for the titles
            page (int, optional): Page number of the results
            fromdate (str, optional): E.g. 1970-01-01
            todate (str, optional): E.g. 1970-01-01
            nice_only (boolean, optional): Show only top rated titles
            sort (str, optional): ( Topic | Date | Count )

        Returns:
            :obj:`list` of :class:`sour_title` objects
        """

        payload = {
            "SearchForm.Keywords": keywords,
            "SearchForm.Author": author,
            "SearchForm.When.From": fromdate,
            "SearchForm.When.To": todate,
            "SearchForm.NiceOnly": nice_only,
            "SearchForm.SortOrder": sort,
            "page": page,
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
                title = "".join([t.strip() for t in result.itertext()])
                count = None
            sour_titles.append(sour_title(href, title, count))

        return sour_titles

    def top_rated(self):
        """
        Return highly rated titles from yesterday.

        Returns:
            :obj:`list` of :class:`sour_title` objects
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

    def list_channels(self):
        """
        Return all channels

        Returns:
            :obj:`list` of :class:`channel` objects
        """
        r = requests.get("https://eksisozluk.com/kanallar",
                         headers=self.headers)

        if r.status_code != 200:
            raise Exception

        doc = html.fromstring(r.content.decode())
        results = doc.xpath('//ul[@id="channel-follow-list"]/li')

        channels = []
        for result in results:
            a = result.xpath('.//a[@class="index-link"]')[0]
            channels.append(
                channel(
                    name=a.text,
                    title=result.xpath('./p/text()')[0],
                    href=a.get('href')
                )
            )

        return channels

    def orphans(self, page=1):
        """
        Return all orphan titles

        Args:
            page (int, optional): Page index of the results

        Returns:
            :obj:`list` of :class:`sour_title` objects
        """

        payload = {
            "p": page
        }

        r = requests.get("https://eksisozluk.com/basliklar/basiboslar",
                         headers=self.headers, params=payload)

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
                title = "".join([t.strip() for t in result.itertext()])
                count = None
            sour_titles.append(sour_title(href, title, count))

        return sour_titles

    def get_channel(self, channel, page=1):
        """
        Return all titles under the given channel

        Args:
            channel (str): Name of the channel
            page (str, optional): Page index of the results

        Returns:
            :obj:`list` of :class:`sour_title` objects
        """

        payload = {
            "p": page,
            "_": int(time.time()*1000)
        }

        r = requests.get(
            f"https://eksisozluk.com/basliklar/kanal/{channel}", params=payload, headers=self.headers)

        if r.status_code != 200:
            raise ChannelException

        doc = html.fromstring(r.content.decode())
        sour_titles = []
        results = doc.xpath('//li/a')

        for result in results:
            href = result.get('href')
            try:
                title, count = [t.strip() for t in result.itertext()]
            except ValueError:
                title = "".join([t.strip() for t in result.itertext()])
                count = None
            sour_titles.append(sour_title(href, title, count))

        return sour_titles

    def throwback(self, year, page=1):
        """
        Return all titles from this day on the given year

        Args:
            year (int): Year to search for
            page (int, optional): Page index of the results

        Returns:
            :obj:`list` of :class:`sour_title` objects
        """

        payload = {
            "p": page,
            "_": int(time.time()*1000),
            "year": year
        }

        r = requests.get("https://eksisozluk.com/basliklar/tarihte-bugun",
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
                title = "".join([t.strip() for t in result.itertext()])
                count = None
            sour_titles.append(sour_title(href, title, count))

        return sour_titles

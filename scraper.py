#!/usr/bin/env python
# encoding: utf-8
__author__ = 'Larix'

import requests
from bs4 import BeautifulSoup

class Scraper():
    def __init__(self, search_term=''):
        self.user_agent = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
        self.search_term = search_term.replace(' ', '+')

    def fetch_yahoo_results(self):
        yahoo_url = 'https://tw.search.yahoo.com/search?fr=yfp-search-sb-bucket-836494&p={}'.format(self.search_term)
        response = requests.get(yahoo_url, headers=self.user_agent)
        response.raise_for_status()

        return response.text

    def fetch_bing_results(self):
        bing_url = 'https://www.bing.com/search?q={}'.format(self.search_term)
        response = requests.get(bing_url, headers=self.user_agent)
        response.raise_for_status()

        return response.text

    def fetch_google_results(self, number_results, language_code):
        google_url = 'https://www.google.com/search?q={}&num={}&hl={}'.format(self.search_term, number_results, language_code)
        response = requests.get(google_url, headers=self.user_agent)
        response.raise_for_status()

        return response.text

    def parse_yahoo_results(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        results = []
        rank = 1
        result_block = soup.find_all('div', attrs={'class': 'compTitle options-toggle'})
        for result in result_block:
            link = result.find('a', href=True)
            title = result.find('h3')
            brief = result.find('p', attrs={'class': 'lh-l'})
            if link and title:
                link = link['href']
                title = title.get_text()
                if brief:
                    brief = brief.get_text()
                if link != '#':
                    results.append({'rank': rank, 'title': title, 'brief': brief, 'link': link})
                    rank += 1
        return results

    def parse_bing_results(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        results = []
        rank = 1
        result_block = soup.find_all('li', attrs={'class': 'b_algo'})
        for result in result_block:
            link = result.find('a', href=True)
            title = result.find('h2')
            brief = result.find('p')
            if link and title:
                link = link['href']
                title = title.get_text()
                if brief:
                    brief = brief.get_text()
                if link != '#':
                    results.append({'rank': rank, 'title': title, 'brief': brief, 'link': link})
                    rank += 1
        return results

    def parse_google_results(self, html):
        soup = BeautifulSoup(html, 'html.parser')

        results = []
        rank = 1
        result_block = soup.find_all('div', attrs={'class': 'g'})
        for result in result_block:
            link = result.find('a', href=True)
            title = result.find('h3', attrs={'class': 'LC20lb'})
            brief = result.find('span', attrs={'class': 'st'})
            if link and title:
                link = link['href']
                title = title.get_text()
                if brief:
                    brief = brief.get_text()
                if link != '#':
                    results.append({'rank': rank, 'title': title, 'brief': brief, 'link': link})
                    rank += 1
        return results

    def scrape_yahoo(self):
        try:
            html = self.fetch_yahoo_results()
            results = self.parse_yahoo_results(html)
            return results
        except AssertionError:
            raise Exception("Incorrect arguments")
        except requests.HTTPError:
            raise Exception("You may be blocked by Yahoo")
        except requests.RequestException:
            raise Exception("connection error")

    def scrape_bing(self):
        try:
            html = self.fetch_bing_results()
            results = self.parse_bing_results(html)
            return results
        except AssertionError:
            raise Exception("Incorrect arguments")
        except requests.HTTPError:
            raise Exception("You may be blocked by Bing")
        except requests.RequestException:
            raise Exception("connection error")

    def scrape_google(self, number_results=50, language_code='zh-TW'):
        try:
            html = self.fetch_google_results(number_results, language_code)
            results = self.parse_google_results(html)
            return results
        except AssertionError:
            raise Exception("Incorrect arguments")
        except requests.HTTPError:
            raise Exception("You may be blocked by Google")
        except requests.RequestException:
            raise Exception("connection error")
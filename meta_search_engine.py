#!/usr/bin/env python
# encoding: utf-8
__author__ = 'Larix'

import time
from scraper import Scraper

if __name__ == '__main__':
    while True:
        try:
            value = str(input('Please Enter The Query Word:' + '\n'))
        except ValueError:
            print("Something Error")
            continue

        results = []
        scraper = Scraper(value)

        try:
            results = scraper.scrape_google() + scraper.scrape_bing() + scraper.scrape_yahoo()          
        except Exception as e:
            print(e)
        finally:
            time.sleep(5)

        for res in results:
            print(res['rank'])
            print(res['title'])
            print(res['link'])
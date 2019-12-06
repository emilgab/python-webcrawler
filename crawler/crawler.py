#!/usr/bin/python3
# crawl.py
# ~ This is the main script for initialising the crawling of a website ~

# imports
import urllib.request
import os
import re
import sys
import datetime

class Crawl():
    '''
    Crawl object which stores the site and methods related to crawling.
    '''
    # The object will store time data on when it was run.
    # This variable will  be used as filename for the crawl result and for the print statement
    run_date_and_time = '{0:%d-%m-%Y--%H:%M:%S}'.format(datetime.datetime.now())
    # The following variable "known_domains" will contain all unique urls
    known_domains = []

    def __init__(self, starting_url):
        self.starting_url = starting_url
        self.initialCrawl(self.starting_url)

    def initialCrawl(self, url):
        req = urllib.request.Request(url)
        resp = urllib.request.urlopen(req)
        print(resp.read())

    def recursiveCrawl(self, url):
        pass

    def writeToFile(self):
        pass

    def __str__(self):
        return "\nStarting domain crawled: %s \nDate and time: %s\n" % (self.starting_url, self.run_date_and_time)

    def crawlNext(self):
        pass

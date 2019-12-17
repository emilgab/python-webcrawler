#!/usr/bin/python3
# crawl.py
# ~ This is the main script for initialising the crawling of a website ~

# imports
import urllib.request
import os
import re
import datetime

class Crawl():
    '''
    Crawl object which stores the site and methods related to crawling.
    '''
    # The object will store time data on when it was run.
    # This variable will  be used as filename for the crawl result and for the print statement
    run_date_and_time = '{0:%d-%m-%Y--%H:%M:%S}'.format(datetime.datetime.now())
    # The following variable "known_domains" will contain all unique urls found during the crawl
    initial_crawl_result = []
    all_links = []
    crawl_tree = {}

    def __init__(self, starting_url):
        '''
        Initialise the object with the starting URL of the crawl
        '''
        self.starting_url = starting_url
        # Creates a regex pattern using the starting URL defined by the user
        self.regex_pat = 'href="('+self.starting_url+'+.*?)"'
        # Calls the method "initialCrawl"
        self.initialCrawl(self.starting_url)

    def initialCrawl(self, url):
        '''
        Takes in the starting URL to crawl
        '''
        try:
            # Parses the website using urllib.request
            req = urllib.request.Request(url)
            urlopen = urllib.request.urlopen(req)
            # stores the result of ReGex
            re_result = re.findall(self.regex_pat,str(urlopen.read()))
            if re_result:
                for i in re_result:
                    self.initial_crawl_result.append(i)
                    print(i)
            # Calls the recursiveCrawl method and passes in the first domain
            self.recursiveCrawl(self.initial_crawl_result[0])
        except:
            print("\nCould not find the URL, please try again")

    def recursiveCrawl(self, url):
        pass

    def writeToFile(self):
        pass

    def __repr__(self):
        '''
        Prints out the information on the parse when printing the object
        '''
        return "\nStarting domain crawled: %s \nDate and time: %s\nRegEx Pattern: %s\n" % (self.starting_url, self.run_date_and_time, self.regex_pat)

    def crawlNext(self):
        pass

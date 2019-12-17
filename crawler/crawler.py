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
    # The following variable "discovered_links" will contain all unique urls found during the crawl
    discovered_links = []

    def __init__(self, starting_url):
        '''
        Initialise the object with the starting URL of the crawl
        '''
        # Creating the folder structure

        self.starting_url = starting_url
        # Creates a regex pattern using the starting URL defined by the user
        self.regex_pat = 'href="('+self.starting_url+'+.*?)"'
        self.domain_name = re.findall('[.](.*)[.]',self.starting_url)[0]
        # Calls the method "initialCrawl"
        # The object will store time data on when it was run.
        # This variable will  be used as filename for the crawl result and for the print statement
        self.run_date_and_time = '{0:%d-%m-%Y-}'.format(datetime.datetime.now())
        # Creates the desired filename.
        # This filename shows date (day-month-year) and the domain name
        self.crawl_filename = self.run_date_and_time+"crawl_results_for_"+self.domain_name
        self.initialCrawl(self.starting_url)

    def initialCrawl(self, url):
        '''
        Takes in the starting URL to crawl
        '''
        self.createFiles()
        try:
            # Parses the website using urllib.request
            req = urllib.request.Request(url)
            urlopen = urllib.request.urlopen(req)
            # stores the result of ReGex
            re_result = re.findall(self.regex_pat,str(urlopen.read()))
            if re_result:
                for i in re_result:
                    if i in self.discovered_links:
                        continue
                    else:
                        self.discovered_links.append(i)
                        self.recursiveCrawl(i)
                        print(i)
        except Exception as exception:
            print(exception)


    def recursiveCrawl(self,url):
        try:
            req = urllib.request.Request(url)
            urlopen = urllib.request.urlopen(req)
        except urllib.error.HTTPError:
            return False
        re_result = re.findall(self.regex_pat, str(urlopen.read()))
        if re_result:
            for i in re_result:
                if i in self.discovered_links:
                    continue
                else:
                    self.discovered_links.append(i)
                    print("    "+i)
                    self.recursiveCrawl(i)

    def createFiles(self):
        # Checks if the dictionary exists or not
        if not os.path.exists("crawl_results"):
            # creates disctionary if it is missing
            os.mkdir("crawl_results")
        os.chdir("crawl_results")
        if not os.path.exists(self.crawl_filename):
            # Opens the file and closes it right away.
            # But now we have a file we can append to.
            open(self.crawl_filename+".txt",'w+').close()


    def __repr__(self):
        '''
        Prints out the information on the parse when printing the object
        '''
        return "\nStarting domain crawled: %s \nDate and time: %s\nRegEx Pattern: %s\n" % (self.starting_url, self.run_date_and_time, self.regex_pat)

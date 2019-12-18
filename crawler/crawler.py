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
    # Counts the occurrences of the word the user inputs
    word_count = 0

    def __init__(self, starting_url, word_to_count):
        '''
        Initialise the object with the starting URL of the crawl
        '''
        # Creating the folder structure

        self.starting_url = starting_url
        # Creates a regex pattern using the starting URL defined by the user
        self.regex_pat_crawl = 'href="('+self.starting_url+'+.*?)"'
        self.domain_name = re.findall('[.](.*)[.]',self.starting_url)[0]
        # Calls the method "initialCrawl"
        # The object will store time data on when it was run.
        # This variable will  be used as filename for the crawl result and for the print statement
        self.run_date_and_time = '{0:%d-%m-%Y-}'.format(datetime.datetime.now())
        # Creates the desired filename.
        # This filename shows date (day-month-year) and the domain name
        self.crawl_filename = self.run_date_and_time+"crawl_results_for_"+self.domain_name+".txt"
        self.word_to_count = word_to_count
        # Checks for if the user inputs a blank space (which means that the user dont want to count words)
        # This will be set to false if that is the case
        if self.word_to_count == " " or self.word_to_count == '':
            self.word_to_count = False
        # If word_to_count is True, then we create the filename for the file that will keep the count
        if self.word_to_count:
            # Filename structure: "[date]+count_for_word_[word_to_count]_on_[domain_name].txt
            self.count_filename = self.run_date_and_time+"count_for_word_"+self.word_to_count+"_on_"+self.domain_name+".txt"
        self.regex_pat_word_count = '["<p>"](.*?)["</p>"]'
        # calls the initialCrawl method and passes in the starting_url that was passed in by the user
        self.initialCrawl(self.starting_url)

    def initialCrawl(self, url):
        '''
        Takes in the starting URL to crawl and crawls it
        '''
        # Calls the createFiles() method that creates the necessary files and folders
        self.createFiles()
        # If the user gives a word for us to count, then we will inform the user with this
        if self.word_to_count:
            print("--")
            print("Ok, I will Count instances of the word: ",self.word_to_count)
            print("--")
        print("Scraping...")
        try:
            # Parses the website using urllib.request
            req = urllib.request.Request(url)
            urlopen = urllib.request.urlopen(req)
            # stores the result of ReGex
            re_result = re.findall(self.regex_pat_crawl,str(urlopen.read()))
            if re_result:
                for i in re_result:
                    # if the object in iteration already exists in our self.discovered_links list, then we skip it
                    if i in self.discovered_links:
                        continue
                    else:
                        # If it is a new link, then we append it to the list of known links
                        self.discovered_links.append(i)
                        # We open our file that we created with the createFiles() method and writes down the new url.
                        # We include a linebreak ("\n") to seperate links by rows
                        with open(self.crawl_filename,'a+') as file:
                            file.write(i+"\n")
                        self.recursiveCrawl(i)
                        print(i)
        # If an error appears, then we catch it an prints it out with a message at the beginning.
        except Exception as exception:
            print("Error in initialCrawl method: ",exception)


    def recursiveCrawl(self,url):
        # In the case of a 404 page not found error we want to have a try/except clause
        try:
            req = urllib.request.Request(url)
            urlopen = urllib.request.urlopen(req)
        # Catches the 404 page not found error reeturned by the urllib library
        # We want to return False, which skips this link to crawling.
        except urllib.error.HTTPError:
            return False
        re_result = re.findall(self.regex_pat_crawl, str(urlopen.read()))
        if re_result:
            for i in re_result:
                # Same process as in the initialCrawl() method
                # The only differences is that we write an indentation (two spaces) in the file and on the screen.
                if i in self.discovered_links:
                    continue
                else:
                    self.discovered_links.append(i)
                    with open(self.crawl_filename, 'a+') as file:
                        file.write('  '+i+"\n")
                    print('  '+i)
                    # If we can find a new and unique link on the page we are scraping, then we want to pass this in this method again
                    # This creates a circle, which will continue until it is no more unique links to scrape.
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
            open(self.crawl_filename,'w+').close()
        else:
            with open(self.crawl_filename,'r+') as file:
                for i in file.readlines():
                    self.discovered_links.append(i.strip(" \n"))
        # Checks if the self.word_to_count is True
        if self.word_to_count:
            # Checks if the file exists from before
            if not os.path.exists(self.count_filename):
                open(self.count_filename,'w+').close()

    def __repr__(self):
        '''
        Prints out the information on the parse when printing the object
        '''
        # Returns information that is useful for the user and the developer.
        # This includes:
        #   - Starting domain to crawl
        #   - Date and time of the crawl
        #   - Regular expression pattern used for the crawling of links
        return "\nStarting domain crawled: %s \nDate and time: %s\nRegEx Pattern: %s\n" % (self.starting_url, self.run_date_and_time, self.regex_pat_crawl)

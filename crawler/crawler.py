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
        Initialise the object with the starting URL and the word the user would like to count
        '''
        # We will use the starting URL to initialise the first crawl
        self.starting_url = starting_url
        # Creates a regex pattern using the starting URL defined by the user
        self.regex_pat_crawl = 'href="('+self.starting_url+'+.*?)"'
        # Uses regular expression to get just the domain name (example, "oslomet" instead of "https://www.oslomet.no/"")
        self.domain_name = re.findall('[.](.*)[.]',self.starting_url)[0]
        # The object will store time data on when it was run.
        # This variable will be used as filename for the crawl result and for the print statement
        self.run_date_and_time = '{0:%d-%m-%Y-}'.format(datetime.datetime.now())
        # Creates the desired filename.
        # This filename shows date (day-month-year) and the domain name
        self.crawl_filename = self.run_date_and_time+"crawl_results_for_"+self.domain_name+".txt"
        self.word_to_count = word_to_count
        # Checks for if the user inputs a blank space or nothing (which means that the user dont want to count words)
        # This will be set to false if that is the case
        if self.word_to_count == " " or self.word_to_count == '':
            self.word_to_count = False
        # If word_to_count is True, then we create the filename for the file that will keep the count
        # We will also create the regular expression that will look for words inside paragraph tags
        if self.word_to_count:
            # Filename structure: "[date]+count_for_word_[word_to_count]_on_[domain_name].txt
            self.count_filename = self.run_date_and_time+"count_for_word_"+self.word_to_count+"_on_"+self.domain_name+".txt"
            self.regex_pat_word_count = '["<p>"](.*?)["</p>"]'
        # calls the initialCrawl method and passes in the starting_url that was passed in by the user
        self.initialCrawl(self.starting_url)

    def initialCrawl(self, url):
        '''
        Takes in the starting URL to crawl and scrapes it for information
        '''
        # Calls the createFiles() method that creates the necessary files and folders
        self.createFiles()
        # If the user gives a word for us to count, then we will inform the user with this
        if self.word_to_count:
            print("--")
            print("Ok, I will Count instances of the word: ",self.word_to_count)
            print("--")
        print("Scraping...")
        # Parses the website using urllib.request
        req = urllib.request.Request(url)
        urlopen = urllib.request.urlopen(req)
        # stores the result of regular expression
        re_result = re.findall(self.regex_pat_crawl,str(urlopen.read()))
        # iterates over the result of the regular expression.
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
                        # Writes the url to the file (in append mode) and adds a line break
                        file.write(i+"\n")
                    if self.word_to_count:
                        # If we have to count a word, then we will call the countwords method
                        self.countWords(i)
                    self.recursiveCrawl(i)
                    print(i)


    def recursiveCrawl(self,url):
        # In the case of a 404 page not found error we want to have a try/except clause
        try:
            req = urllib.request.Request(url)
            urlopen = urllib.request.urlopen(req)
        # Catches the 404 page not found error reeturned by the urllib library
        # We want to return False, which skips this link to crawling.
        except urllib.error.HTTPError:
            return False
        # Same process as in the initialCrawl() method
        # The only differences is that we write an indentation (two spaces) in the file and on the screen and the recursiveness
        re_result = re.findall(self.regex_pat_crawl, str(urlopen.read()))
        if re_result:
            for i in re_result:
                if i in self.discovered_links:
                    continue
                else:
                    self.discovered_links.append(i)
                    with open(self.crawl_filename, 'a+') as file:
                        file.write('  '+i+"\n")
                    print('  '+i)
                    if self.word_to_count:
                        self.countWords(i)
                    # If we can find a new and unique link on the page we are scraping, then we want to pass this in this method again
                    # This creates a circle, which will continue until it is no more unique links to scrape.
                    self.recursiveCrawl(i)

    def createFiles(self):
        # Checks if the dictionary exists or not
        if not os.path.exists("crawl_results"):
            # creates a dictionary if it is missing
            os.mkdir("crawl_results")
        os.chdir("crawl_results")
        if not os.path.exists(self.crawl_filename):
            # Opens the file and closes it right away.
            # now we have a file we can append to.
            open(self.crawl_filename,'w+').close()
        else:
            # if the file already exists, we open it and appends each link that already is discovered to the list
            # we will also make sure that the link does not contain any spaces before or linebreaks after
            with open(self.crawl_filename,'r+') as file:
                for i in file.readlines():
                    self.discovered_links.append(i.strip(" \n"))
        # Checks if the self.word_to_count is True
        if self.word_to_count:
            # Checks if the file exists from before
            if not os.path.exists(self.count_filename):
                open(self.count_filename,'w+').close()

    def countWords(self,url):
        # Checks for 404 page not found
        try:
            req = urllib.request.Request(url)
            urlopen = urllib.request.urlopen(req)
        except urllib.error.HTTPError:
            return False
        # Assigns the result of regular expression
        word_count_result = re.findall(self.regex_pat_word_count,str(urlopen.read()))
        # This process joins everything that was found with the Regular expressions to one big string
        # the .split() method splits this string again by every space
        word_count_result = "".join(word_count_result).split()
        # iterates over the new list that was created with the split method.
        # this combines the words in the word_count_result to the word that was put in by the user
        # if there is a match, then we print the count to the screen and writes the count to the file.
        for i in word_count_result:
            if i.lower() == self.word_to_count:
                self.word_count += 1
                print(self.word_count)
                with open(self.count_filename,"w+") as f:
                    f.write((str(self.word_to_count)+" = "+str(self.word_count)))

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

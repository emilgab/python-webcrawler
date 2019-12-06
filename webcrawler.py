#!/usr/bin/python3
# crawl.py
# ~ This is the main script for initialising the crawling of a website ~

# imports
import sys
from crawler.crawler import Crawl

print("What website would you like to crawl?")
print("NOTE that the URL have to include 'http(s)://''")
x = Crawl(input("URL: "))
print(x)

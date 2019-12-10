#!/usr/bin/python3
# webcrawler.py
# ~ This is the main script for initialising the crawling of a website ~

# imports
import sys
import os
from crawler.crawler import Crawl

def welcome():
    rows, columns = os.popen('stty size','r').read().split()

    decoration = '--+ ~ * ~ +--'.center(int(columns))
    welcome_msg = "Welcome to this Python web crawler!".center(int(columns))
    credit = "Created by Emil Gabrielli".center(int(columns))
    course_inf = "for OsloMet course ACIT4420: Problem-Solving with scripting".center(int(columns))

    print("\n"*int(rows))
    print(decoration)
    print(welcome_msg)
    print(credit)
    print(decoration)
    print("\n"*(int(rows)//5))
    print("What website would you like to crawl?".center(int(columns)))
    print(" ")
    print("** NOTE **".center(int(columns)))
    print("The URL must include 'http(s)://'".center(int(columns)))
    print("A folder will be created containing crawl results".center(int(columns)))
    print("\n"*(int(rows)//5))

    try:
        x = Crawl(input("URL: "))
        print(x)
    except ValueError:
        print(" ")
        print("** !! **".center(int(columns)))
        print("Invalid URL, please try again.".center(int(columns)))
        print("** !! **".center(int(columns)))
        print(" ")

if __name__ == '__main__':
    welcome()

#!/usr/bin/python3
# webcrawler.py
# ~ This is the main script for initialising the crawling of a website ~

# imports
import os
from crawler.crawler import Crawl

def welcome():
    # Reads the size of the terminal window.
    # This is used later to centre the instructions to the scrren
    rows, columns = os.popen('stty size','r').read().split()

    # Some declerations that will be a part of the instructions window
    # The .center() is a method of the string object that will center the string based on a length.
    decoration = '--+ ~ * ~ +--'.center(int(columns))
    welcome_msg = "Welcome to this Python web crawler!".center(int(columns))
    credit = "Created by Emil Gabrielli".center(int(columns))
    course_inf = "for OsloMet course ACIT4420: Problem-Solving with scripting".center(int(columns))

    # Prints out the amount of rows in the terminal in line breaks
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
    print("A folder will be created in the same path as the script containing crawl results".center(int(columns)))
    print(" ")
    print("You will be asked to enter a word to count.".center(int(columns)))
    print("If you don't want to count a word then just input a space or just hit enter.".center(int(columns)))
    print("\n"*(int(rows)//5))

    try:
        # Asks the user for the two required inputs for the Crawl object
        x = Crawl(input("URL: "),input("What word would you like to count? "))
        # Calls the __repr__ method of the Crawl object
        print(x)
    except ValueError:
        print(" ")
        print("** !! **".center(int(columns)))
        print("Invalid URL, please try again.".center(int(columns)))
        print("** !! **".center(int(columns)))
        print(" ")

if __name__ == '__main__':
    welcome()

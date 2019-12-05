#!/usr/bin/python3
# crawl.py
# ~ This is the main script for initialising the crawling of a website ~

# imports
import urllib
import os
import re
import datetime

# The script will store time data on when it was run.
# This variable will also be used as filename for the crawl result
run_date_and_time = '{0:%d-%m-%Y--%H:%M:%S}'.format(datetime.datetime.now())

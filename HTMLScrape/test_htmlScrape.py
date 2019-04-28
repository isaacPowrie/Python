#! /bin/usr/python3

# Test file for HTMLScrape class
# Isaac Powrie 2018

import unittest

from htmlScrape import HTMLScrape

class HTMLScrapeTestCase(unittest.TestCase):
    '''Check the functionality of the HTMLScrape class'''
    
    def setUp(self):
        """Create instances of the HTMLScrape class"""
        self.htmlScrapes = []
        self.urls = ['http://www.gutenberg.org/',
            'gutenberg.org',
            'www.this.is/not/a/thingatall',
            'http://www.google.com/calendar/feeds/developer-calendar@google.com/public/full?alt=json']
        for url in self.urls:
            self.htmlScrapes.append(HTMLScrape(url))
    
    def test_get_html(self):
        """Does the get html work with this varied set of urls?"""
        for i in range(len(self.urls)):
            print(self.htmlScrapes[i].url)
            self.htmlScrapes[i].get_html()
            print("\n")
            
    def test_load_scrape(self):
        """Does the load scrape work for a functional url?"""
        test_scrape = self.htmlScrapes[0]
        print(test_scrape.url + "\n")
        test_scrape.load_scrape()
        print("\n")
        
unittest.main()
    

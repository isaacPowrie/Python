#! /usr/bin/python3

# htmlScrape.py
'''
This file contains the class definition for a type of object which holds
and scrapes raw html documents in order to expose various pieces of data
'''
# Isaac Powrie 2018

import requests, re

# Create the HTMLScrape class
class HTMLScrape():
    
    # Initialize the instance with a url
    def __init__(self, url):
        self.url = url
        self.raw_html = ''
        # Data loaded from html
        self.paras = []
        self.headers = []
        self.images = []
        self.links = []
        # Data loaded from extracted parts
        self.art_embedded_lnks = {}
        self.clean_paras = []
        self.clean_headers = []
        
        
    # Download html from url
    def get_html(self):
        # Validate url
        is_url = re.compile(r'''(
        (^https?://|^HTTPS?://|^www.)
        ([a-zA-Z0-9.]*)  # website name
        (\.[a-z]{1,3})   # .com etc
        (?:[/\\])        # check for longer path
        ([^\s]*)         # allow for any length of path
        )''',re.VERBOSE)
        check = is_url.search(self.url)
        if not check:
            print("**You may not be working with a valid URL**\n")
        # Check for .json
        if "json" in self.url:
            print("**You may be working with JSON data**\n")
        # get HTML
        try:
            req = requests.get(self.url)
            if req.status_code == 200:
                self.raw_html = req.text
            else:
                print("**The URL request was not successful**\n")
        except:
            print("**get_html was not able to derive the raw html**\n")
            
    '''
    Set of 'get_foo' functions to load various extracted data into
    the object
    '''
        
    # Get paragraphs and store in list
    def get_paras(self):
        # Regex for paragraph data, non greedy
        p = re.compile(r'(<p.*?>)(.*?)(</p>)', re.DOTALL)
        # Get paragraphs
        paras_groups = p.findall(self.raw_html)
        # Load paragraphs into object member
        if paras_groups:
            for groups in paras_groups:
                self.paras.append(groups[1])
        else:
            print("**No paragraphs have been found in html**\n")
        
    # Get headers and store in list
    def get_headers(self):
        # Regex for headers data, non greedy
        h = re.compile(r'(<h[0-9].*?>)(.*?)(</h[0-9]>)', re.DOTALL)
        # Get headers
        headers_groups = h.findall(self.raw_html)
        # Load headers into object member
        if headers_groups:
            for groups in headers_groups:
                self.headers.append(groups[1])
        else:
            print("**No headers have been found in html**\n")
        
    
    # Get image urls and store in list
    def get_images(self):
        # Regex for images data, non greedy
        i = re.compile(r'(<img .*?src=")(.*?)(".*?>)')
        # Get images
        images_groups = i.findall(self.raw_html)
        # Load images into object member
        if images_groups:
            for groups in images_groups:
                self.images.append(groups[1])
        else:
            print("**No images have been found in html**\n")
            
    # Get embedded links and store in list
    def get_embedded_lnks(self):
        # Regex for links, non greedy
        ln = re.compile(r'''
        (<a .*?href=")
        (.*?)       # Link URL
        (".*?>)
        (.*?)       # Link title
        (</a>)''', re.VERBOSE)
        # Get links and store in self.art_embedded_lnks
        if self.paras:
            for para in self.paras:
                links_groups = ln.findall(para)
                for group in links_groups:
                    self.art_embedded_lnks[group[3]] = group[1]
            if not self.art_embedded_lnks:
                print("**No links found embedded in article text**\n")
        else:
            message = "***\n"
            message += "No paragraph data has been loaded to look "
            message += "through,\n"
            message += "try running get_paras() method.\n***"
            print(message)
            
    # Cleanse paragraphs of embedded html and store results
    def cleanse_paras(self):
        if self.paras:
            for para in self.paras:
                clean_para = self.cleanse_html(para)
                self.clean_paras.append(clean_para)
        else:
            message = "***\n"
            message += "No paragraph data has been loaded to look "
            message += "through,\n"
            message += "try running get_paras() method.\n***"
            print(message)
            
    # Cleanse headers of embedded html and store results
    def cleanse_headers(self):
        if self.headers:
            for header in self.headers:
                clean_header = self.cleanse_html(header)
                self.clean_headers.append(clean_header)
        else:
            message = "***\n"
            message += "No header data has been loaded to look "
            message += "through,\n"
            message += "try running get_headers() method.\n***"
            print(message)
            
    # Get facts from text, sentence surrounding numeric
    def get_facts(self):
        if self.paras:
            if not self.clean_paras:
                self.cleanse_paras()
            # Fact data regex
            f = re.compile(r'''
            ([.?!] )?
            ([^.?!]*)   # NOT end of sentence chars
            (\d*)       # Numeric data
            ([^.?!]*)   # NOT end of sentence chars
            ([.?!])''', re.VERBOSE)
            # Get fact data and load into self.facts
            for clean_para in clean_paras:
                facts_groups = f.findall(clean_para)
                for group in facts_groups:
                    fact = group[1] + group[2] + group[3] + group[4]
                    self.facts.append(fact)
                if not self.facts:
                    print("**No facts found in article text**\n")
        else:
            message = "***\n"
            message += "No paragraph data has been loaded to look "
            message += "through,\n"
            message += "try running get_paras() method.\n***"
            print(message)
            
    # Get links from html
    def get_links(self):
        # Regex for link data, non greedy
        ln = re.compile(r'(<a.*?>)(.*?href=")(.*?)(".*?)(</a>)',
            re.DOTALL)
        # Get links
        links_groups = ln.findall(self.raw_html)
        # Load links into object member
        if links_groups:
            for group in links_groups:
                self.links.append(group[2])
            # Add home page to relative links
            i = 0
            home = self.extract_home()
            if home:
                for link in self.links:
                    if link[0] == "\\" or "/":
                        self.links[i] = home + link
                    i += 1
        else:
            print("**No links have been found in html**\n")
        
    '''
    Search functions for finding and extracting occurences of 
    called keyword/string
    '''
    # Find keyword in paras and return in list
    def search_paras(self, keystring):
        keystring = str(keystring)
        # Regex for keystring in sentence
        ks = re.compile(r'''
        ([.?!] )?
        ([^.?!]*)   # NOT end of sentence chars
        ''' + 
        r'(?<[\w])\s' +     # if character preceded then space
        keystring +
        r'(?![.?!])\s' +    # if not punctuation then space
        r'''
        ([^.?!]*)   # NOT end of sentence chars
        ([.?!])
        ''', re.VERBOSE)
        # Clean paragraph data of extra html
        if not clean_paras:
            self.cleanse_paras()
        # Search for occurrence of keystring, extract related data
        occurrences = []
        for para in clean_paras:
            if keystring in para:
                found_occs = ks.findall(para)
                for occ in found_occs:
                    occurrence = ''
                    for i in range(7):
                        occurence += occ[i]
                    occurrences.append(occurrence)
        # Return the list of occurrences
        return occurrences

    # Find keyword/string in headers and return in list
    def search_headers(self, keystring):
        keystring = str(keystring)
        # Regex for keystring in header
        ks = (r'''
         (?:^\w*)\s  # if character preceded then space
         ''' + 
         keystring +
         r'''
         (?![.?!])\s    # if not punctuation then space
         ([^.?!]*)   # NOT end of sentence chars
         ([.?!])
         ''', re.VERBOSE)
        if not clean_headers:
            self.cleanse_headers()
        # Search for occurrence of keystring, extract matched header
        occurrences = []
        for header in clean_headers:
            match = ks.search(header, re.IGNORECASE)
            if match:
                occurrences.append(match.groups(0))
        # Return the list of occurrences
        return occurrences
        
    # Find keyword/string in list and return list of occurances
    def search_list(self, keystring, srch_list):
        keystring = str(keystring)
        # Confirm srch_list is list
        try:
            if srch_list[0]:
                exit_flag = 0
        except:
            print("**Your search list is not a list or tuple**")
            exit_flag = 1
        # Search for occurrence of keystring, extract matches
        if exit_flag == 0:
            occurrences = []
            for item in srch_list:
                if keystring in item:
                    occurrences.append(item)
        # Return the list of occurrences
        return occurrences
    
    '''
    Various helper functions to cleanse/ alter extracted data
    '''
    # Cleanse html of inner html
    def cleanse_html(self, text):
        # Regex for html
        html = re.compile(r'(<)(.*?)( .*?>)(.*?)(</)(\2)(>)',
            re.DOTALL)
        text = re.sub(html, "\\4", text)
        return text
        
    # Extract home page
    def extract_home(self):
        # Regex for home page
        home = re.compile(r'www\.[\w\n]*\.[\w]{2,3}')
        home_page = home.search(self.url)
        if home_page:
            url = home_page.group(0)
        else:
            print("**Could not extract a home page from url**\n")
            url = ''
        return url
    
    '''
    Combo methods which use class functions to extract data
    in bulk or execute a series of actions in one call
    '''
    
    # Load main data
    def load_scrape(self):
        print("**Loading " + self.url + "**\n")
        self.get_html()
        if self.raw_html:
            self.get_paras()
            if self.paras:
                print("**Paragraph data loaded**\n")
            self.get_headers()
            if self.headers:
                print("**Header data loaded**\n")
            self.get_images()
            if self.images:
                print("**Image data loaded**\n")
            self.get_links()
            if self.links:
                print("**Link data loaded**\n")

/*
This file contains the readme for the html scrape python class structure.
FILE: readme.txt
CREATED ON: 2019/04/28
CREATED BY: Isaac Powrie
*/

THE PROJECT
This project creates a class module which takes in html and proccesses it 
into lists of it's component parts using regular expressions. These parts are
then made accessible and refinable by the object's methods. The intent of this
project is to create a class useful in web scraping projects. I have used this 
module in a web scraping project of my own which is collecting data from news
websites relevant to the 2019 Canadian federal election. In that project, I
use this module to load and process the data, as well as to find new links to
search, before passing the collected data to some additional helper functions
and finally inserting data into a sqlite database.

LIMITATIONS
Regular expressions are not perfect because it is difficult to account for all
possible matches while simultaneously begin specific enough to avoid all
unwanted matches. That said, they are still a powerful tool and as the test
case hopefully demonstrates this modules basic functionality works as expected 
with generic html sources from the real internet.

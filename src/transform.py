import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from src.config import RATING_MAP
from src.extract import scrape_news
from src.extract import extract_website
from urllib.parse import urljoin
from src.config import NEWS_WEBSITE
from src.config import SOURCE_NAME

##3 flatten data
##flatten_data = {} a dictionary only holds 1 value per key, works for {'Timestamp': [data_from_internetorfile['timestamp']], 
##                    'Latitude': [data_from_internetorfile['iss_position']['latitude']], 
##                    'Longitude': [data_from_internetorfile['iss_position']['longitude']]}
## but not for this, in this create a list instead (post 1 arrives: flatten_data['posttext'] = "Hello world"
##                                                then post 2 arrives: flatten_data['posttext'] = "I love Canada" -> Post 2 erases Post 1!)
## this does NOT create a list instead of a dictionary, this creates a LIST of dictionary
def parse_news(html):
    flatten_data_list = []
#for post in line_or_data:
#    flatten_data_list.append({'personpost': post['account']['acct'], 'posttext': post['content'], 
#                'posttime': post['created_at'], 'likes': post.get('favourites_count', 0), 'reposts': post.get('reblogs_count', 0)})
#tables = pd.DataFrame(flatten_data_list)
#
##4 print data into csv file
##4.1 clean up <> hmml tags:
#def clean_posttext(raw_text):
#    no_tags = re.sub(r'<[^>]+>', ' ' , str(raw_text))
#    decoded_text = html.unescape(no_tags)
#    clean_text = ' '.join(decoded_text.split())
#    return clean_text
#tables['posttext'] = tables['posttext'].apply(clean_posttext)

#import requests

##1 Change this to exact name of the file you want to check - or the destination of the internet you want to look for to extract data
#target_fileoraddress = "http://open-notify.org"

#print(f"--- Printing the first 3 data rows of: {target_fileoraddress} ---")

##Use 'errors=ignore' to bypass any messy formatting or bad character during read
#response_or_file = requests.get(target_fileoraddress) #or use with open() as response_or_file:... 
#                                                        #...(with the colon) for local  files...
#                                                        # or add these after parameter in requests.get(target_fileoraddress):...
#                                                        #...",encoding = 'utf-8', errors='ignore'" for local files
##do Not loop exactly 4 times (1 header row + 3 rows of data) - instead leave the script as a 1 off action
#line_or_data = response_or_file.text #or use line_or_data = response_or_file.readline() (for ONE single line --> loop 3 times for 3 rows) in local files
#
##clean up trailing line breaks and print
#print(line_or_data.strip())

## 1. Fetch the webpage
#url = "https://example.com"
#response = requests.get(url)

## 2. Parse the HTML content
#soup = BeautifulSoup(response.text, "html.parser")

## 3. Extract data
#title = soup.find("h1").get_text()
#links = [a["href"] for a in soup.find_all("a", href=True)]

#print("Page Heading:", title)
#print("Links:", links)

#this is already in "html" parameter 
#    file_or_data_transform = scrape_news(session, page_number_parse_book)
    line_BeautifulSoup_parsed = BeautifulSoup(html, "html.parser")
#if just line_BeautifulSoup_parsed, the loop only works on <html>:
#<html><body><ul><li>Apple</li><li>Banana</li></ul></body></html>
#Imagine opening a giant document and hitting Ctrl + F (Find). If you don't... 
#... type a word into the search bar, the computer doesn't know what you want. The...
#... parameter—the text you put inside the parentheses like ("li") or ("a")—is the word you are... 
#... typing into that search bar
#On the webpage, each book is wrapped in an HTML tag that looks like this:
#<article class="product_pod"> ... </article>
#This tag has two parts:
#• The Tag Name (article): What type of box it is.
#• The Class Name (product_pod): The nametag or label stuck on that specific box
#1. Filtering Out Other <article> Tags
#Websites often reuse generic tags like <article> for multiple things on the same page—such as blog posts, promotional banners, or user reviews.
#• soup.find_all("article") grabs every <article> on the page, which can crash your code if one of those boxes doesn't contain a book price.
#• class_="product_pod" acts as a strict filter, guaranteeing you only grab the boxes designed to hold books.
#2. Keeping Each Book's Data Paired Together
#If you only want a list of titles, you don't actually need product_pod—you could just search for soup.find_all("h3") directly.
#However, if you want to scrape multiple details per book (like Title + Price + Star Rating), grabbing the product_pod container first is essential
    for tag in line_BeautifulSoup_parsed.find_all("tr", class_="athing"):
#        print(line_or_data.strip())
#Why we use ["title"] instead of .text: Look closely at the HTML snippet above. The visible text...
#... between the tags (>A Light in the ...<) gets cut off with dots (...) when a book title is... 
#... long! However, the hidden title="A Light in the Attic" attribute inside the <a ...> tag...
#... always holds the complete, uncut book title
#        tag_BeautifulSoup_parsed = {"title": tag.text}
        tag_BeautifulSoup_parsed_articleid = tag.get("id")
#title is directly in the product_pod box but to find e.g price you have to... 
#... open a sub-box in that named "price_colour"
        tag_BeautifulSoup_parsed_headline = tag.find("span", class_="titleline").find("a")
        tag_BeautifulSoup_parsed_headline2 = tag_BeautifulSoup_parsed_headline.get_text(strip=True)
#index [0] will give value "star-rating" as in <p class="star-rating Three">
        tag_BeautifulSoup_parsed_source = SOURCE_NAME
#use result as key to dictionary RATING_MAP, retrieve value: db_host = config.DATABASE["host"]
#Because you didn't write import src.config as config, calling config.RATING_MAP[...] will crash
        tag_BeautifulSoup_parsed_publishat = tag.find_next_sibling("tr")
        if tag_BeautifulSoup_parsed_publishat is None:
                continue
        else:        
                tag_BeautifulSoup_parsed_publishat2 = tag_BeautifulSoup_parsed_publishat.find("span", class_="age")
        if tag_BeautifulSoup_parsed_publishat2 is None:
                continue
        else:
                tag_BeautifulSoup_parsed_publishat3 = tag_BeautifulSoup_parsed_publishat2["title"].split()[0]
        tag_BeautifulSoup_parsed_url = tag_BeautifulSoup_parsed_headline["href"]
        tag_BeautifulSoup_parsed_url2 = urljoin(NEWS_WEBSITE.format(page=1), tag_BeautifulSoup_parsed_url)
        tag_BeautifulSoup_parsed_text = tag_BeautifulSoup_parsed_headline2
#remove the square brackets [ ] and inner curly braces { } inside .append(...) so it...
#... appends a single dictionary instead of a list of 5 tiny dictionaries
#removing the extra braces will cause a SyntaxError because...
#... Python dictionaries always require ONE pair of outer curly braces { ... }
        flatten_data_list.append({"Article ID": tag_BeautifulSoup_parsed_articleid, 
                                "Title": tag_BeautifulSoup_parsed_headline2, 
                                "Source": tag_BeautifulSoup_parsed_source, 
                                "Publish at": tag_BeautifulSoup_parsed_publishat3, 
                                "URL": tag_BeautifulSoup_parsed_url2,
                                "Text": tag_BeautifulSoup_parsed_text})
    return flatten_data_list



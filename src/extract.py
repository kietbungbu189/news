import pandas as pd
import requests
from src.config import WEBSITE
from src.config import NEWS_WEBSITE

#this is fetch_page()
def extract_website(session, path):
#use this instead of "with open"
#only needed for API (e.g API's like Mastodon's search API requires 'type': 'statuses' to... 
#... return posts, or 'types': 'profiles' on BLueSky. They also requires #search_parameters = ...
#... {'q': 'Canada', 'limit': 100, 'type': 'statuses'} and search_parameters = {'limit':40} etc.
#    response_or_file = requests.get(path, params=search_parameters, headers=headers)
#this is to call 1-off connection
#    response_or_file = requests.get(path)
#this is to call reusable connections
    try:
        response_or_file = session.get(path, timeout=10)
        if response_or_file.status_code == 200:
            pass
        else:
            print(response_or_file.status_code)
            return None
#.exceptions.RequestException are attributes
    except requests.exceptions.RequestException as error:
        print(f"The error is {error}")
        return None
#this is for local file reading
#    file_or_data = response_or_file.readline()
#.text is an attribute like .varValue so no ()
#.encoding is also an attribute
    response_or_file.encoding = "utf-8"
    file_or_data = response_or_file.text
    return file_or_data
    
#def fetch_page(...) only defines the recipe—Python doesn't actually run it until scrape_books() calls it later

def scrape_news(session, page_number):
    path_scrapenews = NEWS_WEBSITE.format(page=page_number)
    a = extract_website(session, path_scrapenews)
    return a
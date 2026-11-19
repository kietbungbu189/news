from src.config import WEBSITE
from src.extract import extract_website
from src.extract import scrape_news
from src.load import create_csv
import requests
from src.transform import parse_news
from src.config import OUTPUT_CSV
import pandas as pd
from src.log import log_analysis
from src.analytics import graph
from src.analytics import top_10
from src.analytics import rating_count

def main():
    session_main = requests.Session()
#Dependency Injection  
    all_books = []
    for pg in range(1, 6):
        file_or_data_main = scrape_news(session_main, pg)
        if file_or_data_main is None:
            continue
        else:
            print(file_or_data_main[:500])
        
        data_dict = parse_book(file_or_data_main)
#data_dict is a list of 20 books. .append() puts the whole box inside all_books, creating...
#... 5 nested lists (which makes pd.DataFrame() build a broken 5-row × 20-column table)        
        all_books.extend(data_dict)
    df = pd.DataFrame(all_books)

    create_csv(df, OUTPUT_CSV)

    log_analysis(df)

    rate = rating_count(df)
    top = top_10(df)
    graph(df, top, rate)

if __name__ == "__main__":
    main()


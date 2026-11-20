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
from src.load import create_db
from src.config import DB
from src.config import COMPANIES
from src.analytics import match_company
from textblob import TextBlob
from src.analytics import get_sentiment 

def main():
    session_main = requests.Session()
#Dependency Injection  
    all_news = []
    for pg in range(1, 6):
        file_or_data_main = scrape_news(session_main, pg)
        if file_or_data_main is None:
            continue
        else:
            print(file_or_data_main[:500])
        
        data_dict = parse_news(file_or_data_main)
#data_dict is a list of 20 books. .append() puts the whole box inside all_books, creating...
#... 5 nested lists (which makes pd.DataFrame() build a broken 5-row × 20-column table)        
        all_news.extend(data_dict)
    df = pd.DataFrame(all_news)

#    create_csv(df, OUTPUT_CSV)
    create_db(df, DB)

    mc = match_company(df, COMPANIES)
    company_sent = []
    for idx, row_ in mc.iterrows():
        sentiment = get_sentiment(row_["Text"])
#Inside .iterrows(), modifying row_["Company sentiment"] = sentiment modifies a...
#... temporary copy of the row rather than mc itself
#        row_["Company sentiment"] = sentiment
        company_sent.append(sentiment)
#Instead, assign your company_sent list directly as a new column after the loop finishes
    mc["Company sentiment"] = company_sent

    create_csv(mc, OUTPUT_CSV)

    log_analysis(df)

#    rate = rating_count(df)
#    top = top_10(df)
#    graph(df, top, rate)

if __name__ == "__main__":
    main()


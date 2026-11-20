import pandas as pd
import functools
import numpy as np
import math
import matplotlib.pyplot as plt
from src.config import HIST
from src.config import BAR_CHART
from src.config import PIE_CHART
from textblob import TextBlob

def top_10(table):
#    average_ratings_bymoviestopdown = (
#        average_ratings_bymovies
#        .sort_values('rating', ascending=False)
#)
    top = table.sort_values('Price', ascending=False)
    return top.head(10)

def rating_count(table):
#    average_ratings_bymoviestopdown = (
#    average_ratings_bymovies.sort_values('rating', ascending=False)
#)
#    df_data2_count = df_data2['tag'].value_counts()
#    print(df_data2_count.head())
    count = table['Rating'].value_counts().sort_index()
    return count

def graph(table, top_10table, ratingCt):
#plot histogram
#    df_data3.hist(column="rating", figsize=(15, 10), bins=10)
#    plt.savefig('../img/show_histogram')
    table.plot(kind="hist", y="Price", figsize=(12, 8), bins=10)
    plt.savefig(HIST)
    plt.clf()
    top_10table.plot(kind="barh", y="Price", figsize=(12, 8), x="Book title")
    plt.savefig(BAR_CHART)
    plt.clf()
    ratingCt.plot(kind="pie", y="Rating", figsize=(12, 8))
    plt.savefig(PIE_CHART)
    return

def match_company(articles_df, companies):
    matched_list = []
    for idx, cp in enumerate(companies):
#        is_animation = df_data['genres'].str.contains("Animation")
        matched = articles_df[articles_df['Text'].str.contains(cp, case=False, na=False)]
        matched2 = matched.copy()
#        rsult = {}
#        for index2, value2 in order_qty_choices.items():
#            rsult[index2] = value2.varValue
#Right now, line 46 filters out the rows that mention cp (say, "Apple"), but it doesn't...
#... write "Apple" down anywhere on those rows. Once you combine all companies...
#... together, you wouldn't know which row matched which company!
        matched2["Matched company"] = cp
        matched_list.append(matched2)
#After the for loop finishes checking every company, matched_list is a list of separate...
#... mini-tables (one mini-table for Anthropic, one for Apple, one for OpenAI, etc.).
#Outside the loop, pd.concat(...):
#    unified_monthly = pd.concat(
#        [df_data3] + [df_data4],
#        ignore_index=True
#    )
#matched_list is already a list of DataFrames (just like [df_data3] + [df_data4] in your...
#... comment), whereas enumerate(matched_list) turns them into (0, df) tuples that...
#... crash pd.concat. Use matched_list directly with ignore_index=True
    matched_list_combined = pd.concat(matched_list, ignore_index=True)
    return matched_list_combined

def get_sentiment(company_text):
    score = TextBlob(str(company_text)).sentiment.polarity
    if score<0 and score>=-1:
        text_sentiment = "negative"
    elif score == 0:
        text_sentiment = "neutral"
    else:
        text_sentiment = "positive"
    return text_sentiment



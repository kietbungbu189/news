import pandas as pd
import functools
import numpy as np
import math
import matplotlib.pyplot as plt
from src.config import HIST
from src.config import BAR_CHART
from src.config import PIE_CHART


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




from pathlib import Path
from src.config import DB
import sqlite3
from src.config import OUTPUT_CSV

def create_csv(dataframe, OUTPUT_CSV):
    a = dataframe.to_csv(OUTPUT_CSV, index=False, encoding = "utf-8")
    return a
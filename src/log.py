from datetime import datetime
#1 Record when an analysis occurs
from src.config import LOG

def log_analysis(table):
    x = datetime.now()
    log_time = x.strftime("%I:%M:%S %p  %a %b-%d-%Y")
    message = (
    f"\nanalysis logged: {log_time}"
    #or f"Run time: {x:%c}"
    f"\nRecords of books imported to csv: {len(table)}"
#shows numbers of rows top down
    )
#shows number of rows top down of dataframe table 
    with open(LOG, mode="a") as log:
        log.write(message)

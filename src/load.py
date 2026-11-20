from pathlib import Path
from src.config import DB
import sqlite3
from src.config import OUTPUT_CSV

def create_csv(dataframe, OUTPUT_CSV):
    a = dataframe.to_csv(OUTPUT_CSV, index=False, encoding = "utf-8")
    return a

def create_db(dataframe, DB):
#    def create_db(dim1, dim2, dim3, fact):
    datadir = Path(DB)
    datadir.parent.mkdir(parents=True, exist_ok=True)
    db_connect = sqlite3.connect(datadir)
    db_connect.execute("PRAGMA foreign_keys=ON")

#Right now, DROP TABLE IF EXISTS newstable erases all...
#... previously saved articles every time you run your script!
#    query_drop_newstable = 'DROP TABLE IF EXISTS newstable'
#    query4 = 'CREATE TABLE supply_chain_datas  (SKU VARCHAR(20), Availability INTEGER, "Number of products sold" INTEGER, "Revenue generated" REAL, "Customer demographics" VARCHAR(20), "Stock levels" INTEGER, "Lead times" REAL, "Order quantities" INTEGER, "Shipping times" REAL, "Shipping costs" REAL, "Lead time" REAL, "Production volumes" INTEGER, "Manufacturing lead time" REAL, "Manufacturing costs" REAL, "Inspection results" VARCHAR(20), "Defect rates" REAL, "Costs" REAL, "Supplier index" INTEGER, "Logistics index" INTEGER, FOREIGN KEY (SKU) REFERENCES products(SKU), FOREIGN KEY ("Supplier index") REFERENCES suppliers("Supplier index"), FOREIGN KEY ("Logistics index") REFERENCES logistics("Logistics index"))'
    query4 = 'CREATE TABLE IF NOT EXISTS newstable ("Article ID" VARCHAR(20) PRIMARY KEY, Title VARCHAR(20), Source VARCHAR(20), "Publish at" VARCHAR(20), URL TEXT, Text VARCHAR(20));'
    
#    db_connect.execute(query_drop_newstable)
    db_connect.execute(query4)


#load into db
#1 identify target
#done by config.py
#target_fileoraddress = "C:/Users/USER/Downloads/study docs/Comp604/assignment/assignment2/New Version/dim_Logistics.csv"

#2 open target
#done by extract.py
#with open(target_fileoraddress, mode="r") as response_or_file:
    #line_or_data = response_or_file.readline()
#response_or_file = pd.read_csv(target_fileoraddress)

#2.1 extract data and save into variable:
#done by transform.py
#oltp_product = pd.DataFrame({'Logistics index':response_or_file['Logistics index'], 'Shipping carriers':response_or_file['Shipping carriers'], 
#                             'Transportation modes':response_or_file['Transportation modes'], 'Routes':response_or_file['Routes']}) 

#3 load into sql:
#doing here, but instead of loading simultaneouly with creating tables as... 
#...below (creating done by python automatically), here tables are created manually first...
#...and the DataFrame from step 2.1 (which is from using function in transform.py as...
#...said above) is then saved to variable "raw" in main and loaded using function...
#...in load.py (which is here)
#connection1 = sqlite3.connect('database.db')
#oltp_product.to_sql('logistics', connection1)

#Pandas .to_sql(..., if_exists="append") does not support INSERT OR IGNORE—if it hits...
#... a PRIMARY KEY duplicate on Run 2, Pandas will crash with a sqlite3.IntegrityError
#    dataframe.to_sql('newstable', db_connect, if_exists="append", index=False)
    cursor = db_connect.cursor()
#    for index, row_ in filtered_supplier.iterrows():
#    order_qty_choices[index] = to_minimize_prob.add_variable(
#        f"order_qty{index}",
#        lowBound=0,
#        cat="Integer"
#    )
    for row_, value in dataframe.iterrows():
#"INSERT OR IGNORE INTO users (id, email) VALUES (?, ?)"->query4, 
#    users_to_add->execute

        execute = 'INSERT OR IGNORE INTO newstable ("Article ID", Title, Source, "Publish at", URL, Text) VALUES (?, ?, ?, ?, ?, ?);'
        values = (value["Article ID"], value["Title"], value["Source"], value["Publish at"], value["URL"], value["Text"])
#db_connect.execute(query4)
#use singular execute, if import all rows at once (when no one-after-another sessions executed)...
#... then need a list of data rows -> use executemany instead of "for" loop
        cursor.execute(execute, values)
    db_connect.commit()
    db_connect.close()
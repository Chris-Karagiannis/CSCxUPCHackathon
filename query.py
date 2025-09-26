import sqlite3
import csv
import pandas as pd

dataPath = '/Users/ashishbehal/Documents/GitHub/CSCxUPCHackathon/data/adidasNike.csv'

# with open(dataPath, mode = 'r', newline='', encoding='utf-8') as file:
#     reader = csv.reader(file)

#     headers = next(reader)
#     print(f"{' | '.join(headers)}")
#     print('-' * 50)

#     for row in reader:
#         print(f"{' | '.join(row)}")

df = pd.read_csv(dataPath)

# Connecting to the downloaded databases
dataConnection = sqlite3.connect('AdidasAndNike_database.db')
cursor = dataConnection.cursor()

table_name = "my_table"
# this below writes the contents of dataFrame(which i got from read_csv above) into a sql database table
df.to_sql(table_name, dataConnection,if_exists='replace',index=False)

#Querying the database
query = f"SELECT  * FROM {table_name};"
result = pd.read_sql_query(query,dataConnection)

print(result)
dataConnection.close()

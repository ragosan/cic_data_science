import sqlite3
import pandas as pd

df = pd.read_csv('investigators.csv')

df.columns = df.columns.str.strip()

connection = sqlite3.connect('cic.db')

df.to_sql('investigators', connection, if_exists='replace')

connection.close()
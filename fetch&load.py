'''
This script will connect to Axie Sales URL and retreive data as JSON. The data is sanitized and inserted
in a connect postgres glcoud database instance
'''

import psycopg2
import requests
from urllib.request import urlopen
import json
from psycopg2.extras import Json

# Connect to axie sales and pull data in a JSON
url = "https://artifacts.space/sales"
response = urlopen(url)
record_list = json.loads(response.read())

if type(record_list) == list:
    first_record = record_list[0]

# get the column names from the first record
columns = list(first_record.keys())
print ("\ncolumn names:", columns) # I can use this to create database columns in the future for automation

table_name = "sales"
sql_string = 'INSERT INTO {} '.format(table_name)
sql_string += "(" + ', '.join(columns) + ")\nVALUES "

# enumerate over the record
for i, record_dict in enumerate(record_list):

    # iterate over the values of each record dict object
    values = []
    for col_names, val in record_dict.items():

        # Postgres strings must be enclosed with single quotes
        if type(val) == str:
            # escape apostrophe with two single quotations
            val = val.replace("'", "''")
            val = "'" + val + "'"

        values += [str(val)]

    # join the list of values and enclose record in parenthesis
    sql_string += "(" + ', '.join(values) + "),\n"

# remove the last comma and end statement with a semicolon
sql_string = sql_string[:-2] + ";"

## Ignore for now, will delete later if necessary

# # value string for the SQL string
# values_str = ""
#
# # enumerate over the records' values
# for i, record in enumerate(values):
#
#     # declare empty list for values
#     val_list = []
#
#     # append each value to a new list of values
#     for v, val in enumerate(record):
#         if type(val) == str:
#             val = str(Json(val)).replace('"', '')
#         val_list += [str(val)]
#
#     # put parenthesis around each record string
#     values_str += "(" + ', '.join(val_list) + "),\n"
#
# # remove the last comma and end SQL with a semicolon
# values_str = values_str[:-2] + ";"

# # concatenate the SQL string
# table_name = "json_data"
# sql_string = "INSERT INTO %s (%s)\nVALUES %s" % (
#     table_name,
#     ', '.join(columns),
#     values_str
# )

try:
    # declare a new PostgreSQL connection object
    conn = psycopg2.connect(dbname="axie-data", user="axieDataAdmin", password="AxieInsights#1", host="35.225.243.143")
    # create cursor
    cur = conn.cursor()
    print("\ncreated cursor object:", cur)

except (Exception, Error) as err:
    print ("\npsycopg2 connect error:", err)
    conn = None
    cur = None

# only attempt to execute SQL if cursor is valid
if cur != None:
    try:
        cur.execute(sql_string)
        conn.commit()
        print('\nfinished INSERT INTO execution')

    except (Exception, Error) as error:
        print("\nexecute_sql() error:", error)
        conn.rollback()

    # close the cursor and connection
    cur.close()
    conn.close()

import datetime
from datetime import datetime
import json
import requests
import psycopg2
from urllib.request import urlopen
import json
from psycopg2.extras import Json

# query
testQuery = """
query GetRecentlyAxiesSold($from: Int, $size: Int) {
  settledAuctions {
    axies(from: $from, size: $size) {
      total
      results {
        ...AxieSettledBrief
        transferHistory {
          ...TransferHistoryInSettledAuction
          __typename
        }
        __typename
      }
      __typename
    }
    __typename
  }
}
fragment AxieSettledBrief on Axie {
  id
  class
  parts {
    ...AxiePart
    __typename
  }
  stats {
    ...AxieStats
    __typename
  }
}
fragment AxiePart on AxiePart {
  id
}
fragment AxieStats on AxieStats {
  hp
  speed
  skill
  morale
  __typename
}
fragment TransferHistoryInSettledAuction on TransferRecords {
  total
  results {
    ...TransferRecordInSettledAuction
    __typename
  }
  __typename
}
fragment TransferRecordInSettledAuction on TransferRecord {
  timestamp
  withPrice
  withPriceUsd
}
"""

# post request
post = {
    "operationName": "GetRecentlyAxiesSold",
    "variables": {
        "from": 0,
        "size": 100
    },
    "query": testQuery,
}

# Make query
url = "https://graphql-gateway.axieinfinity.com/graphql"
r = requests.post(url, post)
res = r.json()
# write to a file -- THIS IS FOR SCRIPT BEHAVIOR CONFIRMATION. DELETE WHEN NO LONGER NECESSARY
with open('axiedata.json', 'w') as f:
    json.dump(res, f)


# Parse through the response JSON and store important values in a dictionary
def get_axie_data(dictionary):

    # defaults
    axies_list = []
    i = 0
    axie_data = dict()

    # Set default datetime to now (UTC)
    now = datetime.now()
    sys_time = now.strftime("%Y-%m-%d %H:%M:%S")

    # connect to database
    conn = psycopg2.connect(dbname="axie-data", user="axieDataAdmin", password="AxieInsights#1", host="35.225.243.143")

    for item in dictionary['data']['settledAuctions']['axies']['results']:
        axies_list.append(item['id'])

        axie_data['id'] = item['id']
        axie_data['class'] = item['class']
        axie_data['hp'] = item['stats']['hp']
        axie_data['speed'] = item['stats']['speed']
        axie_data['skill'] = item['stats']['skill']
        axie_data['morale'] = item['stats']['morale']

        axie_parts = []

        for part in item['parts']:
            axie_parts.append(part['id'])

        axie_data['eyesd'] = axie_parts[0]
        axie_data['earsd'] = axie_parts[1]
        axie_data['backd'] = axie_parts[2]
        axie_data['mouthd'] = axie_parts[3]
        axie_data['hornd'] = axie_parts[4]
        axie_data['taild'] = axie_parts[5]

        if item['transferHistory']['total'] > 1:
            for transactions in item['transferHistory']['results']:
                if transactions['timestamp'] == 0:
                    timestamp = sys_time
                else:
                    timestamp = datetime.fromtimestamp(transactions['timestamp'])
                price = (int(transactions['withPrice']) / 10 ** 18)
                axie_data['timestamp'] = timestamp
                axie_data['price'] = price

                # Execute SQL statement
                execute_sql(axie_data, conn)
                i += 1

        # add in different rows
        elif item['transferHistory']['total'] == 1:
            for transactions in item['transferHistory']['results']:
                if transactions['timestamp'] == 0:
                    timestamp = sys_time
                else:
                    timestamp = datetime.fromtimestamp(transactions['timestamp'])
                price = (int(transactions['withPrice']) / 10 ** 18)
                axie_data['timestamp'] = timestamp
                axie_data['price'] = price

                # Execute SQL statement
                execute_sql(axie_data, conn)
                i += 1

    # close database
    conn.close()

    print("length of unique AxieID in response: ", len(axies_list))
    print("Total rows added added:", i)


# Connect to database and add to table
def execute_sql(axie_sales_dict, db_conn):
    # create cursor
    cur = db_conn.cursor()

    cols = axie_sales_dict.keys()
    cols_str = ", ".join(cols)

    vals = [str(axie_sales_dict[x]) for x in cols]
    vals_str_list = ["%s"] * len(vals)
    vals_str_actual = ", ".join(vals)
    vals_str = ", ".join(vals_str_list)

    # Generate SQL
    sql_string = f"INSERT INTO sales ({cols_str}) VALUES ({vals_str})"

    # exectue sql
    cur.execute(sql_string, vals)
    db_conn.commit()

    cur.close()


# Run script
print("Running script... \n")
get_axie_data(res)
print("\n-------------------------")
print("DONE MOTHER FUCKER")

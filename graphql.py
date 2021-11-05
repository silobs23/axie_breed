import datetime
import json
import requests

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

    axie_data = {}

    for item in dictionary['data']['settledAuctions']['axies']['results']:
        axie_id = item['id']
        axie_class = item['class']
        axie_parts = []
        axie_history = []

        for part in item['parts']:
          axie_parts.append(part['id'])

        hp = item['stats']['hp']
        speed = item['stats']['speed']
        skill = item['stats']['skill']
        morale = item['stats']['morale']

        for transactions in item['transferHistory']['results']:
          timestamp = datetime.datetime.fromtimestamp(transactions['timestamp'])
          price = (int(transactions['withPrice']) / 10 ** 18)
          axie_history.append((timestamp, price))

        # this should be a list because a set doesn't have a garanteed order
        axie_data[axie_id] = (axie_class, axie_parts, hp, speed, skill, morale, axie_history)

    return axie_data

# Print out the axie data
data = get_axie_data(res)
for k, v in data.items():
    print(f"{k} : {v}")


# loop through the dictionary and add the data to the table



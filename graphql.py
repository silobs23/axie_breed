import json
import requests


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
  name
  image
  class
  breedCount
  __typename
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
  name
  class
  type
  specialGenes
  stage
  abilities {
    ...AxieCardAbility
    __typename
  }
  __typename
}

fragment AxieCardAbility on AxieCardAbility {
  id
  name
  attack
  defense
  energy
  description
  backgroundUrl
  effectIconUrl
  __typename
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
  from
  to
  txHash
  timestamp
  withPrice
  withPriceUsd
  fromProfile {
    name
    __typename
  }
  toProfile {
    name
    __typename
  }
  __typename
}

"""

# Gets the latest Axies sold
url = "https://graphql-gateway.axieinfinity.com/graphql"
post = {
  "operationName": "GetRecentlyAxiesSold",
  "variables": {
    "from": 100000,
    "size": 100
  },
  "query": testQuery,
  # "query": "query GetRecentlyAxiesSold($from: Int, $size: Int) {\n  settledAuctions {\n    axies(from: $from, size: $size) {\n      total\n      results {\n        ...AxieSettledBrief\n        transferHistory {\n          ...TransferHistoryInSettledAuction\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment AxieSettledBrief on Axie {\n  id\n  name\n  class\n  breedCount\n stage\n  __typename\n}\n\nfragment TransferHistoryInSettledAuction on TransferRecords {\n  total\n  results {\n    ...TransferRecordInSettledAuction\n    __typename\n  }\n  __typename\n}\n\nfragment TransferRecordInSettledAuction on TransferRecord {\n  from\n  to\n  txHash\n  timestamp\n  withPrice\n  withPriceUsd\n  fromProfile {\n    name\n    __typename\n  }\n  toProfile {\n    name\n    __typename\n  }\n  __typename\n}\n"
}

r = requests.post(url, post)
res = r.json()
print(type(res))
with open('axiedata.json', 'w') as f:
  json.dump(res, f)

print(res)


# Get Axie info
#post_axie_details = {
#  "operationName": "GetAxieDetail",
#  "variables": {
#    "axieId": "3728782"
#  },
#  "query": "query GetAxieDetail($axieId: ID!) {\n  axie(axieId: $axieId) {\n    ...AxieDetail\n    typename\n  }\n}\n\nfragment AxieDetail on Axie {\n  id\n  image\n  class\n  chain\n  name\n  genes\n  owner\n  birthDate\n  bodyShape\n  class\n  sireId\n  sireClass\n  matronId\n  matronClass\n  stage\n  title\n  breedCount\n  level\n  figure {\n    atlas\n    model\n    image\n    typename\n  }\n  parts {\n    ...AxiePart\n    typename\n  }\n  stats {\n    ...AxieStats\n    typename\n  }\n  auction {\n    ...AxieAuction\n    typename\n  }\n  ownerProfile {\n    name\n    typename\n  }\n  battleInfo {\n    ...AxieBattleInfo\n    typename\n  }\n  children {\n    id\n    name\n    class\n    image\n    title\n    stage\n    typename\n  }\n  typename\n}\n\nfragment AxieBattleInfo on AxieBattleInfo {\n  banned\n  banUntil\n  level\n  typename\n}\n\nfragment AxiePart on AxiePart {\n  id\n  name\n  class\n  type\n  specialGenes\n  stage\n  abilities {\n    ...AxieCardAbility\n    typename\n  }\n  typename\n}\n\nfragment AxieCardAbility on AxieCardAbility {\n  id\n  name\n  attack\n  defense\n  energy\n  description\n  backgroundUrl\n  effectIconUrl\n  typename\n}\n\nfragment AxieStats on AxieStats {\n  hp\n  speed\n  skill\n  morale\n  typename\n}\n\nfragment AxieAuction on Auction {\n  startingPrice\n  endingPrice\n  startingTimestamp\n  endingTimestamp\n  duration\n  timeLeft\n  currentPrice\n  currentPriceUSD\n  suggestedPrice\n  seller\n  listingIndex\n  state\n  __typename\n}\n"
#}
#
#r = requests.post(url, post_axie_details)
#res = r.json()

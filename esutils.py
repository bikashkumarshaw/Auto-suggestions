import json

import requests
from urllib.parse import urljoin

HEADERS = {'Content-type': 'application/json'}

ES_NGRAM_MAPPING ={
  "settings": {
    "analysis": {
      "analyzer": {
        "autocomplete": {
          "tokenizer": "autocomplete",
          "filter": [
            "lowercase"
          ]
        }
      },
      "tokenizer": {
        "autocomplete": {
          "type": "ngram",
          "min_gram": 2,
          "max_gram": 30,
          "token_chars": [
            "letter",
            "digit"
          ]
        }
      }
    }
  },
  "mappings": {
    "_doc": {
    "dynamic": False,
    "properties": {
      "token": {
        "type": "text",
        "analyzer": "autocomplete",
       }
     }
   }
  }
}

def create_index(es_loc, name):
    u = urljoin(es_loc, '/%s/' % name)
    r = requests.put(u, data=json.dumps(ES_NGRAM_MAPPING), headers = HEADERS)
    return r.json()

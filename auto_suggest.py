from flask import Flask, request
import json
import requests

from args import _define_args
from load_mapping import _load_mapping
from query import ES_SUGGEST_QUERY

app = Flask(__name__)

ARGS = _define_args()

ES_HEADERS = {'Content-type': 'application/json'}

tok_map = _load_mapping(ARGS.f_name)

@app.route("/api/search", methods=["GET", "POST"])
def search():
    '''
    This function requests Elastic Search with the queried word
    and returns suggestions by combining results with prefix match
    and sorted suffix matches with occurrences
    '''

    if request.method == 'POST':
        word = request.json["word"]
    else:
        word = request.args.get("word")

    word = word.lower().replace(" ", "_").replace("-", "_")

    ES_SUGGEST_QUERY["query"]["match"]["token"]["query"] = word

    r = requests.get("{0}:{1}/{2}/_doc/_search".format(ARGS.es_url, ARGS.es_port, ARGS.es_index), \
            data=json.dumps(ES_SUGGEST_QUERY), headers=ES_HEADERS)

    resp = r.json().get("hits", {}).get("hits", [])

    prefix_matches = []
    suffix_matches = []
    for val in resp:
        token = val.get("_source", {}).get("token", {})
        if token.startswith(word[:4]):
            prefix_matches.append(token)
        else:
            occur = tok_map.get(token, 0)
            suffix_matches.append((token, occur))

    suffix_matches = sorted(suffix_matches, key=lambda x: x[1], reverse=True)

    prefix_matches.extend(list(map(lambda x: x[0], suffix_matches)))


    return json.dumps({"suggestions": prefix_matches})

if __name__=="__main__":
    app.run(debug=True, host=ARGS.ip, port=ARGS.port)

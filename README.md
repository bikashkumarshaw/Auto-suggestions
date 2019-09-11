# Auto-suggestions

#### This service provides auto-suggestions while you type in query.

## Installation guide:

## Clone:
```
git clone https://github.com/bikashkumarshaw/Auto-suggestions
```

## Install Virtual Environment:
```
pip install virtualenv

cd Auto-suggestions

virtualenv -p python3 [environment name eg. env]

source env/bin/activate (env is the name of the environment here. please set according to your environment name)

Now install all the dependencies as listed below
```

## Dependencies:
- pip install -r requirements.txt

## Run command:
```
python auto_suggest.py --es-url `ES url` --es-port `provide the es port` --es-index `provide the es index you created` --ip `ip of the server where the service is running` --port `port for the service --f-name `file containing the word and its occurrences`
```

## API'S supported:

```
search (provides auto-suggestions while you type in query.)
```

## search

#### This API requests Elastic Search with the queried word and returns suggestions by combining results with prefix match and sorted suffix matches with occurrences

### Positional params:

**word:**

* Ref : http://159.69.60.242:3344/api/search?word=the

```jsond
{
suggestions: [
"the",
"thes",
"thew",
"thef",
"thed",
"nthe",
"rthe",
"sthe",
"bthe",
"pthe"
]
}

```

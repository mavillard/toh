import json
import networkx as nx
import urllib2

# Access token
token = 'CAACEdEose0cBAFic3CCIwZAaJ5HVyzRovbqBNmYVD5SX52RMZBNZChgLIIJmK6TkpUYjncL62J3TrJP4tFEGlXu885lZAsnHZCgBFyest49bZAwQFV9OZBpgNvCkLp7BbZBniKhDhcwVCWRakVuVKL2h1OSUDU4UdR2swhZAqrtqXyXZBTcHEsn4nL9yPQeSIIkn0JiZBaXWnT7owZDZD'

# API
api = 'https://graph.facebook.com'

# Action
action = '/me'

# Build query
def q(action):
    query = api + action
    if '?' in query:
        query += '&'
    else:
        query += '?'
    query += 'access_token=' + token
    return query

# URL
url = q(action)

# Operation
response = urllib2.urlopen(url)
content = response.read()
response.close()
data = json.loads(content)

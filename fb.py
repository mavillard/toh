import json
import networkx as nx
import urllib2

# Query
# Access token
token = 'CAACEdEose0cBAOKC0sZBBxxJviYSVTvzz6qVQrPojOzuY3ZCtlFZBLzyZCyvlOJBWMZCO4L8ZCUd30mbVKbej6AZASQAGMeT0YBtcbDyAKEdXe4bfzQFoPdmVdzFWNASrBCrb3E8brLarZAUzJ9x3fY1Csyurpd7YfUAZBqkJ29BjGXSbg3kaDhDZCas5QXHrJYaVKJOiNVZApyLgZDZD'

# API
api = 'https://graph.facebook.com'

# Limit
limit = 25

# Build query
def q(action):
    query = api + action
    if '?' in query:
        query += '&'
    else:
        query += '?'
    query += 'limit=' + str(limit)
    query += '&access_token=' + token
    return query


# FUNCTIONS
# Global var
global_var = {'posts': 0}

def process_posts(posts):
    for post in posts:
        # post info
        ide = post['id']
        message = post.get('message', '')
        info = {
            'type': 'post',
            'message': message
        }
        if not toh.has_node(ide):
            toh.add_node(ide, info)
        # author info
        author_id = post['from']['id']
        if author_id != toh_id:
            author_info = {
                'type': 'user',
                'name': post['from']['name']
            }
            if not toh.has_node(author_id):
                toh.add_node(author_id, author_info)
            if not toh.has_edge(author_id, ide):
                toh.add_edge(author_id, ide, label='posts')
            if not toh.has_edge(author_id, toh_id):
                toh.add_edge(author_id, toh_id, label='likes')
    
    global_var['posts'] += len(posts)
    if global_var['posts'] % 100 == 0:
        print global_var['posts'], 'posts processed...'
    if global_var['posts'] % 1000 == 0:
        nx.write_gexf(toh, 'toh.gexf')

def process_data(data):
    if data['data']:
        process_posts(data['data'])
    if data['paging'] and data['paging']['next']:
        toh_network(data['paging']['next'])

def toh_network(url):
    data = get_data(url)
    process_data(data)

# Get data from url
def get_data(url):
    response = urllib2.urlopen(url)
    content = response.read()
    response.close()
    data = json.loads(content)
    return data


# NETWORK
toh = nx.Graph()

# Central node
action = '/tasteofhome?fields=name'
url = q(action)
data = get_data(url)
ide = data['id']
info = {
    'type': 'toh',
    'name': data['name'],
}
toh.add_node(ide, info)
toh_id = ide

# Network from posts
action = '/tasteofhome/feed'
url = q(action)
toh_network(url)







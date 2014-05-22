import json
import networkx as nx
import os
import time
import urllib2
from datetime import datetime

# QUERY
# Access token
token = '''
CAACEdEose0cBAG3VxO3RCLDYwrqSd57zOO9OoW6GuXM9sYwAnT9uqMXcJSDe5aVMSGXGTmA5hrps9rVhW7srCdUKFSbqjtlezMjRlaQDHGEMplDEZAGWrBluaVodneOdr7bVviXfZA3BSGQI8gWzRK9HPnCx5jSilZCFbjM9ZAficZCmfxsqPZCwFIWZAmZAasGx6all7OitNAZDZD
'''
token = token.strip()

# Api
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


# GLOBAL VARS
global_var = {
    'post_counter': 0,
    'last_date': '',
    'last_year': 0,
    'year': 2014,
}

POSTS = 0
COMMENTS = 1


# FUNCTIONS
# Time functions
def date_to_timestamp(date_str):
    date = datetime.strptime(date_str, "%Y-%m-%d")
    ts = int(time.mktime(date.timetuple()))
    return ts

def get_date(ts_str):
    return ts_str.split('T')[0]

def get_year(date_str):
    return int(date_str.split('-')[0])

# Graph functions
def process_user(user_id, user_name):
    if not toh.has_node(user_id):
        user_info = {
            'name': user_namelast_date,
            'contributions': 1,
        }
        toh.add_node(user_id, user_info)
    else:
        toh.node[user_id]['contributions'] += 1

def process_relation(user_id_1, user_id_2):
    if not toh.has_edge(user_id_1, user_id_2):
        toh.add_edge(user_id_1, user_id_2, grade=1)
    else:
        toh[user_id_1][user_id_2]['grade'] += 1

def process_comments(comments, **extra):
    post_user_id = extra['user']
    for comment in comments:
        user_id = comment['from']['id']
        user_name = comment['from']['name']
        process_user(user_id, user_name)
        process_relation(user_id, post_user_id)

def process_posts(posts):
    created_time = ''
    for post in posts:
        user_id = post['from']['id']
        user_name = post['from']['name']
        process_user(user_id, user_name)
        post_id = post['id']
        post_comments(post_id, user_id)
        
        created_time = post['created_time']
        last_date = get_date(created_time)
        global_var['last_date'] = last_date
        global_var['last_year'] = get_year(last_date)
    
    global_var['post_counter'] += len(posts)
    print global_var['post_counter'], 'posts processed...'
    print 'Last date:', global_var['last_date']
    print 'Users:', len(toh.nodes())
    print 'Relations:', len(toh.edges())
    if global_var['post_counter'] % 1000 == 0:
        nx.write_gexf(toh, 'toh.gexf')
        f = open('last_date.txt', 'w')
        f.write(global_var['last_date'])
        f.close()

# Data processing functions
def process_data(data, result_type, **extra):
    end = False
    if 'data' in data:
        if result_type == POSTS:
            process_posts(data['data'])
            if global_var['year'] != 0:
                end = global_var['last_year'] < global_var['year']
        else: # result_type == COMMENTS:
            process_comments(data['data'], **extra)
    if not end and 'paging' in data and 'next' in data['paging']:
        process_query(data['paging']['next'], result_type, **extra)

def get_data(url):
    response = urllib2.urlopen(url)
    content = response.read()
    response.close()
    data = json.loads(content)
    return data

def process_query(url, result_type, **extra):
    data = get_data(url)
    process_data(data, result_type, **extra)

# Main functions
def post_comments(post_id, user_id):
    action = '/' + post_id + '/comments'
    url = q(action)
    process_query(url, COMMENTS, post=post_id, user=user_id)

def toh_posts():
    action = '/tasteofhome/feed'
    url = q(action)
    process_query(url, POSTS, year=2014)

def toh_posts_ts(ts):
    action = '/tasteofhome/feed?until=' + str(ts)
    url = q(action)
    process_query(url, POSTS, year=2014)


# NETWORK
if os.path.isfile('toh.gexf') and os.path.isfile('last_date.txt'):
    # Recover graph
    toh = nx.read_gexf('toh.gexf')
    # Recover toh id
    action = '/tasteofhome?fields=name'
    url = q(action)
    data = get_data(url)
    toh_id = data['id']
    # Keep processing toh relations
    f = open('last_date.txt')
    last_date = f.read()
    f.close()
    ts = date_to_timestamp(last_date)
#    toh_posts_ts(ts)
else:
    # Graph
    toh = nx.Graph()
    # Add toh node
    action = '/tasteofhome?fields=name'
    url = q(action)
    data = get_data(url)
    toh_id = data['id']
    toh_info = {
        'name': data['name'],
        'contributions': 1,
    }
    toh.add_node(toh_id, toh_info)
    # Process toh relations
#    toh_posts()
nx.write_gexf(toh, 'toh.gexf')












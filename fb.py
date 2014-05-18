import json
import networkx as nx
import urllib2

# QUERY
# Access token
token = 'CAACEdEose0cBAAroE8TmmEIZB1PJZBchts1SLdgrVfWTIFfDjWr37q7htQLsuRXFAiDe1SqFzAkKNscQQEc53jpizC0L8NxZCXCXWtQlyjwfcJubcr9xuYDFqmTxosXjtzFfaYtSPpb4WEqaMrq1OTeZAD1ajRZCv0w3aluZCGd2a4NX6TP0N8etvkluBAINI9sGZB9l0EPZAQZDZD'

# Api
api = 'https://graph.facebook.com'

# Limit
limit = 100

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
global_var = {'post_counter': 0}

POSTS = 0
LIKES = 1
SHARES = 2
COMMENTS = 3


# FUNCTIONS
def post_likes(post_id):
    action = '/tasteofhome/' + post_id + '/likes'
    url = q(action)
    likes_network(url)

def post_shares(post_id):
    action = '/tasteofhome/' + post_id + '/sharedposts'
    url = q(action)
    shares_network(url)

def post_comments(post_id):
    action = '/tasteofhome/' + post_id + '/comments'
    url = q(action)
    comments_network(url)

def process_posts(posts):
    for post in posts:
        # author info
        author_id = post['from']['id']
        if author_id != toh_id:
            author_info = {
                'type': 'user',
                'name': post['from']['name']
            }
            if not toh.has_node(author_id):
                toh.add_node(author_id, author_info)
                toh.add_edge(author_id, toh_id, label='likes')
        # post info
        ide = post['id']
        message = post.get('message', '')
        info = {
            'type': 'post',
            'message': message
        }
        if not toh.has_node(ide):
            toh.add_node(ide, info)
            toh.add_edge(author_id, ide, label='posts')
        # post actions
        post_likes(ide)
        post_shares(ide)
        post_comments(ide)
    
    global_var['post_counter'] += len(posts)
    if global_var['post_counter'] % 100 == 0:
        print global_var['post_counter'], 'posts processed...'
    if global_var['post_counter'] % 1000 == 0:
        nx.write_gexf(toh, 'toh.gexf')

def process_data(data, result_type):
    if data['data']:
        if result_type == POSTS:
            process_posts(data['data'])
        elif result_type == LIKES:
            process_likes(data['data'])
        elif result_type == SHARES:
            process_shares(data['data'])
        else: # result_type == COMMENTS:
            process_comments(data['data'])
    if data['paging'] and data['paging']['next']:
        process_query(data['paging']['next'], result_type)

def get_data(url):
    response = urllib2.urlopen(url)
    content = response.read()
    response.close()
    data = json.loads(content)
    return data

def process_query(url, result_type):
    data = get_data(url)
    process_data(data, result_type)

def comments_network(url)
    process_query(url, COMMENTS)

def shares_network(url)
    process_query(url, SHARES)

def likes_network(url)
    process_query(url, LIKES)

def toh_network(url)
    process_query(url, POSTS)


# NETWORK
#Graph
toh = nx.Graph()

# Central node
action = '/tasteofhome?fields=name'
url = q(action)
data = get_data(url)
ide = data['id']
info = {
    'type': 'toh',
    'name': data['name'],
    'location': data['location']['city']
}
toh.add_node(ide, info)
toh_id = ide

# Network
action = '/tasteofhome/feed'
url = q(action)
toh_network(url)







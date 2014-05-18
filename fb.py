import json
import networkx as nx
import urllib2

# QUERY
# Access token
token = 'CAACEdEose0cBAHqbPZBjrDk1JqPgcTYozRIZBzfv9JPDkHLxQBBnvuGaL3ms06jY1lMN9oVaJeJZBE4J8ixOfSx4O1ZBdpCZATIcrlNHMMPAd4SyZBHkLfNRgH031pSxjVT08eaLdDe2OoFrzu42JZBfEzuVRZBUSnSfYK45JzdJy33X8OJiYZAZAAZCYbzqUcZBxYliYply0t2GRwZDZD'

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
# Graph functions
def process_shares(shares, **extra):
    print shares
    print 'sddasdasd'
    post_id = extra['post']
    post_user_id = extra['user']
    for share in shares:
        print share

def process_likes(likes, **extra):
    post_id = extra['post']
    post_user_id = extra['user']
    for like in likes:
        user_id = like['id']
        if not toh.has_node(user_id):
            user_info = {
                'type': 'user',
                'name': like['name']
            }
            toh.add_node(user_id, user_info)
            toh.add_edge(user_id, toh_id, label='is_member_of')
        toh.add_edge(user_id, post_id, label='likes')
        toh.add_edge(user_id, post_user_id, label='is_friend_of')

def process_posts(posts):
    for post in posts:
        # user info
        user_id = post['from']['id']
        if not toh.has_node(user_id):
            user_info = {
                'type': 'user',
                'name': post['from']['name']
            }
            toh.add_node(user_id, user_info)
            toh.add_edge(user_id, toh_id, label='is_member_of')
        # post info
        post_id = post['id']
        post_info = {
            'type': 'post',
            'message': post.get('message', '')
        }
        toh.add_node(post_id, post_info)
        toh.add_edge(user_id, post_id, label='posts')
        # post actions: likes, shares, comments
        #post_likes(post_id, user_id)
        post_shares(post_id, user_id)
#        comment_users = post_comments(post_id, user_id)
    
    global_var['post_counter'] += len(posts)
    if global_var['post_counter'] % 100 == 0:
        print global_var['post_counter'], 'posts processed...'
    if global_var['post_counter'] % 1000 == 0:
        nx.write_gexf(toh, 'toh.gexf')

# Data processing functions
def process_data(data, result_type, **extra):
    if 'data' in data:
        if result_type == POSTS:
            process_posts(data['data'])
        elif result_type == LIKES:
            process_likes(data['data'], **extra)
        elif result_type == SHARES:
            process_shares(data['data'], **extra)
        else: # result_type == COMMENTS:
            process_comments(data['data'], **extra)
    if 'paging' in data and 'next' in data['paging']:
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

def post_shares(post_id, user_id):
    action = '/' + post_id + '/sharedposts'
    url = q(action)
    process_query(url, SHARES, post=post_id, user=user_id)

def post_likes(post_id, user_id):
    print 'post_likes'
    action = '/' + post_id + '/likes'
    url = q(action)
    process_query(url, LIKES, post=post_id, user=user_id)

def toh_posts():
    action = '/tasteofhome/feed'
    url = q(action)
    process_query(url, POSTS)


# NETWORK
# Graph
toh = nx.Graph()

# Add toh node
action = '/tasteofhome?fields=name'
url = q(action)
data = get_data(url)
toh_id = data['id']
toh_info = {
    'type': 'toh',
    'name': data['name'],
}
toh.add_node(toh_id, toh_info)

# Process toh relations
toh_posts()






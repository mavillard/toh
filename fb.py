import json
import networkx as nx
import os
import time
import urllib2
from datetime import datetime

# QUERY
# Access token
token = '''
CAACEdEose0cBAJme0PpRaYRIWZAGqMGYZAUrJOv4CLv76OnCwUMUoeE7vt8fYdrUi3Q52GY4PWrwyBHZCtIE1wOTMIkI07TZCJj8qCt1OxxnAqyfV92Fw4hwmZCVw8B2SEoDMA0g8481ju0AX4YdE0ZC37LMUfB5jZAs7XJzyTXYiZBTCtkXZAvzIyRn30UgkrsBunlQgReU76wZDZD
'''
token = token.strip()

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
global_var = {
    'post_counter': 0,
    'data_accepted': 0,
    'data_rejected': 0,
    'percentage_rejected': 0.0,
}

POSTS = 0
COMMENTS = 1


# FUNCTIONS
# Coding functions
def check_coding(text):
    result = ''
    try:
        result = str(text)
        global_var['data_accepted'] += 1
    except:
        global_var['data_rejected'] += 1
    finally:
        global_var['percentage_rejected'] = global_var['data_rejected'] * 100 \
            / float(global_var['data_accepted'] + global_var['data_rejected'])
    return result

# Timestamp functions
def previous_day_oldest_date(toh):
    nodes = toh.nodes(data=True)
    posts = filter(lambda x: 'time' in x[1], nodes)
    ordered_posts = sorted(posts, key=lambda x: x[1]['time'])
    i = 0
    oldest_date = ordered_posts[i][1]['time']
    oldest_date_str = oldest_date.split('T')[0]
    oldest_date_previous_day = ordered_posts[i + 1][1]['time']
    oldest_date_previous_day_str = oldest_date_previous_day.split('T')[0]
    while oldest_date_str == oldest_date_previous_day_str:
        oldest_date = ordered_posts[i][1]['time']
        oldest_date_str = oldest_date.split('T')[0]
        oldest_date_previous_day = ordered_posts[i + 1][1]['time']
        oldest_date_previous_day_str = oldest_date_previous_day.split('T')[0]
        i += 1
    oldest_date_datetime = datetime.strptime(
        oldest_date_previous_day_str,
        "%Y-%m-%d"
    )
    ts = int(time.mktime(oldest_date_datetime.timetuple()))
    print 'Recovering posts from', oldest_date_previous_day_str
    return ts

# Graph functions
def process_comments(comments, **extra):
    post_id = extra['post']
    post_user_id = extra['user']
    for comment in comments:
        # user info
        user_id = comment['from']['id']
        if not toh.has_node(user_id):
            user_info = {
                'type': 'user',
                'name': check_coding(comment['from']['name'])
            }
            toh.add_node(user_id, user_info)
            toh.add_edge(user_id, toh_id, label='is_member_of')
            toh.add_edge(user_id, post_user_id, label='is_friend_of')
        # comment info
        comment_id = comment['id']
        comment_info = {
            'type': 'post',
            'message': check_coding(comment.get('message', u'')),
            'time': comment.get('created_time', u''),
        }
        toh.add_node(comment_id, comment_info)
        toh.add_edge(user_id, comment_id, label='posts')
        toh.add_edge(comment_id, post_id, label='is_comment_of')

def process_posts(posts):
    for post in posts:
        # user info
        user_id = post['from']['id']
        if not toh.has_node(user_id):
            user_info = {
                'type': 'user',
                'name': check_coding(post['from']['name'])
            }
            toh.add_node(user_id, user_info)
            toh.add_edge(user_id, toh_id, label='is_member_of')
        # post info
        post_id = post['id']
        post_info = {
            'type': 'post',
            'message': check_coding(post.get('message', u'')),
            'time': post.get('created_time', u''),
        }
        toh.add_node(post_id, post_info)
        toh.add_edge(user_id, post_id, label='posts')
        # post comments
        post_comments(post_id, user_id)
    
    global_var['post_counter'] += len(posts)
    if global_var['post_counter'] % 100 == 0:
        print global_var['post_counter'], 'posts processed...'
        print global_var['percentage_rejected'], '% of data rejected...'
        print 'Last date:', post_info['time']
    if global_var['post_counter'] % 1000 == 0:
        nx.write_gexf(toh, 'toh.gexf')

# Data processing functions
def process_data(data, result_type, **extra):
    if 'data' in data:
        if result_type == POSTS:
            process_posts(data['data'])
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

def toh_posts():
    action = '/tasteofhome/feed'
    url = q(action)
    process_query(url, POSTS)

def toh_posts_ts(ts):
    action = '/tasteofhome/feed?until=' + str(ts)
    url = q(action)
    process_query(url, POSTS)


# NETWORK
if os.path.isfile('toh.gexf'):
    # Recover graph
    toh = nx.read_gexf('toh.gexf')
    # Recover toh id
    action = '/tasteofhome?fields=name'
    url = q(action)
    data = get_data(url)
    toh_id = data['id']
    # Keep processing toh relations
    ts = oldest_time(toh)
    toh_posts_ts(ts)
else:
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













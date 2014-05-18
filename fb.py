import json
import networkx as nx
import urllib2

# Access token
token = 'CAACEdEose0cBAKvE4ANEG6InnkhpZAaiPzWWjZBHAUse2ytZAJaXQbbHnKn3UUNLJevEKx8uFT5BmZB4dDAuu8KWA0xd1Gq48ciwFIg10BfvbPq32G5Uw4ZCeUcUz6JQ3u9JVq9puZAhQKKeEjtE51FONEJCNgrlmV4NmAG6FgtPRj2ce1WUuY06UHtRC0MLy1OUCG41BzCQZDZD'

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


# Network
def toh_network():
    action = '/tasteofhome/feed'
    url = q(action)
    response = urllib2.urlopen(url)
    content = response.read()
    response.close()
    data = json.loads(content)
    process_data(data)

# Process data
def process_data(data):
    if data['data']:
        process_posts(data['data'])
    if data['paging']:
        pass #while

# Process posts
def process_posts(posts):
    for post in posts:
        print 'author:', post['from']['name']
        print '---'




import json
import urllib2

# Input
token = 'CAACEdEose0cBAIva2Ef6o27r3Xjj04cxQSiAznzdYzw8fCmgnp0JsalR41WZCCHqxbODyZCMMw0txodsLvYZAYY2Vd56ZATIYKGQIbgC7CZAg4GRvCD8zKI3727bQv5AZA5V4PhnZCamYfd8ie9N7TXXiy2KZCfbi8Hv1N7ejwSxqzcOpS7FStoSFOrqxAhXMHfvrbbSydI6gQZDZD'

action = '/me'
fields = ''

metadata = '1'

# API
api = 'https://graph.facebook.com'

# Action
act = action

# Fields
flds = '?fields=' + fields

# Metadata
mtdt = '&metadata=' + metadata

# Access
access = '&access_token=' + token

# Operation
url = api + act + flds + mtdt + access
response = urllib2.urlopen(url)
content = response.read()
data = json.loads(content)
print data
response.close()

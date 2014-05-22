import networkx as nx

# Graph
toh = nx.read_gexf('toh.gexf')
nodes = toh.nodes(data=True)
edges = toh.edges(data=True)

# Number of samples
n = 10

# Degrees
degrees = nx.degree(toh)
s_degrees = sorted(degrees.items(), key=lambda x: x[1], reverse=True)
s_degrees = s_degrees[:n]

# Contributions
s_contribs = sorted(nodes, key=lambda x: x[1]['contributions'], reverse=True)
s_contribs = s_contribs[:n]

# Relation grades
s_grades = sorted(edges, key=lambda x: x[2]['grade'], reverse=True)
s_grades = s_grades[:n]

# Relating metrics
import operator

toh_id = '61511025427'

print 'Top nodes by degree'
print '-' * 79
for node, degree in s_degrees:
    print 'NODE:', node
    print 'name:', toh.node[node]['name']
    print 'degree:', degree
    print 'contributions:', toh.node[node]['contributions']
    print 'greatest grade:', sorted(toh[node].iteritems(), key=operator.itemgetter(1), reverse=True)[0]
    print '-' * 79
print '=' * 79

print 'Top nodes by contribution'
print '-' * 79
for node, attrs in s_contribs:
    print 'NODE:', node
    print 'name:', toh.node[node]['name']
    print 'degree:', toh.degree(node)
    print 'contributions:', attrs['contributions']
    print 'greatest grade:', sorted(toh[node].iteritems(), key=operator.itemgetter(1), reverse=True)[0]
    print '-' * 79
print '=' * 79

node = toh_id
print 'Top nodes by relation grades'
print '-' * 79
print 'NODE:', node
print 'name:', toh.node[node]['name']
print 'degree:', toh.degree(node)
print 'contributions:', toh.node[node]['contributions']
print 'greatest grade:', sorted(toh[node].iteritems(), key=operator.itemgetter(1), reverse=True)[0]
print '-' * 79
for node1, node2, relations in s_grades[:n-1]:
    if node1 == toh_id:
        node = node2
    else:
        node = node1
    print 'NODE:', node
    print 'name:', toh.node[node]['name']
    print 'degree:', toh.degree(node)
    print 'contributions:', toh.node[node]['contributions']
    print 'greatest grade:', sorted(toh[node].iteritems(), key=operator.itemgetter(1), reverse=True)[0]
    print '-' * 79
print '=' * 79

# Degree centrality
degree_c = nx.degree_centrality(toh)
s_degree_c = sorted(degree_c.items(), key=lambda x: x[1], reverse=True)
s_degree_c = s_degree_c[:n]

# Betweenness centrality
#betweenness_c = nx.betweenness_centrality(toh)
#s_betweenness_c = sorted(betweenness_c.items(), key=lambda x: x[1], reverse=True)
#s_betweenness_c = s_betweenness_c[:n]



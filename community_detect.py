import networkx as nx
import community as community_louvain  # pip install python-louvain
import matplotlib.pyplot as plt

# Load graph
G = nx.read_gml("user_user_projected_graph.gml")

# Detect communities using Louvain method
partition = community_louvain.best_partition(G, weight='weight')

# Add community ID to each node
nx.set_node_attributes(G, partition, 'community')

# Optionally, save new graph with communities
nx.write_gml(G, "user_user_with_communities.gml")


import pandas as pd
import networkx as nx
from networkx.algorithms import bipartite

# Load nodes and edges
nodes_df = pd.read_csv("nodes.csv")   # Columns: 'Id', 'Label', 'Type', etc.
edges_df = pd.read_csv("edges.csv")   # Columns: 'Source' (user), 'Target' (problem)

# Create bipartite graph
B = nx.Graph()

# Add nodes with bipartite attribute
for _, row in nodes_df.iterrows():
    B.add_node(row['Id'], bipartite=row['Type'], rating=row['Rating'], tags=row['Tags'])

# Add edges (user → problem)
for _, row in edges_df.iterrows():
    B.add_edge(row['Source'], row['Target'])

# Get user and problem node sets
users = {n for n, d in B.nodes(data=True) if d["bipartite"] == "User"}

# Project bipartite graph to user-user graph based on shared problems
user_user_graph = bipartite.weighted_projected_graph(B, users)

# Optional: Filter weak links (e.g., shared ≥ 3 problems)
threshold = 3
filtered_graph = nx.Graph()
for u, v, data in user_user_graph.edges(data=True):
    if data["weight"] >= threshold:
        filtered_graph.add_edge(u, v, weight=data["weight"])

# Save as .gml file (for Gephi or other graph tools)
nx.write_gml(filtered_graph, "user_user_projected_graph.gml")
print("✅ User-user projected graph saved as 'user_user_projected_graph.gml'")


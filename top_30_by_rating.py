import networkx as nx
import pandas as pd
import sys

rating = int(sys.argv[1]) 

#Load data
nodes = pd.read_csv("nodes.csv")
edges = pd.read_csv("edges.csv")


problem_nodes = nodes[(nodes["Type"] == "Problem") & (nodes["Rating"] == rating)]["Id"]


B = nx.Graph()
B.add_nodes_from(nodes["Id"])
B.add_edges_from(zip(edges["Source"], edges["Target"]))

#Degree Centrality
centrality = nx.degree_centrality(B)
filtered_centrality = {node: centrality[node] for node in problem_nodes}

#Top 30 problems by rating
top_rated_problems = sorted(filtered_centrality.items(), key=lambda x: x[1], reverse=True)[:30]
df = pd.DataFrame(top_rated_problems, columns=["Problem", "PopularityScore"])
df.to_csv(f"top_30_rating_{rating}.csv", index=False)
print(f"Saved to top_30_rating_{rating}.csv")


import networkx as nx
import pandas as pd
import sys

tag = sys.argv[1] 

#Load data
nodes = pd.read_csv("nodes.csv")
edges = pd.read_csv("edges.csv")

problem_nodes = nodes[(nodes["Type"] == "Problem") & (nodes["Tags"].str.contains(tag, case=False, na=False))]["Id"]

B = nx.Graph()
B.add_nodes_from(nodes["Id"])
B.add_edges_from(zip(edges["Source"], edges["Target"]))

#Degree centrality
centrality = nx.degree_centrality(B)
filtered_centrality = {node: centrality[node] for node in problem_nodes}

#Top 50 topic problems
top_topic_problems = sorted(filtered_centrality.items(), key=lambda x: x[1], reverse=True)[:50]
df = pd.DataFrame(top_topic_problems, columns=["Problem", "PopularityScore"])
df.to_csv(f"top_50_{tag.lower()}_problems.csv", index=False)
print(f"Saved to top_50_{tag.lower()}_problems.csv")


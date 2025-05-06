import networkx as nx
import pandas as pd

#Load data
nodes = pd.read_csv("nodes.csv")
edges = pd.read_csv("edges.csv")

B = nx.Graph()
B.add_nodes_from(nodes["Id"])
B.add_edges_from(zip(edges["Source"], edges["Target"]))


problem_nodes = nodes[nodes["Type"] == "Problem"]["Id"]

#Degree centrality
centrality = nx.degree_centrality(B)
problem_centrality = {node: centrality[node] for node in problem_nodes}

#Top 50 must-solve problems
top_problems = sorted(problem_centrality.items(), key=lambda x: x[1], reverse=True)[:50]
df = pd.DataFrame(top_problems, columns=["Problem", "PopularityScore"])
df.to_csv("top_50_must_solve.csv", index=False)
print("Top 50 must-solve problems saved to top_50_must_solve.csv")


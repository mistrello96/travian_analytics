import networkx as nx
import sys
import pandas as pd
import matplotlib.pyplot as plt

file = sys.argv[1]

G = nx.read_graphml(file)

nx.draw_spring(G, arrowsize=2, with_labels=False, node_size=50)
plt.savefig("spring.png")
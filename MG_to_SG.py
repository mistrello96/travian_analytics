import networkx as nx
import sys
from MG_to_SG_function import MG_to_SG

file = sys.argv[1]

M = nx.read_edgelist(file, comments='#', delimiter=',', create_using=nx.MultiDiGraph, data = [('type', str), ('weight',int), ('timestamp', int)])
G = MG_to_SG(M)

nx.write_graphml(M, "./MG.graphml")
nx.write_graphml(G, "./SG.graphml")
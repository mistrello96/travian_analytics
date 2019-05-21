import pandas as pd
import sys

# Not tested yet, but it should work

file = sys.argv[1]
edge_type = sys.argv[2]
attributes = [a for a in sys.argv[3:]]

pd.read_csv(file, header = None, names = attributes)
df = df.assign(type = edge_type)
df.to_csv(file, index = False)
import pandas as pd
import sys

# Not tested yet, but it should work

# Please, do note that this method overrides the
# original file

file = sys.argv[1]
edge_value = sys.argv[2]
header = sys.argv[3]
attributes = [a for a in sys.argv[4:]]
df = pd.DataFrame()
if header:
	df = pd.read_csv(file)
else:
	df = pd.read_csv(file, header = header, names = attributes)
df = df.assign(weight = edge_value)
df.to_csv(file, index = False)
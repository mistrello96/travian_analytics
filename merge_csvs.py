import pandas as pd
import sys
from os import walk

# this is an example of execution of the script:
# 1. the directory of the .csv files to merge
# 2. the path where the .csv file has to be saved
# 3. the type of the edges in the files
# 4. a sequence of the names of the columns
# python3 preprocessing.py "./datas_paper/Dataset/trade-csv/"  "./datas_paper/Dataset/trade-csv/messages.csv" "trade" timestamp sender receiver

path = sys.argv[1]
save_path = sys.argv[2]
attributes = [a for a in sys.argv[3:]]

dir_files = []
for (_, _, filenames) in walk(path):
    dir_files.extend(filenames)
    break
all_files = [path + f for f in dir_files]

df = pd.concat((pd.read_csv(f, header = None, names = attributes) for f in all_files))
df.to_csv(save_path, index = False)
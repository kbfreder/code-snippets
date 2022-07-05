import sys, os
import pandas as pd

# ------------------------------
# OPTIONS
# ------------------------------

pd.set_option("display.max_columns", 100)

# to silence the 'Setting with Copy' (??) warning
pd.options.mode.chained_assignment = None

# if tab auto-complete isn't working in Jupyter
%config Completer.use_jedi = False


# ignore other warnings
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)


# to flatten a nested list:
flat_list = [item for sublist in nested_list for item in sublist]
# alt:
import itertools
list2d = [[1,2,3], [4,5,6], [7], [8,9]]
merged = list(itertools.chain(*list2d))



# Dataframes

## differences between two
(there is a function)

## concat a list of df's into a single df

df_list = [df1, df2, ...]
final_df = pd.concat(df_list)



# flatten a list 
flat_list = [item for sublist in t for item in sublist]
reduce(lambda a, b: a + b, l)

# ------------------------------
# SHOWING PROGRESS
# ------------------------------

# using `tqdm:`
from tqdm import tqdm

for item in tqdm(
    iter_list,
    "Action word: ",
    unit=" files",
):
...

# manually
chunk_size = 100
total_size = len(item_list)
for i, item in item_list:
    # do things with item
    if (i != 0) & (i % chunk_size == 0):
        print(f"Progress: {i/total_size * 100:.0f}%")


import time
import sys

for i in range(100):
    time.sleep(0.1)
    sys.stdout.write("\r%d%%" % i)
    sys.stdout.flush()


import sys


def progress(count, total, suffix=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', suffix))
    sys.stdout.flush()  # As suggested by Rom Rube


# ------------------------------
# PATHS
# ------------------------------

import os

for root, dirs, files in os.walk(dir_path):
    for f in files:
        print(f"File path: {os.path.join(root, f)}")
import sys, os
import pandas as pd

# ------------------------------
# OPTIONS
# ------------------------------

pd.set_option("display.max_columns", 100)

# to silence the 'Settings with Copy' warning
pd.options.mode.chained_assignment = None

# if tab auto-complete isn't working in Jupyter
%config Completer.use_jedi = False


# ignore other warnings
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

# divide by zero errors ("RuntimeWarning: invalid value encountered in true_divide")
np.seterr(invalid='ignore')


# ------------------------------
# MISC
# ------------------------------

# to flatten a nested list:
flat_list = [item for sublist in nested_list for item in sublist]
# alt:
import itertools
list2d = [[1,2,3], [4,5,6], [7], [8,9]]
merged = list(itertools.chain(*list2d))



# ------------------------------
# Dataframes
# ------------------------------

## differences between two
(there is a function)

## concat a list of df's into a single df
df_list = [df1, df2, ...]
final_df = pd.concat(df_list)


# reduce a list via a join:
from functools import reduce
df_joined = reduce(lambda df1, df2: df1.join(df2, on='key'), df_list)


## concat 2 df's horizontally (combining columns)
    ## when you know the indexes are aligned, but they aren't equal
    ## Ref: https://github.com/pandas-dev/pandas/issues/25349
    ## Note we reset_index, instead of using ignore_index=True
new_df = pd.concat([df.reset_index(drop=True), scaled_df.reset_index(drop=True)], axis=1, sort=False)



# apply a function across a row:

def func(row):
    # ostensibily this is something more complex, but you get the idea
    return row['A'] * row['B'] + row['C']

## note axis=1, even though we're doing this for every row. Don't ask me why
df['new_col'] = df.apply(func, axis=1)

# ------------------------------
# MISC
# ------------------------------

# flatten a list 
flat_list = [item for sublist in nested_list for item in sublist]
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
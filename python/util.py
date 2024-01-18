import pickle
import numpy as np
import pandas as pd
import datetime as dt
from dateutil.relativedelta import relativedelta as rd
from calendar import monthrange as mr
import random
import subprocess
import sys
from collections import deque

import logging

def configure_logger(logger_name, log_level, log_file=None):
    """Configures a python logger object

    logger_name: string
    log_level: a logging.<LEVEL> object
    log_file: file path. supply if you wish to include a file handler
    """
    # print(f'Log file passed in arguments: {log_file}')

    # logging formatting
    msg_fmt = '%(asctime)s - %(filename)s - %(message)s'
    date_fmt = '%Y-%m-%d %H:%M'

    basic_format = {'format': msg_fmt, 'datefmt': date_fmt}
    fmtr_format = {'fmt': msg_fmt, 'datefmt': date_fmt}

    logging.basicConfig(level=log_level, **basic_format)
    logger = logging.getLogger(logger_name)

    if log_file:
        f_handler = logging.FileHandler(log_file)
        f_handler.setLevel(logging.INFO)
        f_handler.setFormatter(logging.Formatter(**fmtr_format))
        logger.addHandler(f_handler)

    return logger

# --------------------------------------------------------------------
# MISC 

def num_not_zero(data):
    return len(data[data != 0])

def num_pos(data):
    return len(data[data > 0])

def trimmed_mean(data, ptile=95):
    cutoff = np.percentile(data, ptile)
    trimmed_data = data[data <= cutoff].dropna()
    return np.mean(trimmed_data)

def check_dup_cols(df, col_name, suffixes):
    col_sfx_1 = col_name + suffixes[0]
    col_sfx_2 = col_name + suffixes[1]

    check = np.sum(df[col_sfx_1] == df[col_sfx_2]) == len(df)
    print(check)
    if not check:
        return df[df[col_sfx_1] != df[col_sfx_2]][[col_sfx_1, col_sfx_2]]


def df_rel_lens(df1, df2):
    """Relative length of df1 / df2"""
    return len(df1), len(df2), len(df1)/len(df2)


def flatten_list(nested_list):
    return [x for y in nested_list for x in y]

def explode_df_col(df, col_name):
    """Explode df column 'col_name', which is a list, into rows. 
    Returns df with one row per list value

    Ex: 
        >>> df
        id    list_col
        0     [a, b]
        1     [c]
        
        >>> explode_df_col(df, 'list_col')
        id    list_col
        0     a
        0     b
        1     c
        
    """
    temp = df[col_name].apply(pd.Series) \
        .merge(df, left_index=True, right_index=True) \
        .drop(columns=[col_name]) \
        .reset_index(drop=False)
    merge_cols = temp.columns
    num_cols = [x for x in merge_cols if isinstance(x, int)]
    other_cols = [x for x in merge_cols if not isinstance(x, int)]
    temp2 = temp \
        .melt(id_vars=other_cols, value_name=col_name) \
        .drop(columns=['variable', 'index']) \
        .dropna()
    return temp2

# --------------------------------------------------------------------
# DATES 
# --------------------------------------------------------------------

def date_months_prior(n):
        '''Return datetime object x months prior from today
        rounded to first day of month'''
        t = dt.datetime.today()
        exact_dt = t - rd(months=n)
        return dt.datetime(exact_dt.year, exact_dt.month, 1)


def last_months_last_day():
        '''Return datetime object for last day of previous month
        
                Ex: today = 2019-06-15
                
                last_months_last_day()
                >>> Timestamp (2019, 5, 31)
        '''
        t = dt.datetime.today()
        m = t.month
        y = t.year
        if m == 1:
                y -= 1
                m = 12
        else:
                m -= 1
        
        d = mr(y, m)[1]

        return dt.datetime(y, m, d)

    
def get_dates_from_yesterday(n_days, date_format='string'):
    """Return dates for yesterday & yesterday minus n_days
    
    Paramters:
    -----------
    n_days : int
        number of days prior to yesterday to set start date
    
    format : {'string', 'datetime'} optional
        format in which to return dates. options: string, 
    
    Returns:
    -------
    start_date : str or datetime
    end_date: str or datetime
    
    
    Ex: today = 2019-06-15
    
    >>> in: get_dates_from_yesterday(1)
    '2019-06-13', '2019-06-14'
    
    
    Ex: today = 2020-01-02
    
    >>> get_dates_from_yesterday(7, 'datetime')
    datetime.date(2019, 12, 25), datetime.date(2020, 1, 22)
    """
    assert date_format in ['string', 'datetime'], 'Incorrect value provided for `date_format`'
    
    yesterday = dt.date.today() - dt.timedelta(days=1) # this is yesterday
    yesterday_str = yesterday.strftime('%Y-%m-%d')
    start_date = yesterday - dt.timedelta(days=n_days)
    start_date_str = start_date.strftime('%Y-%m-%d')
    
    if date_format == 'string':
        return start_date_str, yesterday_str
    else:
        return start_date, yesterday


def get_start_end_dates(n_days, end_ind, date_format='string'):
    """Return start & end dates 
    
    Paramters:
    -----------
    n_days : int
        number of days prior to end date to set start date
    
    end_ind : int {0, 1}
        the number of days from today to set end date
        i.e. today = 0, yesterday = 1

    format : {'string', 'datetime'} optional
        format in which to return dates. options: string, 
    
    Returns:
    -------
    start_date : str or datetime
    end_date: str or datetime
    
    -----------
    Ex: today = 2019-06-15
    
    >>> in: get_start_end_dates(1,0)
    '2019-06-14', '2019-06-15'
    
    
    Ex: today = 2020-01-02
    
    >>> get_start_end_dates(7, 1, 'datetime')
    datetime.date(2019, 12, 25), datetime.date(2020, 1, 01)
    """
    assert date_format in ['string', 'datetime'], 'Incorrect value provided for `date_format`'
    
    end_dt = dt.date.today() - dt.timedelta(days=end_ind) # this is yesterday
    end_str = end_dt.strftime('%Y-%m-%d')
    start_dt = end_dt - dt.timedelta(days=n_days)
    start_str = start_dt.strftime('%Y-%m-%d')
    
    if date_format == 'string':
        return start_str, end_str
    elif date_format == 'datetime':
        return start_dt, end_dt



def date_to_str(d):
    return d.strftime('%Y-%m-%d')

def gen_date_pairs(n):
    '''Generate date-string pairs spanning done day (ex: ['2020-02-09', '2020-02-10'])
    going back n days from today.
    
    n : number of days prior to today from which to start date-pair list
    
    returns: list of date-pairs, which are themselves a list
    '''
    
    today = dt.datetime.today()
    date_pairs = []
    
    for i in range(n, 0, -1):
        start = today - dt.timedelta(days=i)
        end = start + dt.timedelta(days=1)
        date_pairs.append([date_to_str(start), date_to_str(end)])
    
    return date_pairs

        
# EXPLORING DATAFRAMES ---------------------------------------------------------

def find_val_in_df(val, df):
        '''Return name(s) of column(s) in 'df' in which 'val' is found'''

        for col in list(df.columns):
                if val in list(df[col].unique()):
                        print(col)


def compare_dfs(df1, df2):
    '''Returns DataFrame listing differences (by index & column) between df1 & df2
    Note: df1 & df2 must share the same index.
    '''
    # fillna's to aid in comparison (otherwise nulls return error?)
    df1 = df1.fillna('none specified')
    df2 = df2.fillna('none specified')

    # which entries have changed
    ne_stack = (df1 != df2).stack()
    changed = ne_stack[ne_stack]
    changed.index.names = ['IDX', 'COL']

    diff_idx = np.where(df1 != df2)

    chg_from = df1.values[diff_idx]
    chg_to = df2.values[diff_idx]
    res = pd.DataFrame({'from (df1)': chg_from, 'to (df2)': chg_to}, index=changed.index)

    return res


def check_for_nulls(df):
    '''Return a DataFrame listing columns in df that contain nulls, and the # of nulls'''
    n = df.shape[0]
    null_dict = {}
    for col in list(df.columns):
        if df[col].isnull().any():
            num_null = np.sum(df[col].isnull())
            null_dict[col] = [num_null, np.round(((num_null/n) * 100), 1)]
    
    if len(null_dict) > 0:
        null_df = pd.DataFrame.from_dict(null_dict, orient='index')
        null_df.reset_index(inplace=True)
        null_df.columns = ['Column', 'Num Nulls', '% Null']
        null_df.sort_values(by='Column', inplace=True)
    else:
        null_df = pd.DataFrame()

    return null_df


def null_report(df):
    '''Return a DataFrame listing the # of nulls in each column in df'''
    n = df.shape[0]
    null_dict = {}
    idx = 0
    for col in list(df.columns):
        num_null = np.sum(df[col].isnull())
        null_dict[idx] = [col, num_null, np.round((num_null/n), 4)]
        idx += 1
    
    if len(null_dict) > 0:
        null_df = pd.DataFrame.from_dict(null_dict, orient='index')
        null_df.reset_index(inplace=True)
        null_df.columns = ['Index', 'Column', 'Num Nulls', '% Null']
        null_df.sort_values(by='Index', inplace=True)
    else:
        null_df = pd.DataFrame()

    return null_df


def check_for_inf(df):
    '''Return a DataFrame listing columns in df that contain +inf or -inf, 
        and the # of such records'''
    n = df.shape[0]
    null_dict = {}
    for col in list(df.columns):
        col_inf = df[col].isin([np.inf, -np.inf])
        if col_inf.any():
            num_null = np.sum(col_inf)
            null_dict[col] = [num_null, np.round(((num_null/n) * 100), 1)]
    
    if len(null_dict) > 0:
        null_df = pd.DataFrame.from_dict(null_dict, orient='index')
        null_df.reset_index(inplace=True)
        null_df.columns = ['Column', 'Num Inf', '% Inf']
        null_df.sort_values(by='Column', inplace=True)
    else:
        null_df = pd.DataFrame()

    return null_df

def write_to_excel(filename, df1, sheetname1, index_bool1, *args):
    '''Write df(s) to Excel

    filename: Name of Excel file to save as.
              do not include path (../../reports) or file extension (.xlsx)

    df1 will be saved as Sheet sheetname 1. index_bool indicates whether to include Index
    
    optional: additional df, sheetnames, index_bool to write to Excel file
              (provide as list)

    Ex: 
        write_to_excel('report', summary_df, 'Summary', True, comparison_report, 'Report', False)
    '''
    assert (len(args) - 1) // 3 == 1
        
    with pd.ExcelWriter('../../reports/' + filename + '.xlsx') as writer:
        df1.to_excel(writer, sheet_name=sheetname1, index=index_bool1)  
        if len(args) > 0:
            triplets = list(zip(*[args[i::3] for i in range(3)]))
            
            for t in triplets:
                dfx = t[0]
                sheetnamex = t[1]
                index_boolx = t[2]
                dfx.to_excel(writer, sheet_name=sheetnamex, index=index_boolx)


def get_project_path():
    '''Return path of project folder
        assuming cookiecutter structure, this is two folders "up"
    
    Note, calling notebook must have run `import os`
    '''
    import os
    return os.path.dirname(os.path.dirname(os.path.abspath(os.path.curdir)))


def get_save_path():
    import os

    # set save path for queries
    cwd = os.getcwd()
    if '/' in cwd:
        char = '/'
    else:
        char = '\\'

    path_keyword = os.getcwd().split(char)[-2]

    try:
        if path_keyword == 'src' or path_keyword == 'notebooks':
        # cookiecutter folder structure
            save_path = '../../data/raw/'
        else:
        # KF's old folder structure
            save_path = 'Data/'
    except IndexError:
        save_path = 'Data/'
    
    return save_path

def random_from_dict(dict, n):
    """Return n random keys from dictionary"""
    assert type(n) == int, 'n must be an integer'
    import random
    return random.sample(list(dict.keys()), n)

def defang(x):
    import re
    fangs = re.compile(r'[\[\]]')
    return re.sub(fangs, '', x)

# SPARK ---------------------------------------------------------

def list_from_spark_col(df, col, distinct=True):
    if distinct:
        temp = df.select(col).distinct()
    else:
        temp = df.select(col)
    
    results = [row[col] for row in temp.collect()]
    
    return results

def value_counts_spark(df, col, ascend=False, show=True, pct=False):
    import pyspark.sql.functions as F

    cnt_df = df.groupBy(col).count().orderBy('count', ascending=ascend)
    if pct:
        x = cnt_df.groupby().sum('count').collect()
        tot = x[0]['sum(count)']
        cnt_df = cnt_df.withColumn('pct', F.round(F.col('count') / tot, 3)).orderBy('count', ascending=ascend)
    if show:
        cnt_df.show()
    return cnt_df


def read_text_file_hdfs(file_path, sep='\n'):
    """
    goal: read a text file from hdfs into a list

    args:
        file_path: the path to read from HDFS
            ex: /user/ahennessy/ddns/models/suspicious_ddns/c2_models.txt
        sep: the separator in the text file
    returns:
        a list
    """
    file_current = subprocess.check_output(["hadoop", "fs", "-cat", file_path])  # load dates from hdfs file
    list_obj = filter(None, file_current.split(sep))  # split into array
    return list_obj

def add_pct_from_counts(cts_df, count_col='count'):
    import pyspark.sql.functions as F

    x = cts_df.groupby().sum(count_col).collect()
    sum_col = 'sum({})'.format(count_col)
    tot = x[0][sum_col]
    cts_df = cts_df.withColumn('pct', F.round(F.col(count_col) / tot, 6)) \
                .orderBy(count_col, ascending=0)
    return cts_df

def parse_spark_output(output):
    """Accepts output (stderr & stdout) from a spark-submit job
    Returns 1 if "error" not found in output
    Parses & prints error, and returns 0 if "error" found in output

    Usage:
    # spark-submit command; must end in "exit 0"
    COMMAND = '/opt/spark2/bin/spark-submit --deploy-mode cluster --queue=root.steadystate --executor-memory 6G --num-executors 78 --driver-memory 4G --conf spark.executorEnv.PYSPARK_PYTHON=/usr/local/anaconda/bin/python --conf spark.yarn.appMasterEnv.PYSPARK_PYTHON=/usr/local/anaconda/bin/python /home/jobrunner/graph/graph_generation.py; exit 0'
    output = subprocess.check_output(run_command, shell=True, #text=True, #PYTHON3
                                 stderr=subprocess.STDOUT)
    check = parse_spark_output(output)
    print('Job successful' if check == 1 else 'There was an error') 
    """
    import re

    if re.search('error', output, re.IGNORECASE) is None:
        return 1
    else:
        print('Error')
        app_id_regex = re.compile('(application_[0-9_]*)')
        match = re.search(app_id_regex, output)
        if match:
            app_id = match.group()
            get_log_command = "yarn logs --applicationId {}".format(app_id)
            yarn_log = subprocess.check_output(get_log_command, shell=True)
            yarn_log = yarn_log.split('\n')
            stdout_line_idxs = [i for i,line in enumerate(yarn_log) 
                            if re.search('LogType:stdout', line) is not None
                         and re.search('End of', line) is None]
            star_line_idxs = [i for i,line in enumerate(yarn_log) 
                            if re.search(re.compile('\*\*\*\*\*\*'), line) is not None]
            start = stdout_line_idxs[0]    
            star_after_stdout = [x for x in star_line_idxs if x > start]    
            end = star_after_stdout[0]
            err_msg = yarn_log[start+4:end-1]
            for line in err_msg:
                print(line)
        else:
            print(output)
        return 0


# -----------------------------------------------------------
# Monitor Progress
class monitor_progress():
    """
    Initalize with:
    n [int]: the total count of the thing you wish to monitor the progress for
    chunk_pct [int]: Optional. how often 'X%' is printed out. default: 10
    chunk_dot [int]: Optional. how often a '.' is printout out. default: 2

    Usage:
    
    n = len(long_list)
    prog_monitor = monitor_progress(n, 10, 2)
    for i in range(n):
        # do something to i of long_list
        prog_monitor.run(i)
    """

    def _gen_pct_list(self):
        pct_list = np.arange(90, 0, -self.pct)
        self.pct_list = deque()
        for x in pct_list:
            self.pct_list.append(x)
    
    def _gen_dot_list(self):
        dot_list = np.arange(100-self.dot, 0, -self.dot)
        self.dot_list = deque()
        for x in dot_list:
            self.dot_list.append(x)
        
    def __init__(self, n, chunk_pct=10, chunk_dot=2):
        self.n = n
        self.pct = chunk_pct
        self.dot = chunk_dot
        self._gen_pct_list()
        self._gen_dot_list()
    
    def run(self, i):
        qcurr = int(100 * (i / self.n))
        if qcurr == 100:
            sys.stdout.write('\n')
            sys.stdout.flush()
        elif qcurr % self.pct == 0:
            if qcurr in self.pct_list:
                sys.stdout.write('%u%%' % self.pct_list.pop())
                sys.stdout.flush()
                if qcurr in self.dot_list:
                    self.dot_list.pop()
        elif qcurr % self.dot == 0:
            if qcurr in self.dot_list:
                sys.stdout.write('.')
                sys.stdout.flush()
                self.dot_list.pop()

# PARSING -----------------------

# parse nested json

def check_if_dict(obj, name):
    if isinstance(obj, dict):
        for key, val in obj.items():
            if isinstance(val, dict):
                return check_if_dict(val, name + '_' + key)
            else:
                return {name + '_' + key: check_if_dict(obj[key], key) for key in obj.keys()}
    else:
        return obj

def parse_nested_json(data_list, key_idx=0):
    """
    data_list is a list of nested json entries.
    key_idx [int or list]: Either index of item in data_list that 
            contains all keys. Or, provide list of keys. Default = 0.
    """
    if isinstance(key_idx, int):
        main_keys = list(data_list[key_idx].keys())
    else:
        main_keys = key_idx

    flat_data_list = []

    for item in data_list:
        flat_dict = {}
        for key in main_keys:
            x = item[key]
            check = check_if_dict(x, key)
            if isinstance(check, dict):
                flat_dict.update(check)
            else:
                flat_dict[key] = check
        flat_data_list.append(flat_dict)

    return pd.DataFrame(flat_data_list)

# STRINGS
def remove_punctuation(x):
    return x.translate(str.maketrans('', '', string.punctuation))

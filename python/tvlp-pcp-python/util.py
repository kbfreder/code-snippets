
import boto3
# import configparser
from datetime import datetime, timedelta
import numpy as np

import pyspark.sql.functions as F
import pyspark.sql.types as T
from pyspark.sql.window import Window

CONFIG_FILE_BUCKET = "tvlp-ds-users"
CONFIG_FILE_KEY = "kendra-frederick/full-solution-cache/phase2/.config"
LIST_DELIMITER = ","


# CONFIG PARSING FUNCS
# =======================

def read_config_file():
    """Returns contents of project config file stored in S3.

    How to use this function:
    ```
    cf_contents = util.read_config_file()
    config = configparser.ConfigParser()
    config.read_string(cf_contents)
    ```
    """
    s3 = boto3.resource('s3')
    config_obj = s3.Object(bucket_name=CONFIG_FILE_BUCKET, key=CONFIG_FILE_KEY)
    response = config_obj.get()
    contents = response['Body'].read().decode()
    return contents


# GENERIC
# ----------------

def parse_list_ints(list_str, delim=LIST_DELIMITER):
    return [int(x) for x in list_str.split(delim)]


def parse_list_floats(list_str, delim=LIST_DELIMITER):
    return [float(x) for x in list_str.split(delim)]


def parse_date(date_str, delim=LIST_DELIMITER):
    date_ints = [int(x) for x in date_str.split(delim)]
    date = datetime(*date_ints)
    return date


# PROJECT-SPECIFIC 
# ----------------

def get_keys(config):
    keys_str = config['keys']['keys']
    return keys_str.split(LIST_DELIMITER)


def get_min_data_requirements(config):
    MIN_AVG_NUM_SHOPS = config.getint('min_data_requirements', 'MIN_AVG_NUM_SHOPS')
    MIN_FRACTION_SHOP_DAYS =  config.getfloat('min_data_requirements', 'MIN_FRACTION_SHOP_DAYS')
    MIN_NUM_TRAVEL_DATES =  config.getint('min_data_requirements', 'MIN_NUM_TRAVEL_DATES')

    return {
        'MIN_AVG_NUM_SHOPS': MIN_AVG_NUM_SHOPS,
        'MIN_FRACTION_SHOP_DAYS': MIN_FRACTION_SHOP_DAYS,
        'MIN_NUM_TRAVEL_DATES': MIN_NUM_TRAVEL_DATES,
    }


def get_modeling_configs(config):
    ptile_list_str = config['modeling']['ptile_list_str']
    return {
        'PCT_DIFF_THRESHOLD': config.getfloat('lifetimes', 'PCT_DIFF_THRESHOLD'),
        'NUM_DAYS': config.getint('modeling', 'num_days'),
        # 'DEFAULT_BUCKETS_CHOICE': config.get('modeling', 'ap_buckets_choice'),
        ## NOTE: ptile list is parsed as floats, but later they are treated as int's
        'PTILE_LIST': parse_list_floats(ptile_list_str),
        'TTL_COL': config.get('modeling', 'ttl_col'),
        'TTL_UNITS': config.get('modeling', 'ttl_units'),
        'TTL_PTILES_FORMAT': config.get('modeling', 'ttl_ptiles_format'),
        'AP_CUTOFF': config.getint('modeling', 'ap_cutoff'),
        'CLIP_TTLS_BOOL': config.getboolean('modeling', 'clip_ttls_bool'),
        'CLIP_TTLS_LIM': config.get('modeling', 'clip_ttls_lim'),
        'PTILE': config.getfloat('sim_cache', 'ptile'),
    }


def parse_ap_config(ap_config_str):
    """
    AP buckets configs get loaded as a string, e.g.: 
    '2,4'.
    This needs to get parsed into a list of buckets, e.g.:
    [-2, 2], [2, 4], [4, 366]
    """
    if ap_config_str == 'Null':
        return None
    ap_cutoffs = [int(x) for x in ap_config_str.split(',')]
    ap_buckets = []
    current_cutoff = ap_cutoffs[0]
    last_cutoff = current_cutoff
    for i, current_cutoff in enumerate(ap_cutoffs):
        if i == 0:
            ap_buckets.append([-2, current_cutoff])
        else:
            ap_buckets.append([last_cutoff, current_cutoff])
        if i == len(ap_cutoffs) - 1:
            ap_buckets.append([current_cutoff, 366])
        last_cutoff = current_cutoff
    return ap_buckets


# PROJECT-SPECIFIC SHARED FUNCTIONS 
# =======================



def unconcat_keys(df, keys_wo_dates, drop_key_col: bool=True):
    """
    df must contain column "key", which is concatenated string of key attributes.
    `keys_wo_dates` must be in same order in whichs keys were concatenated
    """
    unconcat_df = df.select("*", 'key', F.split('key', '_').alias('key_array'))
    for i, col in enumerate(keys_wo_dates):
        unconcat_df = unconcat_df.withColumn(col, F.col('key_array').getItem(i))
    if drop_key_col:
        unconcat_df = unconcat_df.drop('key')
    return unconcat_df.drop("key_array")



# COLLECTING TIMESTAMPS
# ----------------

def calc_fare_change_bool_mod(input_df, keys, input_src):
    
    """Detect fare changes as boolean (1/0) events.

    params:
    ------
    input_df: Spark DataFrame
        contains raw data
    keys: list(str)
        Keys to calculate fare changes across. Should include
        travel dates
    input_src: string - ("raw", "rollup")
        Source of input data. "raw" or "rollup"
        
    returns:
    --------
    Spark DataFrame containing all original data, with column related
        to fare changes added.
    """
    if input_src == 'raw':
        order_by_cols = ['shop_req_timeStamp', 'group_id']
    elif input_src == 'rollup':
        input_df = input_df.withColumn("first_ts", F.array_min("timestamps"))
        order_by_cols = ['first_ts']

    w = (Window
         .partitionBy(keys)
         .orderBy(order_by_cols)
        )
    
    df_fc_raw = (input_df
                 .withColumn("prev_fare", F.lag("fare", 1).over(w))
                 # mark "type" of fare change 
                 .withColumn("first_obs", F.when(
                     F.col("prev_fare").isNull(), 1).otherwise(0))
                 .withColumn('prev_fare_different', F.when(
                    F.col("fare") != F.col("prev_fare"), 1).otherwise(0))
                 # modified for revamped lifetimes
                 .withColumn('fare_change_bool', F.when(
                     (F.col("prev_fare_different") == 1)
                     | (F.col("first_obs") == 1)
                     , 1).otherwise(0))
            )
    return df_fc_raw


def collect_ts(df_fcb, keys, input_src):
    """
    
    input_src: string - ("raw", "rollup")
        Source of input data. "raw" or "rollup"
        
    """
    grp_by_cols = [*keys, 'grp_num', 'fare']
    
    if input_src == 'raw':
        time_col = 'shop_req_timeStamp'
        collect_col = 'shop_req_timeStamp'
    elif input_src == 'rollup':
        time_col = 'first_ts'
        collect_col = 'timestamps'

    w_grp = (Window
        .partitionBy(keys)
        .orderBy(time_col)
        )

    df_fcb = df_fcb.withColumn("grp_num", 
                               F.sum((F.col("fare_change_bool") == 1).cast("int")).over(w_grp))
    if input_src == 'raw':
        
        df_ts_agg = (df_fcb
                     .groupBy(grp_by_cols)
                     .agg(
                         F.collect_list(collect_col).alias("grp_timestamps"),
                         F.collect_set("shop_date_dt").alias("shop_days")
                     )
                    )
    
    if input_src == 'rollup':
        df_ts_agg = (df_fcb
                     .groupBy(grp_by_cols)
                     .agg(
                         F.collect_list(collect_col).alias("grp_timestamps"),
                         F.collect_set("shop_days").alias("shop_days")
                     )
                     .withColumn("grp_timestamps", F.flatten("grp_timestamps"))
                     .withColumn("shop_days", F.flatten("shop_days"))
                    )

    return df_ts_agg


def label_censored(df_ts_agg, keys):
    """Label censored observations: left, right, left-right, uncens    
    """
    w = Window.partitionBy(*keys)
        
    df_ts_agg = df_ts_agg.withColumn("last_grp", F.max("grp_num").over(w))
    
    df_mark_cens = df_ts_agg.withColumn(
        "censored", F.when(F.col("last_grp") == 1, "left-right")
        .otherwise(F.when(F.col("grp_num") == 1, "left")
            .otherwise(F.when(F.col("grp_num") == F.col("last_grp"), "right")
                .otherwise("uncens"))))
    
    df_mark_clean = (df_mark_cens
                     .drop("grp_num", "last_grp")
                     .withColumnRenamed("grp_timestamps", "timestamps")
                    )
    return df_mark_clean


# MODELING
# ----------------

## this is currently unused, but copied here for possible future use.
def calc_zip_ptiles_of_lifetimes(df_lft, ptile_list):
    @F.udf(returnType=(T.ArrayType(T.StructType([
        T.StructField('ptile', T.FloatType()), 
        T.StructField('value', T.FloatType())
    ]))))
    def calc_ptile(arr):
        if len(arr) > 0:
            np_val_arr = np.percentile(arr, ptile_list)
            val_arr = [float(x) for x in np_val_arr]
            ptile_arr = [float(p) for p in ptile_list]
            return list(zip(ptile_arr, val_arr))
        else:
            return []

    df_ptile = df_lft.withColumn("lft_ptiles_in_min", calc_ptile("lifetimes"))
    return df_ptile

## not currently in use
TTL_PTILES_FORMAT = 'v1'
LFT_PTILES_COL = 'lft_ptiles_col'
def extract_ttl_ptile(ttl_df, ttl_col, ptile, ptile_list, ttl_ptiles_format=TTL_PTILES_FORMAT):
    idx = ptile_list.index(ptile)
    if ttl_ptiles_format == "v1":
        ttl_df = ttl_df.withColumn(ttl_col, F.col(LFT_PTILES_COL).getItem(idx))
    elif ttl_ptiles_format == "v2":
        ttl_df = ttl_df.withColumn(ttl_col, F.col(LFT_PTILES_COL).getItem(idx).getItem("value"))
    return ttl_df


def get_ttl_col_name_from_ptile(ptile):
    """Derives column name for TTL from given percentile (ptile).
    
    Params:
        ptile: float
    Returns:
        string
    """
    return f"ttl_ptile_{str(ptile).replace('.','-')}"

# I/O / PATHS
# ----------------

# TODO: make accessing any/all paths a class

# TODO: make this a class
## it can be called within a loop in scripts
## class would save us having to parse everything every time
def get_input_source_from_date(date, config):

    INPUT_DIR_1 = config['paths']['INPUT_DIR_1']
    INPUT_DIR_2 = config['paths']['INPUT_DIR_2']
    INPUT_DIR_3 = config['paths']['INPUT_DIR_3']
    INPUT_DIR_4 = config['paths']['INPUT_DIR_4']

    INPUT_DATE_2 = parse_date(config['paths']['raw_input_date_2'])
    INPUT_DATE_3 = parse_date(config['paths']['raw_input_date_3'])
    INPUT_DATE_4 = parse_date(config['paths']['raw_input_date_4'])

    if date < INPUT_DATE_2:
        return INPUT_DIR_1
    elif date < INPUT_DATE_3:
        return INPUT_DIR_2
    elif date < INPUT_DATE_4:
        return INPUT_DIR_3
    else:
        return INPUT_DIR_4


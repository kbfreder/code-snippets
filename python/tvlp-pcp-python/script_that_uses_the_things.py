
import sys
from datetime import datetime, timedelta
import argparse
import configparser

from pyspark.sql import SparkSession
import pyspark.sql.functions as F

import util


# DEFINE/GET CONFIGS/DEFAULTS
cf_contents = util.read_config_file()
config = configparser.ConfigParser()
config.read_string(cf_contents)

APP_NAME = "CollectTimeStamps"
SCRIPT_VERSION = "3.0"
KEYS_VERSION = config['keys']['keys_version']

S3_BASE_FOLDER = config['paths']['S3_BASE_FOLDER']
BASE_OUTPUT_DIR = f"{S3_BASE_FOLDER}/phase2/keys_v{KEYS_VERSION}/collected-ts-data"
BASE_OUTPUT_DIR_RAW = f"{BASE_OUTPUT_DIR}/single-days"

RAW_NUM_PARTS = 50
WEEK_NUM_PARTS = 250

# Copied from `preprocessing.py`, minus the Traveloka markets
## TODO: move to config file
MARKET_DICT = {
 }
MARKET_LIST_NESTED = MARKET_DICT.values()
MARKET_LIST_FLAT = [x for y in MARKET_LIST_NESTED for x in y]

KEYS = util.get_keys(config)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--date-start",
        help="Starting date of preprocessed data to use. Of format YYYY-MM-DD",
        type=str,
        required=True
    )
    parser.add_argument(
        "--date-end",
        help="Ending date of raw preprocessed data to use, inclusive. Of format YYYY-MM-DD. "
        "If not supplied, only a single day (`date-start`) of raw data will be processed. ",
        type=str,
        required=False
    )
    parser.add_argument(
        "--num-legs", "-l",
        help="Number of legs. Restriction placed on itiernaries.",
        type=int,
        default=config.getint('DEFAULT', 'max_num_legs'),
    )
    parser.add_argument(
        "--test", "-t",
        help="Run in test mode: TBD what that means",
        default=False,
        action="store_true"
    )
    args = parser.parse_args()
    return args


# "FINISH PREPROCESSING" FUNCTIONS
# ------------------------------
# <REDACTED>

# META FUNCTIONS
def process_day(date, keys=KEYS):
    src = "raw"
    date_str = date.strftime("%Y%m%d")
    base_input_dir = util.get_input_source_from_date(date, config)
    input_dir = f"{base_input_dir}/{date_str}/"
    df = spark.read.parquet(input_dir)
    df_proc = finish_preprocessing(df, keys, 2)
    df_fcb = util.calc_fare_change_bool_mod(df_proc, keys, src)
    df_ts_agg = util.collect_ts(df_fcb, keys, src)
    df_cens_ts = util.label_censored(df_ts_agg, keys)
    return df_cens_ts   


def process_days_raw(date_list):
    for date in date_list:
        loop_start = datetime.now()
        
        df = process_day(date)
        
        date_str = date.strftime("%Y%m%d")
        out_path = f"{BASE_OUTPUT_DIR_RAW}/{date_str}"
        print(f"Saving to {out_path}")
        df.coalesce(RAW_NUM_PARTS).write.mode("overwrite").parquet(out_path)
        
        loop_end = datetime.now()
        loop_elapsed_time = (loop_end - loop_start).total_seconds() / 60
        print(f"Done with {date_str}! Loop elasped time: {loop_elapsed_time:.2f} min")


# ==================================
if __name__ == "__main__":
    script_start = datetime.now()

    args = parse_args()
    date_start_str = args.date_start
    date_end_str = args.date_end
    num_legs = args.num_legs
    test = args.test

    # do stuff with args
    start_dt = datetime.strptime(date_start_str, "%Y-%m-%d")

    if test:
        print(util.get_input_source_from_date(start_dt, config))
        sys.exit(0)
    
    spark = SparkSession.builder.getOrCreate()
    print(args)
    print(f"Using keys: {KEYS}")

    if date_end_str is None:
        end_dt = start_dt
    else:
        end_dt = datetime.strptime(date_end_str, "%Y-%m-%d")
    num_days = (end_dt - start_dt).days + 1
    date_list = [start_dt + timedelta(days=x) for x in range(num_days)]
    
    process_days_raw(date_list)
    
    script_end = datetime.now()
    elapsed_time = (script_end - script_start).total_seconds() / 60
    print(f"Done with script! Total elasped time: {elapsed_time:.2f} min")
    spark.stop()
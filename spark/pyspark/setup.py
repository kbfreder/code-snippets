
import argparse
import pyspark
from pyspark.sql import SparkSession


APP_NAME = "KF-LowFare"

# We do this so we can run code (.py file) using 
# spark-submit, where configurations regarding memory & number 
# of executors is defined at run-time -- i.e.:
# `spark-submit --driver-memory 20g --master yarn pyfile.py``
# or using python .exe (i.e.: `/bin/python pyfile.py``)


parser = argparse.ArgumentParser()
parser.add_argument(
    "--run-mode",
    help="Run-mode",
    choices=("spark-submit", "python-exe")
)
args = parser.parse_args()

run_mode = args.run_mode


if run_mode == "python-exe":
    conf1 = pyspark.SparkConf().setAll(
        [('spark.master','yarn'),
        ('spark.app.name', APP_NAME),
        ('spark.driver.memory','20g'),
        ('spark.executor.memory', '20g'),
        ('spark.executor.instances', 10),
        ('spark.executor.cores', '10'),
        ])
    spark = SparkSession.builder.config(conf = conf1).getOrCreate()
elif run_mode == "spark-submit":
    spark = SparkSession.builder.appName(APP_NAME).getOrCreate()
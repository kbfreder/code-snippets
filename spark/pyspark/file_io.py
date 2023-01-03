

# LOADING
df = spark.read.parquet("hdfs:///path/to/parent/folder")

# to read all files in a higher level dir
df = spark.read.parquet("hdfs:///path/to/grand-parent/folder/*")

df = spark.read.csv("hdfs://path/to/file.csv", header=True, inferSchema=True)



# SAVING
    # note: you may want to repartition or coalesce before saving to reduce
    # number of files written / optimize their size

df.write.mode("append").parquet("hdfs:///path/to/folder")
    # note: folder will be created if it does not exist
    # parquet files will be saved within this location / folder

df.write.mode("overwrite").option("header", True).csv("hdfs://path/to/file.csv")

# PYTHON


## LOADING
df = spark.read.parquet("hdfs:///path/to/parent/folder")

### to read all files in a higher level dir
df = spark.read.parquet("hdfs:///path/to/grand-parent/folder/*")

df = spark.read.csv("hdfs://path/to/file.csv", header=True, inferSchema=True)


## SAVING
    # note: you may want to repartition or coalesce before saving to reduce
    # number of files written / optimize their size

df.write.mode("append").parquet("hdfs:///path/to/folder")
    # note: folder will be created if it does not exist
    # parquet files will be saved within this location / folder

df.write.mode("overwrite").option("header", True).csv("hdfs://path/to/file.csv")


# SCALA

// Loading data
val df = spark.read.parquet("hdfs:///data/consumerpref/merged/encoded/cut301/20220701/00")

  // csv with header
val top_markets_df = spark.read.format("csv").option("header", true).load(top_markets_path)


// Writing data
df.write.parquet("hdfs://path/to/data/")
df.write.option("header", true).csv("/path/to/file.csv") 


# schema issues
if your schema got messed up
- can manifest as "column not in schema" even though it is, at least for some of the data
- or as "java.lang.UnsupportedOperationException: "

try this:
```
spark.conf.set("spark.sql.parquet.mergeSchema", "true")
```
or:
```scala
spark.read.option("mergeSchema", "true").parquet(path)
```
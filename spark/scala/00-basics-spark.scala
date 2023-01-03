
// In Spark compiled jobs, you need to start with the following:

import org.apache.spark.sql.SparkSession
import org.apache.spark.SparkContext

val spark = SparkSession.builder.        // builder pattern to construct the session
  master("local[*]").                    // run locally on all cores ([*])
  appName("Console").
  config("spark.app.id", "Console").     // to silence Metrics warning
  getOrCreate()                          // create it!

val sc = spark.sparkContext              // get the SparkContext
val sqlContext = spark.sqlContext        // get the old SQLContext, if needed
import sqlContext.implicits._            // import useful stuff
import org.apache.spark.sql.functions._  // here, import min, max, etc.


// string concatenation 
val hdfs_path = "hdfs://" + data_dir + date + "/" + h_str

// int to string, with formatting:
val h = 7
val h_str = "%02d".format(h)
> h_str: String = 00

// Loading data
val df = spark.read.parquet("hdfs:///data/consumerpref/merged/encoded/cut301/20220701/00")

  // csv with header
val top_markets_df = spark.read.format("csv").option("header", true).load(top_markets_path)


// Writing data
df.write.parquet("hdfs://path/to/data/")
df.write.option("header", true).csv("/path/to/file.csv") 


// filter
val jb_raw = df_raw.filter(
    (col("s_outOriginAirport") === 201398272) &&
    (col("s_outDestinationAirport") === 168168192) && 
    (col("s_outDeptDt") === 20220705) && 
    (col("pos") === 353566720) &&
    array_contains(col("s_outMarketingCxr"), 35717120)
)

// different way to refer to a column
col("col_name")
$"col_name"
'col_name



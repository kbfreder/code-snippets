/**
Common code edits one must do when converting from PySpark to Scala
*/

// single quotes --> double quotes


// f-strings --> s-strings
    // pyspark
.withColumn(f"{dcn}_fbc_leg1", ...
    // scala
.withColumn(s"${dcn}_fbc_leg1", ...
     
    // note sometimes you'll need the `$`, sometimes you won't


// select a list of columns
var df2 = df.select(cache_cols.map(m=>col(m)):_*)
var df2 = df.select(cache_cols.map(col(_)):_*)
var df2 = df.select(cache_cols.map(col):_*)



// None --> null

// Scala typically imports sql functions as so:
import org.apache.spark.sql.functions._

    // so they are called as so:
df.withColumn("new_col", when(col("a") === col(b), 1).otherwise(0))


// equality, and, or
df.filter((col("a") === "a") && (col("b") === "b") || (col("c") === "c"))


// Arrays / Lists behave differently
    // ex:
    val RAW_COLS_TO_WRITE = List(
      "id", "group_id", "shop_req_timeStamp", "originalRequest",
      "pcc", "gds")
        val CACHE_COLS = RAW_COLS_TO_WRITE ::: List(
      "request_PTC", "response_PTC",
      "private_fare")

    // see `sequences.scala` for further examples, info
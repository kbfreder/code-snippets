
// select
    // from a list
var df2 = df.select(cache_cols.map(m=>col(m)):_*)
var df2 = df.select(cache_cols.map(col(_)):_*)


/// all and a computed col:
var df2 = df.select($"*", posexplode($"request_PTC").as(Seq("requ_pos", "requ_ptc_")))


// filter 
// ref: https://sparkbyexamples.com/spark/spark-dataframe-where-filter/

/// note the triple '=' and the double '&'
val ex_raw = df_raw.filter(
    (col("s_outOriginAirport") === 101452800) &&
    (col("s_outDestinationAirport") === 85398016) && 
    (col("s_outDeptDt") === 20220627) && 
    array_contains(col("s_outMarketingCxr"), 67895296)
)

/// column val is in a list 
df_filt = df.filter(col("market").isin(TOP_MARKETS_LIST: _*)

/// filter on column is / is not Null
val cond_ow = ((col("in_origin_airport").isNull) && (col("in_destination_airport").isNull))
val cond_other = ((col("in_origin_airport").isNotNull) && (col("in_destination_airport").isNotNull))




//  =================================
// GROUP-BY + AGG
//  =================================

var min_fare_df = df.groupBy("col_name").count()

// multple columns
val df_agg = df.groupBy("outOriginAirport", "outDestinationAirport")...

// using an array
var groupby_cols = Array(
     |     "s_outOriginAirport",
     |     "s_outDestinationAirport",
     |     "s_outDeptDt",
     |     "s_inOriginAirport",
     |     "s_inDestinationAirport",
     |     "s_inDeptDt"
     |     )

var min_fare_df = (df
        .groupby(groupby_cols.head, groupby_cols.tail : _*)
        .agg(min("fare").alias("min_fare"))
)


// alias'ing the agg column
var min_fare_df = df.groupBy("col_name")
    .agg(min("fare").alias("min_fare"))

// count, then order descending
// this is essentially 'value_counts' in pandas
df_raw.groupBy("validatingCxr").count().orderBy(col("count").desc)


// explode an array to rows
df_adt_expl = df_adt.withColumn("PTC", explode($"responsePTC"))
    .withColumn("farePTC", explode($"fareBreakDownByPTC"))


//  =================================
// JOIN
//  =================================

// when key is same in both df's
    // also note use of broadcast if 1 of the df's is small
val df_join = df_adt2.join(broadcast(top_mrkt_df), Seq("market_key"), "inner")

// when name of key col is different
val df_join = df1.join(df2, df1("key_1") === df2("key_2"), "inner")

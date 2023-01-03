


# PYTHON
- alias column after:
```python
min_fare_df = (df.groupBy(groupby_cols)
                .agg(
                    F.min("paxprice").alias("min_fare"),
                    F.max("paxprice").alias("max_fare")
                    )
            )
```
- group by, count, order desc
cnt_df = df.groupby("key").count().orderBy(F.desc("count"))




# SCALA

//  =================================
// GROUP-BY + AGG
//  =================================
```scala
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

// group by, count, order desc
var cnt_df = df.groupby("col_name").count().sort($"count".desc)

```
// 
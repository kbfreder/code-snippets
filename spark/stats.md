

# general stats

## sum, pcts of total
- sum over a column
df.agg({'subject 1': 'sum'}).show()

- divide each row/values by sum of column:
```pyspark
w = Window.partitionBy()
df = df.withColumn("pct_total", F.col("data") / F.sum("data").over(w))
```

- cumulative pct

w2 = Window.partitionBy().orderBy("search_rank").rowsBetween(Window.unboundedPreceding, Window.currentRow)
w3 = Window.partitionBy().orderBy("search_solutions").rowsBetween(Window.unboundedPreceding, Window.currentRow)

pl_market_stats = (pl_market_stats
                   .withColumn("cum_pct_searches", F.sum("pct_searches").over(w2))
                   .withColumn("cum_pct_solutions", F.sum("pct_solutions").over(w3))
                  )


# binning data

## using QuantileDiscretizer
- note: works ok if data is normally distributed, less so if not
- Does not split range of values into equally sized bins

```scala
import org.apache.spark.ml.feature.{Bucketizer, QuantileDiscretizer}

val discretizer = new QuantileDiscretizer()
  .setInputCol("colToBucket")
  .setOutputCol("quantiledFeature")
  .setNumBuckets(4)

val result = discretizer.fit(df).transform(df)
```

## using Bucketizer
Must supply split values

```scala
import org.apache.spark.ml.feature.{Bucketizer, QuantileDiscretizer}

val split_vals = Array(0.0, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.0)
val bucketizer = new Bucketizer()
    .setInputCol("colToBucket")
    .setOutputCol("discretizedFeature")
    .setSplits(split_vals)

val binnedData = bucketizer.transform(df)
```

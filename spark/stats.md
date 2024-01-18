

# stats on rows by group

## sum, pcts of total
- sum over a column
df.agg({'subject 1': 'sum'}).show()


- divide each row/values by sum of column:
```pyspark
w = Window.partitionBy()
df = df.withColumn("pct_total", F.col("data") / F.sum("data").over(w))
```

- cumulative pct

w = Window.partitionBy().orderBy(F.desc("count")).rowsBetween(Window.unboundedPreceding, Window.currentRow)

df = df.withColumn("cum_pct_counts", F.sum("pct_counts").over(w))


# stats on columns

## taking average of 2 or more columns

marksColumns = [col('marks1'), col('marks2')]
averageFunc = sum(x for x in marksColumns)/len(marksColumns)
df = df.withColumn('Result(Avg)', averageFunc)

- to specify col's programatically
df = df.withColumn("all_features_avg", sum(F.col(x) for x in feature_list) / len(feature_list))

- or:
ttl_cols = [F.col(f"ttl_{d}") for d in date_str_list]
df_for_comp = df_for_comp.withColumn("avg_ttl", sum(ttl_cols) / len(ttl_cols))


### ignoring nulls
```python
col_names = [list,of,column,names,to,average]
df_avg = df.fillna(0)
df_avg = df_avg.withColumn("avg_ttl",
                           sum([df_avg[col] for col in col_names]) /
                           sum(F.when(df_avg[col] > 0, 1).otherwise(0) for col in col_names)
                          )
```

## getting the min or max of 2 or more columns
ttl_cols = [F.col(f"ttl_{d}") for d in date_str_list]
df.withColumn("minimum", F.least(*ttl_cols))


## standard deviation of 2 or more columns
```python
from pyspark.ml.feature import VectorAssembler
ttl_cols = [F.col(f"ttl_{d}") for d in date_str_list]
va = VectorAssembler(inputCols=ttl_cols, outputCol="features")
df_for_comp = va.transform(df_for_comp)

# notes: 
## - must convert output using `float` because spark doesn't play nice with numpy
## - must use `toArray()` and not `tolist()`, because VectorAssembler output both
##   Dense and Sparse Vectors, and the latter doesn't have a `tolist` method
np_std_udf = F.udf(lambda x: float(np.std(x.toArray())), T.DoubleType())
df_for_comp = df_for_comp.withColumn("std_ttl", np_std_udf("ttls"))
```


## sum of an array col

# general stats




## percentiles
- `approxQuantile`
  - args are: column, list of percentiles, relative error
ptiles = [0.01, 0.05, 0.95, 0.99]
qtiles = df.stat.approxQuantile("min_fare", ptiles, 0.005)
qtiles

- with groupBy:
df_grp = df.groupBy("market").agg(
  F.expr('percentile_approx(col_name, 0.5)'
                       ).alias("median_col_name"),
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

```python

from pyspark.ml.feature import Bucketizer, QuantileDiscretizer

split_vals = np.linspace(0,1,11)
bucketizer = Bucketizer(
    inputCol=col,
    outputCol="bucket",
).setSplits(split_vals)

bin_df = bucketizer.transform(err_by_td_filt)

bin_stats = (bin_df
             .groupBy("bucket")
             .agg(F.count("*").alias("count"))
             .orderBy("bucket")
            )
bin_pdf = bin_stats.toPandas()

# note: this assumes all bins are used. they might not be
xs = range(len(bin_pdf))
plt.clf()
plt.bars(xs, bin_pdf['count'])
plt.xticks(xs, bin_pdf['bucket'])
# or see below for make nice labels 


# if not all buckets used. uses "nice" labels below
split_labels = get_split_labels(split_vals)
split_label_lkup = dict(zip(range(len(split_labels)), split_labels))
bin_pdf['label'] = bin_pdf['bucket'].map(split_label_lkup)
```

say you do this 2x, then plot as a heatmap:

```
ns_bucketizer = Bucketizer(
    inputCol="log_orig_num_shops",
    outputCol="num_shops_bucket",
).setSplits(ns_split_vals)

df_w_bins_1 = ns_bucketizer.transform(df_filt)

cer_split_vals = np.linspace(0,1,11)

cer_bucketizer = Bucketizer(
    inputCol="cache_err_rate",
    outputCol="cache_err_bucket",
).setSplits(cer_split_vals)

df_w_bins_2 = cer_bucketizer.transform(df_w_bins_1)

bin_stats = (df_w_bins_2
             .groupBy("num_shops_bucket", "cache_err_bucket")
             .agg(F.count("*").alias("count"))
             .orderBy("num_shops_bucket", "cache_err_bucket")
            )
bin_pdf = bin_stats.toPandas()

bin_pivot = bin_pdf.pivot(index="num_shops_bucket", columns="cache_err_bucket")


def _get_str(x):
    return f"{x:.1f}"

def get_split_labels(split_vals):
    n = len(split_vals)

    split_labels = []
    for i in range(n-1):
        if i == 0:
            split_labels.append(f"{_get_str(split_vals[i])}-{_get_str(split_vals[i+1])}")
        elif i == n-2:
            split_labels.append(f">{_get_str(split_vals[i])}")
        else:   
            split_labels.append(f"{_get_str(split_vals[i])}-{_get_str(split_vals[i+1])}")

    return split_labels



ns_split_labels = get_split_labels(ns_split_vals)
cer_split_labels = get_split_labels(cer_split_vals)

xs = np.arange(bin_pivot.shape[1])+0.5
ys = np.arange(bin_pivot.shape[0])+0.5

# if you need to plot log counts in heatmap:
from matplotlib.colors import LogNorm

plt.clf()
fig, ax = plt.subplots(figsize=(6,6))
sns.heatmap(bin_pivot, cmap='viridis', ax=ax, square=True,
           norm=LogNorm())

plt.xlabel("cache error rate")
plt.xticks(xs, cer_split_labels, rotation=90)

plt.ylabel("log shopping volume")
plt.yticks(ys, ns_split_labels, rotation=360)
plt
fig.tight_layout()
plt.show()
%matplot plt
```
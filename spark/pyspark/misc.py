

# check data skew
p_cnts = df.groupBy(F.spark_partition_id()).count().orderBy("count", ascending=False)


# equivalent of np.where

from pyspark.sql.functions import when, col

df = df.withColumn('color', when(col('Set') == 'Z', 'green').otherwise('red'))


# pretty print a row
def pp_row(df):
    cols = df.columns
    out = df.take(1)
    for i, x in enumerate(out[0]):
        print(cols[i], x)
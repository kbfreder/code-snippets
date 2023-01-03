import pyspark.sql.functions as F


# helper func to "peek" at one row of data

# ======================
# DATA TYPES
# ======================

# cast to new data type
from pyspark.sql.types import FloatType # etc
df.withColumn("paxprice", F.col("paxprice").cast(FloatType())) 



# ======================
# GROUP-BY AGG
# ======================

# multiple aggs:


# alias column after:

min_fare_df = (df.groupBy(groupby_cols)
                .agg(F.min("paxprice").alias("min_fare"))
)


# ======================
# NULLS
# ======================

df.filter(df["colName"].isNull())
df.filter(df["colName"].isNotNull())
df.filter("colName is NULL")

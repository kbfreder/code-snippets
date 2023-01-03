

```python
from pyspark.sql.window import Window

w = (Window
    .partitionBy("outDeptDt", "inDeptDt")
    .orderBy("searchDt") 
    .rowsBetween(Window.unboundedPreceding, Window.currentRow)
    )


# function to compute the number of seconds in a day
days = lambda i: i * 864000

w = (Window
    .partitionBy("outDeptDt", "inDeptDt")
    .orderBy("timestamp").cast('long') # must be numeric
    .rangeBetween(-days(7), 0)
    )

```

Cumulative percent

df.show()
+-------------+---------------+
|days_til_dept|sum_shop_counts|
+-------------+---------------+
|           31|        9532855|
|           53|        4056964|
|           34|        6388114|
|           28|        8370667|
|           27|        7915019|
+-------------+---------------+

w = (Window
         .orderBy("days_til_dept")aaa
         .rowsBetween(Window.unboundedPreceding, Window.currentRow)
    )

df = (df
        .withColumn("cum_sum", F.sum("sum_shop_counts").over(w))
        .withColumn("cum_pct", F.col("sum_shop_counts") / F.col("cum_sum"))
        )

df.show()
+-------------+---------------+-------+-------+
|days_til_dept|sum_shop_counts|cum_sum|cum_pct|
+-------------+---------------+-------+-------+
|           31|        9532855|9532855|    1.0|
|           53|        4056964|4056964|    1.0|
|           34|        6388114|6388114|    1.0|
|           28|        8370667|8370667|    1.0|
|           26|        7499215|7499215|    1.0|
+-------------+---------------+-------+-------+
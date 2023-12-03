// quick dummy dataframe
```scala
val columns = Seq("language", "users_count")
val data = Seq(("Java", "20000"), ("Python", "100000"), ("Scala", "3000"))
val df = spark.createDataFrame(data).toDF(columns:_*)
```

```python



```



# map dict to col in spark data frame
```python
from itertools import chain
curr_lookup = {
    'KRW': 0.00078,
    'USD': 1.0, 
    'TWD': 0.032, 
    'INR': 0.012, 
    'JPY': 0.0071, 
    'HKD': 0.13, 
    'CAD': 0.75,
    'MYR': 0.22,
    'GBP': 1.27,
    'AUD': 0.68
}

map_expr = F.create_map([F.lit(x) for x in chain(*curr_lookup.items())])
err_by_cur = err_by_cur.withColumn("exchange_rate", map_expr.getItem(F.col("currency")))

```
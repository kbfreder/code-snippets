
# basic window func
```python
from pyspark.sql.window import Window

w = (Window
    .partitionBy("outDeptDt", "inDeptDt")
    .orderBy("searchDt") 
    .rowsBetween(Window.unboundedPreceding, Window.currentRow)
    )
```

# `orderBy` a date
```
# function to compute the number of seconds in a day
calc_days = lambda i: i * 60*60*24

w = (Window
    .partitionBy("outDeptDt", "inDeptDt")
    .orderBy("timestamp").cast('long') # must be numeric
    .rangeBetween(-calc_days(7), 0)
    )

```

# Cumulative percent

w_shop = (Window
          .orderBy('shop_date')
          .partitionBy(p_cols)
          .rangeBetween(Window.unboundedPreceding, Window.currentRow)
        )

w_trip = (Window
          .partitionBy(p_cols)
        )

df = (df
        .withColumn("cum_sum_shop_vol", F.sum('shops_day').over(w_shop))
        .withColumn("total_shop_vol", F.sum('shops_day').over(w_trip))
        .withColumn("cum_pct_shop_vol", 
                    F.col('cum_sum_shop_vol') / F.col("total_shop_vol"))
        )


df.select(...).show()
+---------+---------+--------------+----------------+--------------------+
|shop_date|shops_day|total_shop_vol|cum_sum_shop_vol|    cum_pct_shop_vol|
+---------+---------+--------------+----------------+--------------------+
| 20221110|      884|         29362|             884|0.030106940944077377|
| 20221111|      726|         29362|            1610| 0.05483277705878346|
| 20221112|      743|         29362|            2353| 0.08013759280702949|
| 20221113|      702|         29362|            3055| 0.10404604590967918|
| 20221114|      774|         29362|            3829| 0.13040664804849805|
| 20221115|      970|         29362|            4799| 0.16344254478577755|
| 20221116|     1455|         29362|            6254| 0.21299638989169675|
| 20221117|     1320|         29362|            7574| 0.25795245555479873|
| 20221118|     1181|         29362|            8755| 0.29817451127307404|
| 20221119|     1026|         29362|            9781|  0.3331176350384851|
| 20221120|     1171|         29362|           10952| 0.37299911450173695|
| 20221121|      950|         29362|           11902|  0.4053538587289694|
| 20221122|     1256|         29362|           13158|   0.448130236359921|
| 20221123|     1476|         29362|           14634| 0.49839929160138957|
| 20221124|     1384|         29362|           16018|  0.5455350452966419|
| 20221125|     1466|         29362|           17484|   0.595463524283087|
| 20221126|     1941|         29362|           19425|  0.6615693753831483|
| 20221127|     1678|         29362|           21103|  0.7187180709760915|
| 20221128|     1791|         29362|           22894|  0.7797152782508003|
| 20221129|     2001|         29362|           24895|  0.8478645868810026|
| 20221130|     2075|         29362|           26970|  0.9185341597983788|
| 20221201|     2392|         29362|           29362|                 1.0|
+---------+---------+--------------+----------------+--------------------+
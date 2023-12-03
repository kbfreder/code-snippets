

# converting between
- date to timestamp
df = df.withColumn("date_ts", F.col("date").cast("timestamp"))


- timestamp to date
df = df.withColumn("date", F.to_date("date_ts"))


- string to date
    - pyspark < 3.0
```py
df.registerTempTable("data")
df = spark.sql("""
    SELECT *,
        TO_DATE(CAST(UNIX_TIMESTAMP(CAST(out_departure_date AS string), 'yyyyMMdd') AS TIMESTAMP)) AS outDeptDt_dt,
        TO_DATE(CAST(UNIX_TIMESTAMP(CAST(shop_date AS string), 'yyyyMMdd') AS TIMESTAMP)) AS shopDate_dt
    FROM data
""")
```

- long to timestamp
df_tmp = df.withColumn("shop_req_ts", F.col("shop_req_long").cast("timestamp"))
df_tmp.select("shop_req_long", "shop_req_ts").show()
+------------------+-------------------+
|     shop_req_long|        shop_req_ts|
+------------------+-------------------+
|        1676525647|2023-02-16 05:34:07|
|        1676532158|2023-02-16 07:22:38|
|        1676532246|2023-02-16 07:24:06|
|        1676535475|2023-02-16 08:17:55|
|        1676530035|2023-02-16 06:47:15|
|        1676534687|2023-02-16 08:04:47|
|        1676534687|2023-02-16 08:04:47|
|        1676538727|2023-02-16 09:12:07|
|        1676532158|2023-02-16 07:22:38|


- timestamp to long
df = df.withColumn("epoch_seconds", F.col("timestamp").cast("long"))


- hour (month, day) from timestamp:
`              .withColumn("shop_hour", F.hour("shop_req_ts"))`




# date math

- difference between two dates
df_mod = df.withColumn('days_til_dept', F.datediff(
                        F.col('outDeptDt_dt'), F.col('shopDate_dt'))
                    )

- adding a constant number of days to a date
df_mod = df.withColumn('next_day', F.date_add(
                        F.col('date'), 1
                    ))

- adding date and integer column (where int rep's num days)
df_mod = (df
           .withColumn("dd_ts", F.to_timestamp("departure_date_dt"))
           .withColumn("return_date_dt", 
                                  F.expr("date_add(dd_ts, los)")
                      )
          )
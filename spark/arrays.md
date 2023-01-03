import pyspark.sql.functions as F



# get an element of an array
df.withColumn("first_out_cxr", F.col("out_marketing_cxr")[0])

# explode array to cols
- I think you have to do this manually
    - use above to extract each element of an array, sending to a new column
    - this isn't very elegant when the size of the array isn't consistent between records

# explode ararray to rows
```python
df_expl = df.select("*", F.explode("request_PTC").alias("requ_ptc_single"))
```
- see also `explode_outer` function

- and match position
```scala
import org.apache.spark.sql.functions._  

val df2 = (df
    .select("*", posexplode(col("responsePTC")) as Seq("ptc_pos", "PTC"))
    .select("*", posexplode(col("fareBreakDownByPTC")) as Seq("fare_pos", "farePTC"))
    .filter(col("ptc_pos") === col("fare_pos"))
    .drop("ptc_pos", "fare_pos")
    .select("id", "PTC", "farePTC")
    )
```

# Passing Array to Spark Lit function
- ref: https://stackoverflow.com/questions/49683897/passing-array-to-spark-lit-function

- e.g. you want to test for the overlap between an array column and a defined list of values
    - note: instead of `F.size(F.array_intersect(...))`, could use `F.array_overlap` in Spark 3
```python
BUDGET_CXRS = ['NK', 'F9']
df_ow_mf = df_ow_mf.withColumn("out_cxr_is_budget", F.size(F.array_intersect(F.col("out_cxrs"), F.array([F.lit(x) for x in BUDGET_CXRS]))) > 0)
```


# convert array element dtype
```python
# this is an array of int's
df.select("out_flight_numbers").printSchema()
> 
|-- out_flight_numbers: array (nullable = true)
 |    |-- element: integer (containsNull = true)

# convert to an array of str's
df = df.withColumn("out_flight_nos_str", F.col("out_flight_numbers").cast('array<string>'))

df.select("out_flight_nos_str").printSchema()
>
 |-- out_flight_nos_str: array (nullable = true)
 |    |-- element: string (containsNull = true)
```


# zip two arrays
- note both arrays must be strings
df = df.withColumn("out_cxr_fn_zip", F.arrays_zip(F.col("out_marketing_cxr"), F.col("out_flight_nos_str"))

- ...and then concat them
df = df.withColumn('out_zip_concat', F.expr("transform(out_cxr_fn_zip, x -> concat_ws('-', x.out_marketing_cxr, x.out_flight_nos_str))"))
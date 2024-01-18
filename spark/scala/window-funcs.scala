import org.apache.spark.sql.expressions.Window


val windowSpec  = Window.partitionBy("department").orderBy("salary")
df.withColumn("row_number",row_number.over(windowSpec))
  .show()

// window partitioned by a list
val w1 = Window.partitionBy(groupby_cols.map(col(_)):_*)
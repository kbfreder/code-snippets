

// count if null

## python
df2.select(F.col("solution_counts").isNull).count()

## scala
df2.select(col("solution_counts").isNull).count()


// filter in list

val pos_list: Array[String] = Array("US", "GB", "HK", "RU", "CA", "IN", "TW", "DE", "AU", "TH", "JP", "KR", "PH", "ES", "IT", "FR", "IL", "MY", "AE", "PT")

val df2_filt = df2.filter(col("pos_decoded") isin(pos_list: _*))
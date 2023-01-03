
- array to rows

val df2 = (df
    .select("*", posexplode(col("responsePTC")) as Seq("ptc_pos", "PTC"))
    .select("*", posexplode(col("fareBreakDownByPTC")) as Seq("fare_pos", "farePTC"))
    .filter(col("ptc_pos") === col("fare_pos"))
    .drop("ptc_pos", "fare_pos")
    .select("id", "PTC", "farePTC")
    )


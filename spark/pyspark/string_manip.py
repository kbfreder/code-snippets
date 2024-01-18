
F.concat_ws(
    "-",
    F.col("s_outOriginAirport").cast(StringType()), 
    F.col("s_outDestinationAirport").cast(StringType())
)
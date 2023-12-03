

# splitting a string:
'AGENCY-PCC' col is of format: "M|067D"

```python
pcc_df_split = (pcc_df
          .withColumn("pcc_split", F.split(F.col("AGENCY - PCC"), "\|"))
          .withColumn("pcc", F.col("pcc_split").getItem(1))
         )
```

# trimming a string, 
    - e.g. remove last X char's
```python
ex_df_expl = ex_df_expl.withColumn("requ_ptc_trim", 
                                   F.expr("substring(requ_ptc_, 1, length(requ_ptc_) - 1)")
                                  )
+---------+-------------+
|requ_ptc_|requ_ptc_trim|
+---------+-------------+
|     ADT1|          ADT|
|    XADT1|         XADT|
```

# combining strings

df_mod = df.withColumn("combined_strings", F.concat_ws("-", "string_col1", "string_col2"))
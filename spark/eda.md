

# count if null

```python
df2.select(F.col("solution_counts").isNull).count()
```

```scala
df2.select(col("solution_counts").isNull).count()
```

# filter value



## column value contains string

```python
df.filter(F.col("url").contains('google.com'))
```
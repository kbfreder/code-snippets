

To shuffle a df:
```python
train_shuffled = train.orderBy(F.rand())
```


Map a dictionary to a column in spark:

```python
from itertools import chain
import pyspark.sql.functions as F

    gds_conversion_dict = {
        "SAB": "1S",
        "AMA": "1A",
        "TP": "1G"
    }
    mapping_expr = F.create_map([F.lit(x) for x in chain(*gds_conversion_dict.items())])
    
    # Spark >= 2.0, < 3.0
    pcc_df = pcc_df.withColumn("gds", mapping_expr.getItem(F.col("AGENCY - GDS")))
    
    # Spark >= 3.0
    pcc_df = pcc_df.withColumn("gds", mapping_expr[F.col("AGENCY - GDS")])
```
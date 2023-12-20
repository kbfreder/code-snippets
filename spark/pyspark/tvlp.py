
from datetime import datetime, timedelta

import pyspark.sql.functions as F
import pyspark.sql.types as T
from pyspark.sql.window import Window


# assign group number based when a boolean column changes from 0 --> 1

w_grp = (Window
    .partitionBy(keys)
    .orderBy(time_col)
    )

df_grp = df.withColumn("grp_num", 
                            F.sum((F.col("bool_col") == 1).cast("int")).over(w_grp))


"""
df_grp.show()

>
bool_col    grp_num
0           0
0           0
0           0
1           1
0           1
0           1
1           2
0           2
...

"""


# split one array based on another
"""
Here, 'AP_in_days' and 'lifetimes_in_min' and 'timestamps' are index-matched
array columns. We want to split them into "buckets" based on AP.

i.e. get lifetimes where AP is between 4,16
"""

def spilt_ap_by_bucket(df_lft, ap_buckets):
    """Splits lifetimes into AP buckets. Filters out 0 lifetimes and does not
    return empty buckets.
    """
    df_ap_lft_zip = df_lft.withColumn(
            "AP_lft_zip", F.arrays_zip(F.col("AP_in_days"), 
                                       F.col("lifetimes_in_min"), 
                                       F.col("timestamps"))
        )
    
    @F.udf(returnType=(T.ArrayType(T.StructType([
        T.StructField('bucket', T.ArrayType(T.IntegerType())), 
        T.StructField('lifetimes', T.ArrayType(T.FloatType())),
        T.StructField('shop_days', T.ArrayType(T.DateType()))
    ]))))
    def split_ap(zip_arr):
        if len(zip_arr) > 0:
            bkt_lft_zip = []
            for bucket in ap_buckets:
                bkt_lfts = [lft for ap, lft, _ in zip_arr if (ap >= bucket[0]) & (ap < bucket[1])]
                filt_lfts = [float(lft) for lft in bkt_lfts if lft != 0]
                
                ts_list = [ts for ap, lft, ts in zip_arr if (ap >= bucket[0]) & (ap < bucket[1]) & (lft != 0)]
                bkt_sds = list(set([datetime.fromtimestamp(ts).date() for ts in ts_list]))
                
                if len(filt_lfts) > 0:
                    bkt_lft_zip.append([bucket, filt_lfts, bkt_sds])
            
            if len(bkt_lft_zip) > 0:
                return bkt_lft_zip
            else:
                return None
        else:
            return None

    df_split = (df_ap_lft_zip
                .withColumn(f"AP_bucket_lft_zip", split_ap("AP_lft_zip"))
                .drop("AP_lft_zip")
    )
    return df_split

## Note: we then split out these arrays: first into rows, then into columns
def explode_ap(df_ap_bucket):
    df_ap_expl = (df_ap_bucket
                  .drop("shop_days") # get rid of key-level list
                  # explode array --> rows
                  .select("*", F.explode("AP_bucket_lft_zip").alias("AP_bucket_lft"))
                  # explode map --> columns
                  .withColumn("AP_bucket", F.col("AP_bucket_lft").getItem("bucket"))
                  .withColumn("lifetimes", F.col("AP_bucket_lft").getItem("lifetimes"))
                  .withColumn("shop_days", F.col("AP_bucket_lft").getItem("shop_days"))
                  # no longer need original array or map columns
                  .drop("AP_bucket_lft_zip", "AP_bucket_lft", "lifetimes_in_min", 
                        # "APs_in_days", # keep this?
                        )
                  # rename, so it's the same as the base model
                  .withColumnRenamed("lifetimes", "lifetimes_in_min")
    )
    return df_ap_expl  

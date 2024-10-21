
from datetime import datetime, timedelta


# Dates
from dateutil.relativedelta import relativedelta

now_date = datetime.today()
past_date = now_date - relativedelta(months=3)



# print datetime in local TZ
from zoneinfo import ZoneInfo

utc = ZoneInfo('UTC')
localtz = ZoneInfo('US/Mountain')

fit_start = datetime.now()
print(f"Starting at {fit_start.astimezone(localtz).strftime('%Y-%m-%d %H:%M')} local time")


# TIME SOMETHING
# =====================
start_time = datetime.now()
#<do the thing>
end_time = datetime.now()
elapsed_time = (end_time - start_time)/timedelta(min=1)
print(f"That took {elapsed_time:.2f} minutes")


# using tqdm




# CONVERTING DATA TYPES
# =====================

# Date from datetime
    # use .date() method:
DATE_FORMAT = "%Y-%m-%d"
shop_start_str = "2022-09-20" #args.shop_start
shop_start_dt = datetime.datetime.strptime(shop_start_str, DATE_FORMAT).date()
shop_start_dt
> datetime.date(2022, 9, 20)

# month from full date
## this works, but results in a weird data type
df1['visit_month_date'] = pd.to_datetime(df1['VISIT_DATE']).dt.to_period('M')

## hacky but works. if you want/need a datetime object
outbound_sms_df['month'] = outbound_sms_df['date'].apply(lambda dt: datetime(dt.year, dt.month, 1))

## if a string works
outbound_sms_df['month_str'] = outbound_sms_df['date'].apply(lambda dt: dt.strftime("%Y-%m"))


# LOOPING OVER TIME
# =====================
# Loop over days, given start & end date
shop_start_str = args.shop_start
shop_end_str = args.shop_end

start_dt = datetime.datetime.strptime(shop_start_str, "%Y-%m-%d")
end_dt = datetime.datetime.strptime(shop_end_str, "%Y-%m-%d")
num_days = (end_dt - start_dt).days
date_list = [start_dt + datetime.timedelta(days=x) for x in range(num_days + 1)]

for date in date_list:
    # do stuff



# Loop over months, given start & end date
date_start_str = args.date_start
date_end_str = args.date_end

start_dt = datetime.datetime.strptime(date_start_str, "%Y-%m")
end_dt = datetime.datetime.strptime(date_end_str, "%Y-%m")
num_months = relativedelta(end_dt, start_dt).months

for i in range(num_months):
        month_date = start_dt + relativedelta(months=+i)


# Loop over months, given end date & num months

    date_end_str = args.last_date
    num_months = args.num_months

    end_dt = datetime.datetime.strptime(date_end_str, "%Y-%m")
    start_dt = end_dt - relativedelta(months=num_months)

    for i in range(num_months):
        month_dt = start_dt + relativedelta(months=+i)


# convert date types


# month from full date
## this works, but results in a weird data type
df1['visit_month_date'] = pd.to_datetime(df1['VISIT_DATE']).dt.to_period('M')

## hacky but works. if you want/need a datetime object
outbound_sms_df['month'] = outbound_sms_df['date'].apply(lambda dt: datetime(dt.year, dt.month, 1))

## if a string works
outbound_sms_df['month_str'] = outbound_sms_df['date'].apply(lambda dt: dt.strftime("%Y-%m"))


# week
## week number: can use isocalendar, I think?

## date


def get_week(d):
    """returns date of Sunday of that week"""
    wkday = d.weekday()
    if wkday == 6:
        return d
    else:
        return d - timedelta(days=wkday+1)



# ================================
# SPARK
# ================================
## long to datetime
    # eStreaming data has dates saved as long int's

df_mod = df.withColumn("out_departure_date_dt", F.to_date(F.col("out_departure_date").cast('string'), 'yyyyMMdd'))
> """
+------------------+---------------------+
|out_departure_date|out_departure_date_dt|
+------------------+---------------------+
|          20231026|           2023-10-26|
|          20231102|           2023-11-02|
|          20230929|           2023-09-29|
|          20230930|           2023-09-30|
|          20230927|           2023-09-27|
|          20230915|           2023-09-15|
|          20231019|           2023-10-19|
|          20230911|           2023-09-11|
|          20230921|           2023-09-21|
|          20230905|           2023-09-05|
+------------------+---------------------+
"""

## datetime to unix timestamp
df_mod2 = df_mod.withColumn("out_departure_date_ts", F.unix_timestamp(F.col("out_departure_date_dt")))
> """
+---------------------+---------------------+
|out_departure_date_dt|out_departure_date_ts|
+---------------------+---------------------+
|           2023-10-26|           1698278400|
|           2023-11-02|           1698883200|
|           2023-09-29|           1695945600|
|           2023-09-30|           1696032000|
|           2023-09-27|           1695772800|
|           2023-09-15|           1694736000|
|           2023-10-19|           1697673600|
|           2023-09-11|           1694390400|
|           2023-09-21|           1695254400|
|           2023-09-05|           1693872000|
+---------------------+---------------------+
"""

## unix timestamp to datetime
F.from_unixtime()


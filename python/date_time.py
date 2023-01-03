



# Dates
from datetime import datetime
from dateutil.relativedelta import relativedelta

now_date = datetime.today()
past_date = now_date - relativedelta(months=3)


# Date from datetime
    # use .date() method:
DATE_FORMAT = "%Y-%m-%d"
shop_start_str = "2022-09-20" #args.shop_start
shop_start_dt = datetime.datetime.strptime(shop_start_str, DATE_FORMAT).date()
shop_start_dt
> datetime.date(2022, 9, 20)
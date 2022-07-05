



# Dates
from datetime import datetime
from dateutil.relativedelta import relativedelta

now_date = datetime.today()
past_date = now_date - relativedelta(months=3)
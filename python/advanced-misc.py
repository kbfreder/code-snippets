

# cross join
# must add a 'key' column, join on this
stay_dur_pdf = pd.DataFrame([x for x in range(30)], columns=['stay_duration'])
stay_dur_pdf['key'] = 0

dtd_pdf = pd.DataFrame([x for x in range(120)], columns=['days_til_dept'])
dtd_pdf['key'] = 0


date_cross_pdf = dtd_pdf.merge(stay_dur_pdf, on='key', how='outer')


# WINDOW FUNCTION EQUIVALENT
# lag within a group
iter_dt_df['min_fare_prev_day'] = (iter_dt_df
                                              .sort_values(by=['inDeptDt'])
                                              .groupby(['searchDt'])['min_fare']
                                              .shift(1)
                                             )

# trailing mean within a group
df['trailing_avg'] = (
    df
    .sort_values(by='')
)

# cumulative sum 
df['cum_pct_x'] = df['x'].cumsum()
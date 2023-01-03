# WINDOW FUNCTION EQUIVALENT

# lag within a group
iter_dt_df['min_fare_prev_day'] = (iter_dt_df
                                              .sort_values(by=['inDeptDt'])
                                              .groupby(['searchDt'])['min_fare']
                                              .shift(1)
                                             )

# rank within a group
dtd_grp['dtd_rank'] = dtd_grp.groupby("days_til_dept")['count'].rank(method='dense', ascending=False)


# sum within a group
df['grp_sum'] = df.groupby('key')['count'].transform('sum')


# trailing mean within a group
df['trailing_avg'] = (
    df
    .sort_values(by='')
)

# cumulative sum 
df['cum_pct_x'] = df['x'].cumsum()
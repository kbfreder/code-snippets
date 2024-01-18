# WINDOW FUNCTION EQUIVALENT

# lag within a group
iter_dt_df['min_fare_prev_day'] = (iter_dt_df
                                    .sort_values(by=['inDeptDt'])
                                    .groupby(['searchDt'])
                                    ['min_fare']
                                    .shift(1)
                                    )

# rank within a group
dtd_grp['dtd_rank'] = (dtd_grp
                        .groupby("days_til_dept")
                        ['count']
                        .rank(method='dense', ascending=False)
)


# sum within a group
df['grp_sum'] = df.groupby('key')['count'].transform('sum')


# rolling or trailing mean within a group
    # https://stackoverflow.com/questions/53339021/python-pandas-calculate-moving-average-within-group
    # rolling: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.rolling.html
df['trailing_avg'] = (df
    .sort_values(by='') # optional
    .groupBy('key')
    .rolling(window_size)['target'].mean().reset_index(drop=True)
)

## to do a trailing mean, set window size equal to max value for trailing dimension


# min or max of previous or future instances


# cumulative sum 
df['cum_pct_x'] = df['x'].cumsum()
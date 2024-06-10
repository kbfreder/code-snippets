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

# cum pct in group
df['total'] = df.groupby('group')['value'].transform(pd.Series.sum)
df['cum_sum'] = df.groupby('group')['value'].transform(pd.Series.cumsum)
df['cum_pct'] = df['cum_sum'] / df['total'] * 100


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


# first
## this isn't a window function -- it returns one value per group
##  have to map back

## using `first.()` results in a Series where the index is the `groupby` group id's
first_srs = (donor_union_df
          .sort_values(by=['date', 'first_date'])
          .groupby('donor_number')
            ['event_type'].first()
      )
df_first = pd.DataFrame(first_srs)
df_first.columns = ['first_event']
df_first.reset_index(inplace=True)
df_first.rename(columns={'index': 'donor_number'}, inplace=True)

donor_agg = donor_agg.merge(df_first, on='donor_number')

## using `nth(0)` results in a Series where the index is the index of the row in the original 
## dataset. Harder to map back to something useful
first_event = donor_union_df.groupby('donor_number')['event_type'].nth(0)

## alt syntax
first = grouped.agg(lambda x: x.iloc[0])
last = grouped.agg(lambda x: x.iloc[-1])

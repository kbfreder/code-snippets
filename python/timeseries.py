# =======================================
# ROLLING AVERAGES
# =======================================

# if your data is already "dense" -- i.e. every `id` has an entry for every `date`,
# then it's easy:
df = df.sort_values(by=[id_col, date_col])
df.groupby(id_col)[col_to_tally].rolling(window=x).mean()


# if you need to interpret dates...

# sum over calendar week
## in this example, `df` contains one row per event, with an `id` col and a `date` col
## so we count on a random other column from the dataframe
ts_idx_df = df.set_index(keys=date_col)
ts_agg_df = (ts_idx_df
             .groupby([id_col, pd.Grouper(freq='W')])
             [rando_col].count()
             .reset_index()
             .rename(columns={rando_col: 'num_events'})
            )

# opt: pivot to get a time series matrix, where index = ID and columns = week
id_ts_mtx = ts_agg_df.pivot(index=id_col, columns=date_col, values='num_events').fillna(0)


# rolling average:
## first, 
ra_df = (df.set_index(keys=date_col)
       .groupby(id_col)[col_to_tally]
       .apply(lambda x: x.asfreq('1D').rolling('28D').mean())
       .reset_index()
      )
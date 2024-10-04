

# cross join
# must add a 'key' column, join on this
stay_dur_pdf = pd.DataFrame([x for x in range(30)], columns=['stay_duration'])
stay_dur_pdf['key'] = 0

dtd_pdf = pd.DataFrame([x for x in range(120)], columns=['days_til_dept'])
dtd_pdf['key'] = 0


date_cross_pdf = dtd_pdf.merge(stay_dur_pdf, on='key', how='outer')


# add "group numbers" to events
## ex: have timeseries data of different kinds of events
## want to number event type A consecutively, and apply these 
## numbers to all events in between. (useful for computing time
## between previous event A and any event B)
df['donation_grp_num'] = (df['is_donation'].eq(1)
                          .groupby(df['donor_number'])
                          .cumsum()
                            )


# number "groups" by consecutive indicators
## ex: have time series of A,A,A,A,B,B,A,A,A
## group numbers would be: 1,1,1,1,2,2,3,3,3
dtns_df['camp_pd_id'] = (dtns_df.groupby('donor_number')
                         ['during_campaign'].transform(lambda x: (x != x.shift()).cumsum())
                        )
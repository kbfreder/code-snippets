

# cross join
# must add a 'key' column, join on this
stay_dur_pdf = pd.DataFrame([x for x in range(30)], columns=['stay_duration'])
stay_dur_pdf['key'] = 0

dtd_pdf = pd.DataFrame([x for x in range(120)], columns=['days_til_dept'])
dtd_pdf['key'] = 0


date_cross_pdf = dtd_pdf.merge(stay_dur_pdf, on='key', how='outer')



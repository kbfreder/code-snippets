


# subplot
    # num_rows, num_cols
fig, _ = plt.subplots(2,1, figsize=(12, 10))
plt.subplot(2,1,1)
plt.plot(...)

plt.subplot(2,1,2)
plt.plot(...)


# get a nice linear sequence of colors from a color map:
import matplotlib.cm as cm

ranks = [1,10,20,50]
cmap_name = "viridis_r"
colors = [cm.get_cmap(cmap_name)(x) for x in np.linspace(0, 1, len(ranks))]

plt.figure(figsize=(8,5))
for i, rank in enumerate(ranks):
    rank_pdf = df[df['rank'] == rank]
    market = rank_pdf['market'].unique()[0]
    shops = rank_pdf['avgCounts'].unique()[0]
    plt.scatter(rank_pdf['days_til_dept'], rank_pdf['avg_coverage'],
                c=[colors[i]], alpha=0.5,
                label=f"{rank} - {market} ({shops:,.0f})",
             )
    plt.xlabel("days until departure")
    plt.ylabel("avg coverage")
    plt.legend()
    plt.title(f"Average Coverage - LOS 1-7 days");



# overlay two plots -- different y-axes
data_bar = pdf_shop_cnts_by_dtd['sum_shop_counts']
labels = pdf_shop_cnts_by_dtd['days_til_dept']
data_line = pdf_shop_cnts_by_dtd['cum_pct']
xs = np.arange(len(data_bar))

fig, ax = plt.subplots(figsize=(10,5))
ax.bar(xs, data_bar);
ax.set_xticks(xs[4::5])
ax.set_xticklabels(labels[4::5]) #, rotation=90)
ax.set_ylabel("shop volume")

ax2 = ax.twinx()
ax2.plot(xs, data_line, marker="o", color="red")
ax2.set_ylim(0, 1)
ax2.set_ylabel("Cumulative % Total Shop Volume")

plt.title("Distribution of shopping volumes by days 'til dept");

# give the legend a title
plt.legend("title"="Days")


# get bins from plt.hist:
counts, bins, fig = plt.hist(data)
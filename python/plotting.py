# BAR GRAPHS
# ----------------------------------
# bar graph of 2 entities side-by-side
xs = np.arange(len(data_to_plot))
w = 0.4

labels = data_to_plot['label_col']
color1 = 'lightblue'
color2 = 'grey'

plt.figure(figsize=(12,4))
plt.bar(xs, data_to_plot['data1'], 
        width=w, color=color1, label="individual models")
plt.bar(xs+w, data_to_plot['data2'], width=w, color=color2, label="one model")

plt.xticks(xs, labels)
plt.xlabel()
plt.xticks(rotation=90)

plt.legend();
plt.ylabel("MAE")
plt.title("Lead Price Archive data - with carriers");


# stacked bar graph
## use `bottom` keyword

## example here is more complex then may be necesary, because datasets aren't equal in length
plt.figure(figsize=(8,4))

base_data = df['total_num_emails_sent'].value_counts().sort_index()
bottom = np.zeros_like(base_data)
plt.bar(base_data.index, base_data, label="total")
bottom += base_data.values

for label in ['bonus', 'nudge']:
    col = f'num_{label}_emails'
    data = df[col].value_counts().sort_index()
    if data.index[0] == 0: # could make this adaptive
        data = data[1:]

    data_bottom = [bottom[list(base_data.index).index(di)] for di in data.index]
    plt.bar(data.index, data, bottom=data_bottom, label=label)

    for (di, val) in zip(data.index, data.values):
        bottom[list(base_data.index).index(di)] += val

plt.xticks(base_data.index, base_data.index)   
plt.ylabel('num donor-contacts')
plt.xlabel('num emails received in month')
plt.legend();


# ============================================
# SUBPLOTS
# ============================================

# subplot
    # num_rows, num_cols
fig, _ = plt.subplots(2,1, figsize=(12, 10))
plt.subplot(2,1,1)
plt.plot(...)

plt.subplot(2,1,2)
plt.plot(...)


# share axes
## note: cannot use plt.subplot, must use axs[i]
fig, axs = plt.subplots(top_n_cxr, 1, sharex=True, sharey=True, figsize=(10,7))
for i, cxr in enumerate(plot_data[cxr_col].unique()):
    cxr_data = plot_data[plot_data[cxr_col] == cxr]

    axs[i].bar(-cxr_data['days_til_dept'], cxr_data['pct_dtd_count'], color=colors[i], label=cxr)
    axs[i].legend()
    if i == top_n_cxr-1:
        axs[i].set_xlabel("advance purchase days")
    else:
        plt.xlabel("")

fig.suptitle(market);
fig.tight_layout();



# getting plots to go down first (vs across first)
num = 5  # total number of data to plot
num_cols = 2
num_rows = int(num/num_cols)

plot_idx = [i for i in range(num) if i % 2 == 1] + [i for i in range(2, num+2) if i % 2 == 0]

plt.clf()
fig, _ = plt.subplots(num_rows, num_cols, figsize=(7*num_cols, 2.5*num_rows), sharey=True)

for i, data in enumerate(data_list):
    plt.subplot(num_rows, num_cols, plot_idx[i]) 
    ...


# one title per row
## https://stackoverflow.com/questions/27426668/row-titles-for-matplotlib-subplot
fig, big_axes = plt.subplots( figsize=(15.0, 15.0) , nrows=3, ncols=1, sharey=True) 

for row, big_ax in enumerate(big_axes, start=1):
    big_ax.set_title("Subplot row %s \n" % row, fontsize=16)

    # Turn off axis lines and ticks of the big subplot 
    # obs alpha is 0 in RGBA string!
    big_ax.tick_params(labelcolor=(1.,1.,1., 0.0), top='off', bottom='off', left='off', right='off')
    # removes the white frame
    big_ax._frameon = False


for i in range(1,10):
    ax = fig.add_subplot(3,3,i)
    ax.set_title('Plot title ' + str(i))

fig.set_facecolor('w')
plt.tight_layout()
plt.show()



# share x or y axis, but repeat tick labels

## for yaxis:
fig, axs = plt.subplots(1,2,figsize=(10,4), sharey=True)
...
## after 2nd plot:
axs[1].yaxis.set_tick_params(which='both', labelleft=True)

## for xaxis sharing:
fig, axs = plt.subplots(2,1,figsize=(10,4), sharex=True)
...
## after 2nd plot:
axs[1].xaxis.set_tick_params(which='both', labelbottom=True)


# adjust width ratio of subplots
fig, axs = plt.subplots(1,2,figsize=(10,4), sharey=True, gridspec_kw={'width_ratios':[2,1]})


# ===========================
# COLORS
# ===========================

# -----------------
# get a nice linear sequence of colors from a color map:
# import matplotlib.cm as cm
import matplotlib as mpl

ranks = [1,10,20,50]
cmap_name = "viridis_r"
# colors = [cm.get_cmap(cmap_name)(x) for x in np.linspace(0, 1, len(ranks))]
colors = [mpl.colormaps.get_cmap(cmap_name)(x) for x in np.linspace(0, 1, len(ranks))]


plt.figure(figsize=(8,5))
for i, rank in enumerate(ranks):
    ...
    plt.scatter(xs, ys,
                c=[colors[i]]
                )


# use sequence of Qualitative color map
colors = iter([plt.cm.tab20(i) for i in range(20)])
...
plt.scatter(x, y, c=next(colors))


# ===========================
# LAYOUT
# fig suptitle displays on top of subplot title
fig.suptitle("this is kind of annoying", y=1.05)


# -----------------
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


# do the above, but get everything in one legend
fig, ax = plt.subplots(figsize=(8,4))
p1 = ax.bar(pdf['bucket'], pdf['base_err_rate'], label='bucket error rate')
...
p2 = ax.hlines(oa_avg, *plt.xlim(), linestyle='--', color='k', label='overall error rate')

ax2 = ax.twinx()
p3 = ax2.scatter(pdf['bucket'], pdf['base_avg_daily_shops'], s=6, c='r', label='num shops')
...

ps = [p1, p2, p3]
labels = [p.get_label() for p in ps]
ax.legend(ps, labels)

# -----------------
# give the legend a title
plt.legend(title="Days")

# -----------------
# get bins from plt.hist:
counts, bins, fig = plt.hist(data)

# ----------------
# hide ticks
plt.plot(range(10)) # your plotting code goes here
plt.tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom=False,      # ticks along the bottom edge are off
    top=False,         # ticks along the top edge are off
    labelbottom=False) # labels along the bottom edge are off


# ---------------
# plot a diagonal line of y=x
plt.plot(plt.xlim(), plt.ylim(), ls='--')

# ---------------
# hide unused subplots
    ## this assumes all the blank plots are in the last row
num_blank_plots = (n_rows*n_cols) - i
if num_blank_plots > 0:
    for j in range(num_blank_plots):
        fig.delaxes(axs[n_rows-1][n_cols-(j+1)])


# ----------------
# make your own legend
## see overlay plot above for one way




# SEABORN
# =======================

# setting figure size

## some methods are Axes-level:
fig, ax = plt.subplots(figsize=(8,5))
sns.distplot(..., ax=ax)

## others are figure-level:
sns.catplot(data=..., height=5, aspect=1.3)


# heatmap handy settings
sns.heatmap(data, 
            cmap="viridis", 
            cbar_kws={"shrink": 0.5, "label": "min"},
            square=True,
            annot=True
            )

# using seaborn with `ax` interface
ax1 = fig.add_subplot(n,2,(i*2)+1)
sns.heatmap(data, ax=ax1)
ax1.set_title("Lifetime")
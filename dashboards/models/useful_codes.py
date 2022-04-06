rcParams['figure.figsize'] = 9, 7
font = { 'size'   : 9}
matplotlib.rc('font', **font)


# Some useful functions
def plot_raw_polls(df, filename, heading=None):
	import datetime
	fig, ax = plt.subplots(figsize=(12, 5))
	
	min_date = None
	max_date = None
	for col_name in df.columns.values:
		
		# plot the column
		col = df[col_name]
		col = col[col.notnull()] # drop NAs
		dates = df.index
		ax.plot_date(x=dates, y=col, fmt='-', label=col_name,
			tz=None, xdate=True, ydate=False, linewidth=1.5)
		
		# establish the date range for the data
		if min_date:
			min_date = min(min_date, min(dates))
		else:
			min_date = min(dates)
		if max_date:
			max_date = max(max_date, max(dates))
		else:
			max_date = max(dates)
			
	# give a bit of space at each end of the plot - aesthetics
	span = max_date - min_date
	extra = int(span.days * 0.03) * datetime.timedelta(days=1)
	ax.set_xlim([min_date - extra, max_date + extra])
	
	# format the x tick marks
	ax.xaxis.set_major_formatter(DateFormatter('%Y'))
	ax.xaxis.set_minor_formatter(DateFormatter('\n%b'))
	ax.xaxis.set_major_locator(YearLocator())
	ax.xaxis.set_minor_locator(MonthLocator(bymonthday=1, interval=2))
	
	# grid, legend and yLabel
	ax.grid(True)
	ax.legend(loc='best', prop={'size':'large'})
	ax.set_ylabel('% das intenções')
	
	# heading
	if heading:
		fig.suptitle(heading, fontsize=18)
	fig.tight_layout(pad=1.5)
	
	# footnote
	fig.text(0.99, 0.00, 'JOTA Labs', ha='right', 
		va='bottom', fontsize=8, color='#999999')
	
	# save to file
	fig.savefig(filename, dpi=125)
	
# plot_raw_polls(data[["Bolsonaro"]], "raw_polls")
	
	


	
def dates_to_idx(timelist):
	"""Convert datetimes to numbers in reference to a given date"""
	import numpy as np
	
	reference_time = timelist[0]
	t = (timelist - reference_time) / np.timedelta64(1, "W")
	
	return np.asarray(t)


def standardize(series):
	"""Standardize a pandas series"""
	return (series - series.mean()) / series.std()
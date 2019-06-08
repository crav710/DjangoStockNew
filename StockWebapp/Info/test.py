import sqlite3 
import pandas as pd
import os 
import matplotlib.pyplot as plt
from mpl_finance import candlestick2_ochl,candlestick_ochl
import matplotlib.ticker as ticker
import datetime
from matplotlib.dates import  date2num,DateFormatter, WeekdayLocator, HourLocator,DayLocator, MONDAY
import matplotlib
def load_db(stock):
	Stock_data='StockData/Stocks_INFO_table.db'
	Stock_earning='StockData/Stocks_earning_loss_table.db'
	cnx = sqlite3.connect(Stock_data)
	stk_info = pd.read_sql_query("SELECT * FROM STOCKSINFO", cnx)
	cnx2=sqlite3.connect(Stock_earning)
	stk_earn=pd.read_sql_query("SELECT * FROM STOCKSLOSS", cnx2)
	print(stk_info)
	# print table for Stock 
	
	return stk_info,stk_earn

def load_database(stock):
	Stock_data='StockData/Stocks_INFO_table.db'
	Stock_earning='StockData/Stocks_earning_loss_table.db'
	cnx = sqlite3.connect(Stock_data)
	stk_info = pd.read_sql_query("SELECT * FROM STOCKSINFO", cnx)
	cnx2=sqlite3.connect(Stock_earning)
	stk_earn=pd.read_sql_query("SELECT * FROM STOCKSLOSS", cnx2)
	# print table for Stock 
	info_table=stk_info[stk_info['SYMBOL']==stock]
	earn_table=stk_earn[stk_info['SYMBOL']==stock]

	html_info=info_table.to_html()
	html_loss=earn_table.to_html()

	return html_info,html_loss


def load_json(stock):
	title='Plot the time, open, close, high, low as a vertical line ranging from low to high. Use a rectangular bar to represent the open-close span. If close >= open, use colorup="k" to color the bar, otherwise use colordown="r"'
	df=pd.read_json('AllStocks.json')
	df=df[df['Symbol']==stock]
	fig,ax=plt.subplots()
	df['Open']=pd.to_numeric(df['Open'])
	df['Low']=pd.to_numeric(df['Low'])
	df['High']=pd.to_numeric(df['High'])
	df['Date']=date2num(pd.to_datetime(df['Date']).tolist())
	new_df=df.copy()
	new_df=new_df[['Date','Open','Close','Low','High']]
	quotes = [tuple(x) for x in new_df.values]

	candlestick_ochl(ax,quotes)	
	ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%Y-%m-%d'))
	ax.grid(True)
	ax.set_xlabel('Dates')
	ax.set_ylabel('Price')

	fig_size = ax.rcParams["figure.figsize"]  
	# Set figure width to 12 and height to 9
	fig_size[0] = 35
	fig_size[1] = 25
	ax.rcParams["figure.figsize"] = fig_size

	plt.savefig('GOOG.png')

	plt.show()

def display_plots(info_table,earn_table):
	print(earn_table)
		# plot 1  SYMBOL vs NO_SHARES
	ax=info_table.plot(kind='bar',x='SYMBOL',y='NO_SHARES')
	ax.set_xlabel('SYMBOL')
	ax.set_ylabel('NO_SHARES')
	plt.show()
	# plt.savefig('') 
	# plot 2 SYMBOL vs Purchase price 
	ax=info_table.plot(kind='bar',x='SYMBOL',y='PURCHASE_PRICE')
	ax.set_xlabel('SYMBOL')
	ax.set_ylabel('Purchase Price ')
	plt.show()
	# plot 3 SYMBOL vs CURRENT_PRICE
	ax=info_table.plot(kind='bar',x='SYMBOL',y='CURRENT_PRICE')
	ax.set_xlabel('SYMBOL')
	ax.set_ylabel('CURRENT PRICE')
	plt.show()

	# plot 4  SYMBOL vs EARNING or LOSS 

	ax=earn_table.plot(kind='bar',x='SYMBOL',y='EARNING_LOSS')
	ax.set_xlabel('SYMBOL')
	ax.set_ylabel('EARNING_LOSS')
	plt.show()

	#  plot 5 SYMBOL vs Yearly Earning/ LOSS

	ax=earn_table.plot(kind='bar',x='SYMBOL',y='YEARLY_EARNING_LOSS')
	ax.set_xlabel('SYMBOL')
	ax.set_ylabel('YEARLY_EARNING_LOSS')
	plt.show()
	

	
	




if __name__ == '__main__':
	stock='GOOGL'
	info_table,earn_table=load_db(stock)
	display_plots(info_table,earn_table)


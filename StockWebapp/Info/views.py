from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from Info.forms import StockForm,StockInfoForm,StockGraph
import matplotlib.pyplot as plt
from mpl_finance import candlestick2_ochl,candlestick_ochl
import matplotlib.ticker as ticker
import datetime
from matplotlib.dates import  date2num,DateFormatter, WeekdayLocator, HourLocator,DayLocator, MONDAY
import matplotlib
import sqlite3
import pandas as pd 
import os
import csv
from Info.stockapi import load_stocks

# Create your views here.
def plot_graph(info_table,x_axis,y_axis):
	title='Graph Representing {} VS {}'.format(x_axis,y_axis)
	ax=info_table.plot(kind='bar',x=x_axis,y=y_axis)
	ax.set_xlabel(x_axis)
	ax.set_ylabel(y_axis)
	plot_name=y_axis
	cwd=os.getcwd()
	file_path1=os.path.join(cwd,'Info/static/images/{}.png'.format(plot_name))
	plt.savefig(file_path1)
	image_path='images/{}.png'.format(plot_name)
	return image_path,title


def index(request):
	images=[]
	titles=[]
	info_table,earn_table=load_db()
	# plot1 SYMBOL vs NO_SHARES
	image_file,title=plot_graph(info_table,'SYMBOL','NO_SHARES')
	images.append(image_file)
	titles.append(title)
	# plot 2 SYMBOL vs Purchase price
	image_file,title=plot_graph(info_table,'SYMBOL','PURCHASE_PRICE')
	images.append(image_file)
	titles.append(title)

	# plot 3 SYMBOL vs CURRENT_PRICE
	image_file,title=plot_graph(info_table,'SYMBOL','CURRENT_PRICE')
	images.append(image_file)
	titles.append(title)

	# plot 4  SYMBOL vs EARNING or LOSS 

	image_file,title=plot_graph(earn_table,'SYMBOL','EARNING_LOSS')
	images.append(image_file)
	titles.append(title)

	#  plot 5 SYMBOL vs Yearly Earning/ LOSS
	image_file,title=plot_graph(earn_table,'SYMBOL','YEARLY_EARNING_LOSS')
	images.append(image_file)
	titles.append(title)
	zipped_data=zip(titles,images)
	# print(zipped_data)
	context={
	'image_data':zipped_data
	}

	return render(request,'index.html',context=context)



def stock_graph_form(request):
	form=StockGraph()
	if request.method=="POST":
		form=StockGraph(request.POST)
		if form.is_valid():
			stock_symbol=form.cleaned_data['stock_symbol']
			print(stock_symbol)
			request.session['stock_symbol']=stock_symbol
			return HttpResponseRedirect(reverse('stock_graph'))
	context={
	'form': form,
	}
	return render(request,'graph_form.html',context)


def display_graph(request):
	title='''Plot Show the time, open, close, high, low as a vertical line ranging from low to high.
			 Use a rectangular bar to represent the open-close span. If close >= open, use colorup="k" to color the bar, otherwise use colordown="r"'''
	stock_symbol=request.session.get('stock_symbol')
	# print(stock_symbol)
	file_path1=load_json(stock_symbol)
	context={
		'title':title,
		'Stock_symbol':stock_symbol,
		'image_path':file_path1,
		}
	return render(request,'stock_graph.html',context)

def load_json(stock_symbol):
	cwd=os.getcwd()
	file_path1=os.path.join(cwd,'Info/AllStocks.json')
	df=pd.read_json(file_path1)
	# print(data)
	df=df[df['Symbol']==stock_symbol]
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

	file_path1=os.path.join(cwd,'Info/static/images/{}.png'.format(stock_symbol))
	
	# fig_size = plt.rcParams["figure.figsize"]  
	# # Set figure width to 12 and height to 9
	# fig_size[0] = 20
	# fig_size[1] = 15
	# plt.rcParams["figure.figsize"] = fig_size
	ax.xaxis_date()
	ax.autoscale_view()
	plt.setp( plt.gca().get_xticklabels(), rotation=25, horizontalalignment='right')
	plt.savefig(file_path1)
	# plt.savefig(file_path1)
	
	# plt.show()
	image_path='images/{}.png'.format(stock_symbol)

	return image_path





def stock_form(request):
	form=StockForm()
	if request.method=="POST":
		form=StockForm(request.POST)
		if form.is_valid():
			stock_symbol=form.cleaned_data['stock_symbol']
			print(stock_symbol)
			request.session['stock_symbol']=stock_symbol
			return HttpResponseRedirect(reverse('stock_page'))


	context={
	'form': form,
	}

	return render(request,'form.html',context)



def stock_detail_form(request):

	form=StockInfoForm()
	if request.method=="POST":
		form=StockInfoForm(request.POST)
		if form.is_valid():
			stock_symbol=form.cleaned_data['stock_symbol']
			share_count=form.cleaned_data['share_count']
			purchase_price=form.cleaned_data['purchase_price']
			current_price=form.cleaned_data['current_price']
			purchase_date=form.cleaned_data['purchase_date']
			purchase_date=str(purchase_date.month)+'/'+str(purchase_date.day)+'/'+str(purchase_date.year)
			row=[stock_symbol,share_count,purchase_price,current_price,purchase_date]
			cwd=os.getcwd()
			file_path1=os.path.join(cwd,'Info/Data_Stocks.csv')
			with open(file_path1,'a',newline='',encoding='utf-8') as file:
				writer=csv.writer(file)
				writer.writerow(row)
			request.session['stock_symbol']=stock_symbol
			return HttpResponseRedirect(reverse('stock_page'))


	context={
	'form': form,
	}

	return render(request,'stock_detail_form.html',context)







def stock_page(request):
	stock_symbol=request.session.get('stock_symbol')
	print(stock_symbol)
	html_info,html_loss=load_database(stock_symbol)
	context={
		'Stock_symbol':stock_symbol,
		'table_info':html_info,
		'table_loss':html_loss,
	}
	return render(request,'stock_detail.html',context)

def load_database(stock):
	load_stocks()
	Stock_data='Stocks_INFO_table.db'
	Stock_earning='Stocks_earning_loss_table.db'
	cwd=os.getcwd()
	print(cwd)
	file_path1=os.path.join(cwd,'Info/Stocks_INFO_table.db')
	file_path2=os.path.join(cwd,'Info/Stocks_earning_loss_table.db')
	print(file_path1)
	cnx = sqlite3.connect(file_path1)
	stk_info = pd.read_sql_query("SELECT * FROM STOCKSINFO", cnx)
	cnx2=sqlite3.connect(file_path2)
	stk_earn=pd.read_sql_query("SELECT * FROM STOCKSLOSS", cnx2)
	info_table=stk_info[stk_info['SYMBOL']==stock]
	earn_table=stk_earn[stk_info['SYMBOL']==stock]
	html_info=info_table.to_html(classes=['table'],index=False)
	html_loss=earn_table.to_html(classes=['table'],index=False)

	return html_info,html_loss

def load_db():
	Stock_data='Stocks_INFO_table.db'
	Stock_earning='Stocks_earning_loss_table.db'
	cwd=os.getcwd()
	print(cwd)
	file_path1=os.path.join(cwd,'Info/Stocks_INFO_table.db')
	file_path2=os.path.join(cwd,'Info/Stocks_earning_loss_table.db')
	print(file_path1)
	cnx = sqlite3.connect(file_path1)
	stk_info = pd.read_sql_query("SELECT * FROM STOCKSINFO", cnx)
	cnx2=sqlite3.connect(file_path2)
	stk_earn=pd.read_sql_query("SELECT * FROM STOCKSLOSS", cnx2)
	
	return stk_info,stk_earn
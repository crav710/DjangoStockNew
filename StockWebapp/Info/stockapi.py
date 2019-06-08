from datetime import date
import csv
import sqlite3
import os

Stock_file='Data_Stocks.csv'
Data_Bonds='Data_Bonds.csv'

class Stock:
	
	def __init__(self,stock_id,stock_symbol,no_of_shares,purchase_price,current_value,purchase_date):
		self.stock_id=stock_id
		self.no_of_shares=no_of_shares
		self.stock_symbol=stock_symbol
		self.purchase_price=purchase_price
		self.current_value=current_value
		self.purchase_date=purchase_date
		self.f_date=date(2019,4,28)


	def calculate_Earning_or_loss(self):
		return round((self.current_value-self.purchase_price)*self.no_of_shares,1)

	def calculate_yearly_earning_or_loss(self):
		z=self.purchase_date.split('/')
		print(z)
		curr_date=date(int(z[2]),int(z[0]),int(z[1]))
		diff_date=str(self.f_date - curr_date)
		days_count=float(diff_date.split('days')[0])/365.0
		return round(((self.current_value - self.purchase_price)/float(self.purchase_price)/days_count),4)*100
	def print_stock_detail(self):
		str1='| {:12} | {:14} | {:14} | {:16} | {:15} | \n'.format(self.stock_symbol,self.no_of_shares,self.purchase_price,self.current_value,self.purchase_date)
		return str1

	def print_stock_earnings(self):
		y=float("%.2f" %self.calculate_yearly_earning_or_loss())
		str1='| {:14} | {:11} | {:16} | {:13} \n'.format(self.stock_symbol, self.no_of_shares, self.calculate_Earning_or_loss(),str(y)+'%')
		return str1
	def stock_earning(self):
		y=float("%.2f" %self.calculate_yearly_earning_or_loss())
		return self.calculate_Earning_or_loss(),y

	# def get_stock_symbol()






class Bonds(Stock):
	"""docstring for Bonds"""
	def __init__(self, bond_id,stock_symbol,no_of_shares,purchase_price,current_value,purchase_date,coupon,yield_percentage):
		super(Bonds, self).__init__(bond_id,stock_symbol,no_of_shares,purchase_price,current_value,purchase_date)
		self.coupon=coupon
		self.yield_percentage=yield_percentage

	# i could have added that in the constructor as well but i am doing it this way 

	def set_coupon_price(self,coupon):
		self.coupon=coupon
	
	def set_yield_percentage(self,yield_percentage):
		self.yield_percentage=yield_percentage
	
	def get_coupon_price(self):
		return self.coupon

	def get_yield_percentage(self):
		return self.yield_percentage

	def print_bond_info(self):
 		str_1='| {:12} | {:14} | {:14} | {:16} | {:15} | {:16}| {:14} |\n'.format(self.stock_symbol,self.no_of_shares,self.purchase_price,self.current_value,self.coupon,str(self.yield_percentage)+'%',self.purchase_date)
 		return str_1 
	def print_bond_earning(self):
 		y=float("%.2f" %self.calculate_yearly_earning_or_loss())
 		str1='| {:14} | {:11} | {:16} | {:13} \n'.format(self.stock_symbol, self.no_of_shares, self.calculate_Earning_or_loss(),str(y)+'%')
 		return str1

	def bond_earning(self):
 		y=float("%.2f" %self.calculate_yearly_earning_or_loss())
 		return self.calculate_Earning_or_loss(),y



class Investor():
	"""docstring for Investor"""
	def __init__(self, Id,address,phone_number):
		self.Id=Id
		self.address=address
		self.phone_number=phone_number

	def get_phone_number(self):
		return self.phone_number

	def get_address(self):
		return self.address

	def display_info(self):
		str1='| {:14} | {:11} | {:16} | \n'.format(self.Id,self.address,self.phone_number)
		return str1
		
def printing_stocks_info(list_stocks):
	cwd=os.getcwd()
	print(cwd)
	file_path1=os.path.join(cwd,'Info/Stocks_INFO_table.db')
	db_file_name=file_path1
	conn=sqlite3.connect(db_file_name)
	# Creating Stock table 
	try:	
		conn.execute('''CREATE TABLE STOCKSINFO 
						( ID INT PRIMARY KEY NOT NULL,
						  SYMBOL TEXT NOT NULL,
						  NO_SHARES INT NOT NULL,
						  PURCHASE_PRICE INT NOT NULL,
						  CURRENT_PRICE  INT NOT NULL,
						  PURCHASE_DATE TEXT NOT NULL);''')
	except Exception as e:
		print("Create table error",e)
	# Inserting in the table
	for x in list_stocks:
		statement='''INSERT INTO STOCKSINFO(ID,SYMBOL,NO_SHARES,PURCHASE_PRICE,CURRENT_PRICE,PURCHASE_DATE) VALUES ({},{},{},{},{},{})'''.format(x.stock_id,"'"+x.stock_symbol+"'",x.no_of_shares,x.purchase_price,x.current_value,"'"+x.purchase_date+"'")
		# print(statement)
		try:
			conn.execute(statement)
		except Exception as e:
			# print("Insert Error",e)
			z=0
	conn.commit()
	conn.close()

	file_path2=os.path.join(cwd,'Info/Stocks_earning_loss_table.db')
	db_file_name=file_path2
	conn1=sqlite3.connect(db_file_name)
	# Creating Stock table 
	try:	
		conn1.execute('''CREATE TABLE STOCKSLOSS
						( ID INT PRIMARY KEY NOT NULL,
						  SYMBOL TEXT NOT NULL,
						  NO_SHARES INT NOT NULL,
						  EARNING_LOSS INT NOT NULL,
						  YEARLY_EARNING_LOSS  INT NOT NULL);''')
	except Exception as e:
		print("Create table error",e)
	# Inserting in the table
	for x in list_stocks:
		loss,year_loss=x.stock_earning()
		statement='''INSERT INTO STOCKSLOSS(ID,SYMBOL,NO_SHARES,EARNING_LOSS,YEARLY_EARNING_LOSS) VALUES ({},{},{},{},{})'''.format(x.stock_id,"'"+x.stock_symbol+"'",x.no_of_shares,loss,year_loss)
		try:
			conn1.execute(statement)
		except Exception as e:
			# print("Loss Insert Error",e)
			z=0
	conn1.commit()
	conn1.close()



def print_bond_info(list_bonds):
	db_file_name='Bonds_INFO_table.db'
	conn=sqlite3.connect(db_file_name)
	# Creating Stock table 
	try:	
		conn.execute('''CREATE TABLE BONDSINFO 
						( ID INT PRIMARY KEY NOT NULL,
						  SYMBOL TEXT NOT NULL,
						  NO_SHARES INT NOT NULL,
						  PURCHASE_PRICE INT NOT NULL,
						  CURRENT_PRICE  INT NOT NULL,
						  COUPON_PRICE  INT NOT NULL,
						  YEILD_PERCENT INT NOT NULL,
						  PURCHASE_DATE TEXT NOT NULL);''')
	except Exception as e:
		# print("Create table error",e)
		z=0
	# Inserting in the table
	for x in list_bonds:
		statement='''INSERT INTO BONDSINFO(ID,SYMBOL,NO_SHARES,PURCHASE_PRICE,CURRENT_PRICE,COUPON_PRICE,YEILD_PERCENT,PURCHASE_DATE) VALUES ({},{},{},{},{},{},{},{})'''.format(x.stock_id,"'"+x.stock_symbol+"'",x.no_of_shares,x.purchase_price,x.current_value,x.coupon,x.yield_percentage,"'"+x.purchase_date+"'")
		# print(statement)
		try:
			conn.execute(statement)
		except Exception as e:
			print("Insert Error",e)
	conn.commit()
	conn.close()


	db_file_name='Bonds_earning_loss_table.db'
	conn1=sqlite3.connect(db_file_name)
	# Creating Stock table 
	try:	
		conn1.execute('''CREATE TABLE BONDSLOSS
						( ID INT PRIMARY KEY NOT NULL,
						  SYMBOL TEXT NOT NULL,
						  QUANTITY INT NOT NULL,
						  EARNING_LOSS INT NOT NULL,
						  YEARLY_EARNING_LOSS  INT NOT NULL);''')
	except Exception as e:
		print("Create table error",e)
	# Inserting in the table
	for x in list_bonds:
		loss,year_loss=x.bond_earning()
		statement='''INSERT INTO BONDSLOSS(ID,SYMBOL,QUANTITY,EARNING_LOSS,YEARLY_EARNING_LOSS) VALUES ({},{},{},{},{})'''.format(x.stock_id,"'"+x.stock_symbol+"'",x.no_of_shares,loss,year_loss)
		try:
			conn1.execute(statement)
		except Exception as e:
			# print("Loss Insert Error",e)
			z=0
	conn1.commit()
	conn1.close()




def print_investor_info(list_investor):
	db_file_name='Investor_INFO_table.db'
	conn=sqlite3.connect(db_file_name)
	# Creating Stock table 
	try:	
		conn.execute('''CREATE TABLE INVESTORSINFO 
						( ID INT PRIMARY KEY NOT NULL,
						  ADDRESS TEXT NOT NULL,
						  PHONE INT NOT NULL);''')
	except Exception as e:
		print("Create table error",e)
	# Inserting in the table
	for x in list_investor:
		statement='''INSERT INTO INVESTORSINFO(ID,ADDRESS,PHONE) VALUES ({},{},{})'''.format(x.Id,"'"+x.address+"'",x.phone_number)
		# print(statement)
		try:
			conn.execute(statement)
		except Exception as e:
			print("Insert Error",e)
	conn.commit()
	conn.close()

def load_stocks():
	cwd=os.getcwd()
	print(cwd)
	file_path1=os.path.join(cwd,'Info/Data_Stocks.csv')
	Stock_file=file_path1
	list_stocks=[]
	with open(Stock_file,'r',encoding='utf8') as stk_file:
		csvreader=csv.reader(stk_file)
		fields=next(csvreader)
		Id=1
		for row in csvreader:
			stk_name=row[0]
			# print(isinstance(stk_name,str))
			if isinstance(stk_name, str)==False:
				print('Stock Name is not valid, please enter the new Stock Name for the entry ',row)
				stk_name=input('Enter the New Stock Name')
			
			try:
				No_of_shares=int(row[1])
			except Exception as e:
				print('No_of_shares is not valid, please enter the New No_of_shares for the entry ',row)
				No_of_shares=input('Enter the New No_of_shares')
			try:
				Purchase_price=float(row[2])
			except Exception as e:
				print('Purchase_price is not valid, please enter the new Purchase_price for the entry ',row)
				Purchase_price=input('Enter the New Purchase_price')		
			
			try:
				Current_price=float(row[3])
			except Exception as e:
				print('Current_price is not valid, please enter the new Current_price for the entry ',row)
				Current_price=input('Enter the New Current_price')
			
			Purchase_date=row[4]
			if isinstance(Purchase_date, str)==False:
				print('Purchase_date is not valid, please enter the new Purchase_date for the entry ',row)
				Purchase_date=input('Enter the New Purchase_date')	
			list_stocks.append(Stock(Id,stk_name,No_of_shares,Purchase_price,Current_price,Purchase_date)) 
			Id=Id+1
	printing_stocks_info(list_stocks)

def load_bonds():
	list_bonds=[]
	with open(Data_Bonds,'r',encoding='utf8') as bnd_file:
		csvreader=csv.reader(bnd_file)
		fields=next(csvreader)
		Id=1
		for row in csvreader:
			bnd_name=row[0]
			if isinstance(bnd_name, str)==False:
				print('Stock Name is not valid, please enter the new Stock Name for the entry ',row)
				bnd_name=input('Enter the New Stock Name')
			No_of_shares=row[1]
			try:
				No_of_shares=int(row[1])
			except Exception as e:
				print('No_of_shares is not valid, please enter the New No_of_shares for the entry ',row)
				No_of_shares=input('Enter the New No_of_shares')
			try:
				Purchase_price=float(row[2])
			except Exception as e:
				print(e)
				print('Purchase_price is not valid, please enter the new Purchase_price for the entry ',row)
				Purchase_price=input('Enter the New Purchase_price')		
			
			try:
				Current_price=float(row[3])
			except Exception as e:
				print('Current_price is not valid, please enter the new Current_price for the entry ',row)
				Current_price=input('Enter the New Current_price')
			

			Purchase_date=row[4]
			if isinstance(Purchase_date, str)==False:
				print('Purchase_date is not valid, please enter the new Purchase_date for the entry ',row)
				Purchase_date=input('Enter the New Purchase_date')	
			
			try:
				Coupon=float(row[5])
			except Exception as e:
				print('Coupon is not valid, please enter the new Coupon for the entry ',row)
				Coupon=input('Enter the New Coupon')	
			
			try:
				Yield=float(row[6])
			except Exception as e:
				print('Yield is not valid, please enter the new Yield for the entry ',row)
				Yield=input('Enter the New Yield')	
			
		

			list_bonds.append(Bonds(Id,bnd_name,No_of_shares,Purchase_price,Current_price,Purchase_date,Coupon,Yield))
			
			
			Id=Id+1
	print_bond_info(list_bonds)

def load_investor():
	list_investor=[]
	list_investor.append(Investor(1,"Address1",704542525))
	print_investor_info(list_investor)







		
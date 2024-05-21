import pandas as pd
import sqlite3
import numpy as np

from settings import DB

db = DB['dbname']

def clean_address(df):
    if 'Customer Address.1' in df.columns:
        df['Customer Address'] = df['Customer Address'] + df['Customer Address.1'] + df['Customer Address.2']
        return df.drop(['Customer Address.1', 'Customer Address.2'], axis=1)
    return df

def create_database():
	try:
		SQLConnection = sqlite3.connect(db)
		cursor = SQLConnection.cursor()
		# print('Database created/connected successfully')

		with open('create_tables.sql', 'r') as sql_file:
			sql_script = sql_file.read()
		
		cursor.executescript(sql_script)
		
		cursor.close()
	except Exception as e:
		if SQLConnection:
			SQLConnection.close()
		print("Something went wrong while creating/connecting database. Error:", e)
		SystemExit()
	finally:
		if SQLConnection:
			SQLConnection.close()


def load_csv(filename: str):
	'''
		Function load_csv accepts the csv filename as a variable, reads the csv file and loads it to the database
	'''
	create_database()
	df = pd.read_csv('sample.csv', index_col=False)
	df = clean_address(df)

	# try:
	SQLConnection = sqlite3.connect(db)
	cursor = SQLConnection.cursor()
	# print('Database created/connected successfully')
	print(df.head())
	for idx, row in df.iterrows():
		selectquery = f"SELECT * FROM orders WHERE orderid={row['Order ID']} and productid={row['Product ID'][1:]} and customerid={row['Customer ID'][1:]};"

		res = cursor.execute(selectquery)
		if len(res.fetchall()) > 0:
			continue

		selectquery = f"SELECT * FROM categories WHERE categoryname=?;"
		res = cursor.execute(selectquery, [row['Category']])
		out = res.fetchall()

		if len(out) == 0:
			insertquery = f"INSERT INTO categories (categoryid, categoryname) VALUES (NULL, ?);"
			res.execute(insertquery, [row['Category']])
			selectquery = f"SELECT * FROM categories WHERE categoryname=?;"
			res = cursor.execute(selectquery, [row['Category']])
			out = res.fetchall()
		categoryid = out[-1][0]
		
		selectquery = f"SELECT * FROM regions WHERE regionname=?;"
		res = cursor.execute(selectquery, [row['Region']])
		out = res.fetchall()

		if len(out) == 0:
			insertquery = f"INSERT INTO regions (regionid, regionname) VALUES (NULL, ?);"
			res.execute(insertquery, [row['Region']])
			selectquery = f"SELECT * FROM regions WHERE regionname=?;"
			res = cursor.execute(selectquery, [row['Region']])
			out = res.fetchall()
		regionid = out[-1][0]

		if pd.isnull(row['Product ID']):
			insertquery = f"INSERT INTO products (productid, productname, unitprice, category) VALUES (NULL, ?, ?, ?);"
			cursor.execute(insertquery, [row['Product Name'], row['Unit Price'], categoryid])
		else:
			selectquery = f"SELECT productid from products WHERE productid=?;"
			res = cursor.execute(selectquery, [row['Product ID'][1:]])
			out = res.fetchall()

			if len(out) == 0:
				insertquery = f"INSERT INTO products (productid, productname, unitprice, category) VALUES (?, ?, ?, ?);"
				cursor.execute(insertquery, [row['Product ID'][1:], row['Product Name'], row['Unit Price'], categoryid])

		if pd.isnull(row['Customer ID']):
			insertquery = f"INSERT INTO customers (customerid, customername, customeremail, customeraddress, customerregion) VALUES (NULL, ?, ?, ?, ?);"
			cursor.execute(insertquery, [row['Customer Name'], row['Customer Email'], row['Customer Address'], regionid])
		else:
			selectquery = f"SELECT productid from products WHERE productid=?;"
			res = cursor.execute(selectquery, [row['Product ID'][1:]])
			out = res.fetchall()

			if len(out) == 0:
				insertquery = f"INSERT INTO customers (customerid, customername, customeremail, customeraddress, customerregion) VALUES (?, ?, ?, ?, ?);"
				cursor.execute(insertquery, [row['Customer ID'][1:], row['Customer Name'], row['Customer Email'], row['Customer Address'], regionid])

		selectquery = f"SELECT * FROM payment_methods WHERE methodname=?;"
		res = cursor.execute(selectquery, [row['Payment Method']])
		out = res.fetchall()

		if len(out) == 0:
			insertquery = f"INSERT INTO payment_methods (methodid, methodname) VALUES (NULL, ?);"
			res.execute(insertquery, [row['Payment Method']])
			selectquery = f"SELECT * FROM payment_methods WHERE methodname=?;"
			res = cursor.execute(selectquery, [row['Payment Method']])
			out = res.fetchall()
		methodid = out[-1][0]
		
		insertquery = f"INSERT INTO orders (orderid, productid, customerid, orderdate, quantitysold, discount, shipping, paymentmethod) VALUES (NULL, ?, ?, ?, ?, ?, ?, ?);"
		cursor.execute(insertquery, [row['Product ID'][1:], row['Customer ID'][1:], row['Date of Sale'], row['Quantity Sold'], row['Discount'], row['Shipping Cost'], methodid])
	
	cursor.close()
	# except Exception as e:
	# 	print("Something went wrong while creating/connecting database. Error:", e)
	# finally:
	# 	if SQLConnection:
	# 		SQLConnection.close()

if __name__ == '__main__':
	load_csv('sample.csv')
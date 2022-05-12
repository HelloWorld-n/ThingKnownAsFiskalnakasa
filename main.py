#!/bin/python3
import time
from tkinter.constants import COMMAND
import pymysql
import os, sys
import Stuff
from Stuff import COLORS, generateMessage, gridElement, theAppFont, __OPERATORS, __ALPHABET
import tkinter as Tk
import threading
import Connect

db = Connect.connectSql()

global products
products: '''<{id: pKey, name: string, price: float}>''' = []

def downloadCurrentProducts():
	global products
	try:
		problem = False
		cursor = db.cursor()
				
		cursor.execute("USE db_fiskalnakasa;")
		
		cursor.execute("SELECT * FROM products")
		data = cursor.fetchall()
		products = data

		db.commit()
	except Exception as exception:
		print("<h1 class=\"failure\">Problem.</h1>")
		print(exception)
	
	db.rollback()

def insertText(text):
	calcResult = None
	lbl_output["text"] = ""
	if text in __OPERATORS:
		lbl_input["text"] += " "
	lbl_input["text"] += text
	if text in __OPERATORS + ",":
		lbl_input["text"] += " "


def alterColors(isLightMode):
	stuff.setColorMode(isLightMode)
	calculator.saveState("temp")
	os.execl(sys.executable, sys.executable, *sys.argv)

def setColorMode():
	root = Tk.Tk()
	root.configure(bg = COLORS["bg"])
	gridElement(
		Tk.Button, root, text = "Dark",
		row = 0, column = 0, 
		bg = COLORS["bg"], font = theAppFont(size = "16"),
		padx = 5, pady = 5,
		command = lambda: alterColors(False)
	)
	gridElement(
		Tk.Button, root, text = "Ask System",
		row = 1, column = 0, 
		bg = COLORS["bg"], font = theAppFont(size = "16"),
		padx = 5, pady = 5,
		command = lambda: alterColors(None)
	)
	gridElement(
		Tk.Button, root, text = "Light",
		row = 2, column = 0, 
		bg = COLORS["bg"], font = theAppFont(size = "16"),
		padx = 5, pady = 5,
		command = lambda: alterColors(True)
	)




def addProduct():
	global products
	
	tk = Tk.Tk()
	tk.configure(bg = COLORS["bg"])
	def add(id_, name, price):
			
		try:
			problem = False
			cursor = db.cursor()
			
			try:
				int(id_.get()), 
			except ValueError:
				raise ValueError("Id Must Be Integer")

			try:
				float(price.get()), 
			except ValueError:
				raise ValueError("Price Must Be Float")
				

			cursor.execute("USE db_fiskalnakasa;")
			cursor.execute(
				"""
					INSERT INTO products(id, name, price) VALUES (%s, %s, %s)
				""", 
				[
					int(id_.get()), 
					nameEntry.get(), 
					float(priceEntry.get()), 
				]
			)
			data = cursor.fetchall()
			products = data

			db.commit()
			generateMessage("Success")
		except pymysql.err.IntegrityError as err:
			print("Problem.\n")
			if err.args[0] == 1062:
				generateMessage("Id must be unique!")
		except ValueError as err:
			generateMessage(err)
		except Exception as err:
			generateMessage(err)

	db.rollback()	
	
	entryPos = 0

	gridElement(
		Tk.Label, tk, text = f"""Id: """,
		row = entryPos, column = 0,
		bg = COLORS["bg"], font = theAppFont(size = "12"),
		padx = 5, pady = 5,
	)
	idEntry = gridElement(
		Tk.Entry, tk,
		row = entryPos, column = 1, 
		bg = COLORS["bg-plus"], fg = COLORS["fg"], font = theAppFont(),
	)
	entryPos += 1

	gridElement(
		Tk.Label, tk, text = f"""Name: """,
		row = entryPos, column = 0,
		bg = COLORS["bg"], font = theAppFont(size = "12"),
		padx = 5, pady = 5,
	)
	nameEntry = gridElement(
		Tk.Entry, tk,
		row = entryPos, column = 1, 
		bg = COLORS["bg-plus"], fg = COLORS["fg"], font = theAppFont(),
	)
	entryPos += 1
	
	gridElement(
		Tk.Label, tk, text = f"""Price: """, 
		row = entryPos, column = 0,  
		bg = COLORS["bg"], font = theAppFont(size = "12"), 
		padx = 5, pady = 5, 
	)
	priceEntry = gridElement(
		Tk.Entry, tk, 
		row = entryPos, column = 1, columnspan = 2, 
		bg = COLORS["bg-plus"], fg = COLORS["fg"], font = theAppFont(), 
	)
	entryPos += 1
	
	gridElement(
		Tk.Button, tk, text = f"""Confirm""",
		row = entryPos, column = 0, columnspan = 3,
		bg = COLORS["bg-key"], font = theAppFont(size = "12"),
		padx = 5, pady = 5,
		command = lambda id_ = idEntry, name = nameEntry, price = priceEntry: add(id_, name, price)
	)

	tk.mainloop()



def regisratsiya():
	global products
	downloadCurrentProducts()
	tk = Tk.Tk()
	tk.configure(bg = COLORS["bg"])

	productsBuyen = []
	productsQuantityList = []

	def alterQuantity(pos):
		nonlocal productsBuyen
		tk = Tk.Tk()
		tk.configure(bg = COLORS["bg"])
		
		def quantityAltered(pos):
			nonlocal quantityEntry
			nonlocal productsBuyen
			nonlocal productsQuantityList
			try: 
				float(quantityEntry.get())
				generateMessage("Success")
			except:
				quantityEntry.delete(0, Tk.END)
				quantityEntry.insert(0, str(productsBuyen[pos]["quantity"]))
				generateMessage("Err: Please make sure it is float!")
			productsBuyen[pos]["quantity"] = float(quantityEntry.get())
			productsQuantityList[pos].configure(
				text = f""".&{
					(
						productsBuyen[pos]["quantity"] 
					) if productsBuyen[pos]["quantity"] != round(productsBuyen[pos]["quantity"]) else (
						round(productsBuyen[pos]["quantity"])
					)
				}"""
			)

		gridElement(
			Tk.Label, tk, 
			text = f"""Quantity of [{pos}]@> \"{productsBuyen[pos]["name"]}\": """, 
			row = 0, column = 2,  width = 45, height = 1, 
			bg = COLORS["bg"], font = theAppFont(size = "12"),
			padx = 5, pady = 5, 
		)
		quantityEntry = gridElement(
			Tk.Entry, tk, 
			row = 0, column = 3,
			state = "normal", 
			bg = COLORS["bg"], font = theAppFont(size = "12"),  
		)
		gridElement(
			Tk.Button, tk, 
			text = f"""\"Alter""", 
			row = 0, column = 4,  width = 5, height = 1, 
			bg = COLORS["bg-key"], font = theAppFont(size = "12"),
			padx = 5, pady = 5,
			command = lambda pos=pos: quantityAltered(pos)
		)
		tk.mainloop()
	
	
	def buy(providenProduct):
		nonlocal productsBuyen
		nonlocal productsQuantityList
		gridElement(
			Tk.Label, tk, 
			text = f"""\"{providenProduct["name"]}\" ({providenProduct["price"]}) """, 
			row = len(productsBuyen), column = 2,  width = 45, height = 1, 
			bg = COLORS["bg"], font = theAppFont(size = "12"),
			padx = 5, pady = 5,
		)
		productsQuantityList += [
			gridElement(
				Tk.Label, tk, 
				text = f""".&1""", 
				row = len(productsBuyen), column = 3,  width = 5, height = 1, 
				bg = COLORS["bg"], font = theAppFont(size = "12"),
				padx = 5, pady = 5,
			), 
		]
		gridElement(
			Tk.Button, tk, 
			text = f"""\"Alter""", 
			row = len(productsBuyen), column = 4,  width = 5, height = 1, 
			bg = COLORS["bg-key"], font = theAppFont(size = "12"),
			padx = 5, pady = 5,
			command = lambda pos=len(productsBuyen): alterQuantity(pos)
		)
		productsBuyen += [{**providenProduct,  "quantity": 1}]

	def calculateTotalPrice():
		nonlocal productsBuyen
		result = 0
		for item in productsBuyen:
			result += item["price"] * item["quantity"]
		generateMessage(result)
		return result

	itemPos = 0
	for item in products:
		gridElement(
			Tk.Button, tk, text = f"""({item["id"]}) \"{item["name"]}\" = ({item["price"]} EUR)""",
			row = itemPos, column = 0, columnspan = 1, width = 45, height = 1, 
			bg = COLORS["bg-key-variable"], font = theAppFont(size = "12"),
			padx = 5, pady = 5,
			command = lambda item = item: buy(item)
		)
		itemPos += 1
	
	fnPos = 0
	gridElement(
		Tk.Button, tk, text = f"""Calculate Total Price""",
		row = fnPos, column = 1, columnspan = 1, width = 45, height = 1, 
		bg = COLORS["bg-key-function"], font = theAppFont(size = "12"),
		padx = 5, pady = 5,
		command = lambda: calculateTotalPrice() 
	)
	tk.mainloop()


if __name__ == "__main__":
	root = Tk.Tk()
	root.configure(bg = COLORS["bg"])
	genericOptionsPos = 0
	
	gridElement(
		Tk.Button, root, text = "Add Product",
		row = genericOptionsPos, column = 0, columnspan = 1,  width = 15, height = 1, 
		bg = COLORS["bg-key-function"], font = theAppFont(size = "12"),
		padx = 5, pady = 5,
		command = lambda: addProduct()
	)
	genericOptionsPos += 1 
	gridElement(
		Tk.Button, root, text = "Regisratsiya",
		row = genericOptionsPos, column = 0, columnspan = 1,  width = 15, height = 1, 
		bg = COLORS["bg-key-function"], font = theAppFont(size = "12"),
		padx = 5, pady = 5,
		command = lambda: regisratsiya()
	)
	genericOptionsPos += 1 
	
	gridElement(
		Tk.Button, root, text = "Izves'tay",
		row = genericOptionsPos, column = 0, columnspan = 1,  width = 15, height = 1, 
		bg = COLORS["bg-key-function"], font = theAppFont(size = "12"),
		padx = 5, pady = 5,
		command = lambda: izves_tay()
	)
	genericOptionsPos += 1 
	
	gridElement(
		Tk.Button, root, text = "Nuliranye",
		row = genericOptionsPos, column = 0, columnspan = 1,  width = 15, height = 1, 
		bg = COLORS["bg-key-function"], font = theAppFont(size = "12"),
		padx = 5, pady = 5,
		command = lambda: nuliranye()
	)
	genericOptionsPos += 1 
	
	gridElement(
		Tk.Button, root, text = "Programiranye",
		row = genericOptionsPos, column = 0, columnspan = 1,  width = 15, height = 1, 
		bg = COLORS["bg-key-function"], font = theAppFont(size = "12"),
		padx = 5, pady = 5,
		command = lambda: programiranye()
	)

	
	root.mainloop()

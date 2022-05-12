#!/bin/python3
import Connect

try:
	db = Connect.connectSql()
	cursor = db.cursor()
	cursor.execute("CREATE DATABASE IF NOT EXISTS db_fiskalnakasa;")
	cursor.execute("USE db_fiskalnakasa;")
	cursor.execute(
		"CREATE TABLE IF NOT EXISTS products ("
			"id Int NOT NULL,"
			"name VarChar(100) NOT NULL,"
			"price float NOT NULL,"
			"PRIMARY KEY(id)"
		")"
	)
	db.commit()
except Exception as exception:
	print(exception)
	db.rollback()

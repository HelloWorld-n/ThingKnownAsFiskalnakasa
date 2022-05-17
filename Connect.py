#!/bin/python3
import pymysql
import requests
import os


UPCASE = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
DOWNCASE = "abcdefghijklmnopqrstuvwxyz"
DIGITS = "0123456789"
BASIC_ALPHANUM = UPCASE + DOWNCASE + DIGITS

HOST = "::1"
PORT = "3306"
SQL_USERNAME = "the_user"
SQL_PASSWORD = "the_pass"

def connectSql():
	return pymysql.connect(
		host=HOST, 
		port=int(PORT), 
		user=SQL_USERNAME,
		password=SQL_PASSWORD,
		cursorclass=pymysql.cursors.DictCursor
	)

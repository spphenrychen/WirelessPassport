#!/usr/bin/python
# coding=UTF-8

import SocketServer, sys, threading
from time import ctime
import MySQLdb
from time import localtime,strftime

class DBConn:
	def __init__(self):
		self.host = 'localhost'
		self.user = 'root'
		self.passwd = 'ib402'
		self.dbname = 'oose'

	def dbConnect(self):
		try:
			self.db = MySQLdb.connect(self.host,self.user,self.passwd,self.dbname,charset='utf8')
			
		except:
     			print 'Error occurred when connecting to SQL database'
     			sys.exit(1)


	# Exec SQL Query 
	def runSelect(self, sql):
		ssid=[]
		cursor=self.db.cursor()
		cursor.execute(sql)
		results = list(cursor)
		for row in results:
			ssid.append(row[0])
		cursor.close()
		return ssid
	# Exec SQL Insert
	def runInsert(self, sql):
		cursor=self.db.cursor()
		cursor.execute(sql)
		self.db.commit()
		cursor.close()


	# Exec SQL Update
	#def runUpdate(self, sql):
		#self.cursor.execute(sql)
		#self.db.commit()

	# Exec SQL Delete
	def runDelete(self, sql):
		cursor=self.dbConnect.cursor()
		cursor.execute(sql)
		self.db.commit()

	# 關閉資料庫連線
	def dbClose(self):
		self.db.close()
	

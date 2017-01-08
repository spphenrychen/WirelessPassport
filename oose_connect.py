#!/usr/bin/python
# coding=UTF-8

import SocketServer, sys, threading
from time import ctime
import MySQLdb

HOST= '140.123.92.243'
PORT = 12345


def Compare_DB(Door,SSID):
	if Door in SSID:
		return True
	else:
		return False

class MyServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
	daemon_threads = True
 	allow_reuse_address = True

class MyHandler(SocketServer.StreamRequestHandler):
	def handle(self):
		ssid=[]
 		cur = threading.current_thread()
		print '[%s] Client connected from %s and [%s] is handling with him.' % (ctime(), self.request.getpeername(), cur.name)
		while True:
			msg = self.request.recv(1024).strip()
			if not msg:
				pass
			else:
				print "Client send SSID: " + msg 
				ssid=MySQL.Sol_Connect("localhost","root","ib402","oose" )
				if MySQL.Compare_DB(msg,ssid) is True:	
					self.wfile.write("1\r\n")
				else:
					self.wfile.write("0\r\n")
		self.request.close()
class MySQL():
	@staticmethod
	def  Sol_Connect(IP,User,Passwd,Table):
		print 1
		# Open database connection
		db = MySQLdb.connect(IP,User,Passwd,Table ) 
		print 2
		ssid=[] #declare  a list
		# prepare a cursor object using cursor() method
	    	cursor = db.cursor()

		# Prepare SQL query to INSERT a record into the database.
		sql = "SELECT * FROM gate1"
		try:
			# Execute the SQL command
			cursor.execute(sql)
			# Fetch all the rows in a list of lists.
			results = cursor.fetchall()
			for row in results:
	 			ssid.append(row[1])
				 # Now print fetched result
	 			print ssid
			return ssid
		except:
			print "Error: unable to fecth data"
			# disconnect from server
			db.close()

	@staticmethod
	def Compare_DB(Door,SSID):
		if Door in SSID:
			return True
		else:
			return False
if __name__ == '__main__':
	server = MyServer((HOST,PORT), MyHandler)
	ip, port = server.server_address
	print "Server is starting at:", (ip, port)
	try:
		server.serve_forever()
	except KeyboardInterrupt:
		sys.exit(0)

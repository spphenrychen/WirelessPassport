#!/usr/bin/python
# coding=UTF-8

import SocketServer, sys, threading
from time import ctime,localtime,strftime
import MySQLdb
import dbconn


HOST= '10.42.0.90'
PORT = 12345


class MyServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
	daemon_threads = True
 	allow_reuse_address = True

class MyHandler(SocketServer.StreamRequestHandler):
	def handle(self):
		ssid=[]
 		cur = threading.current_thread()
 		dbuse=dbconn.DBConn()
 		dbuse.dbConnect()

		print '[%s] Client connected from %s and [%s] is handling with him.' % (ctime(), self.request.getpeername(), cur.name)
		while True:
			msg = self.request.recv(1024).strip()
			if not msg:
				pass
			else:
				print "Client send SSID: " + msg 
				Door,MAC=Auxiliary_Conn.SplitData(msg)
				sql_select=Auxiliary_Conn.Generate_Selectsql(Door)
				ssid=dbuse.runSelect(sql_select)
				print ssid
				if Auxiliary_Conn.Compare_DB(MAC,ssid) is True:
					sql_history=Auxiliary_Conn.Generate_Insertsql(MAC,Door,'1')
					dbuse.runInsert(sql_history)
					self.wfile.write("1")
				else:
					sql_history=Auxiliary_Conn.Generate_Insertsql(MAC,Door,'0')
					dbuse.runInsert(sql_history)
					self.wfile.write("0")
		dbuse.dbclose()
		self.request.close()
class Auxiliary_Conn():
	@staticmethod
	def Compare_DB(msg_MAC,db_SSID):
		if msg_MAC in db_SSID:
			return True
		else:
			return False
	@staticmethod
	def SplitData(SSID):
		Data=SSID.split(" ")
		Door=Data[0]
		MAC=Data[1]
		return Door,MAC
	@staticmethod
	def  Generate_Selectsql(gate):
		door='gate'+gate
		sql='SELECT  ssid FROM %s '%(door)
		return sql
	
	@staticmethod
	def  Generate_Insertsql(ssid,door,ifvalid):
		#for insert history
		datetime=strftime("%Y-%m-%d %H:%M:%S",localtime())
		db='gate'+door+'_history'
		sql="INSERT INTO %s VALUES('%s','%s','%s')"%(db,ssid,datetime,ifvalid)
		return sql
	


if __name__ == '__main__':
	server = MyServer((HOST,PORT), MyHandler)
	ip, port = server.server_address
	print "Server is starting at:", (ip, port)
	try:
		server.serve_forever()
	except KeyboardInterrupt:
		sys.exit(0)

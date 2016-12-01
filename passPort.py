import time
import threading
import socket
from datetime import datetime
from wifi import Cell, Scheme

HOST = '10.42.0.1'
PORT = 50030

global s

def thread_recv(connObj):
	while True:
		data = connObj.recv(1024)
		#print data
		if data == '1':
			print "OPEN"
		else:
			print "WRONG"

def thread_transmit(conn):
	while True:
		x = raw_input("")
		#print x
		conn.send(x)

def wifiDirectScan():
	while True:
		cell = Cell.all('wlan1')

		if cell != []:
			i = 0
			print "-----------------"
			for item in cell:
				print "Cell%i"% i
				print "\tssid:"+ item.ssid
				print "\taddress:"+ item.address
				print "\tsignal:%i"% item.signal
				i = i + 1
			print "----------------"
			log = open(str(item.address)+'.txt', 'a')
			log.write(str(datetime.now())+' '+str(item.signal)+'\n')
			log.close()
		else:
			print "No device found..."

def main():
	global s
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	s.connect((HOST, PORT))

	sendT = threading.Thread(target=thread_transmit, args=(s,))
	sendT.setDaemon(True)
	recvT = threading.Thread(target=thread_recv, args=(s,))
	recvT.setDaemon(True)

	sendT.start()
	recvT.start()

	wifiScantask = threading.Thread(target=wifiDirectScan)
	wifiScantask.setDaemon(True)
	wifiScantask.start()

	while True:
		pass

if __name__ == '__main__':
	main()


import time
import threading
import Queue
import socket
import RPi.GPIO as GPIO
from datetime import datetime
from wifi import Cell, Scheme

HOST = '10.42.0.1'
PORT = 50030

global s

class Userdata:
	def __init__(self, ssid, addr, rssi):
		self.ssid = ssid
		self.addr = addr
		self.rssi = rssi

class Switch:
	def __init__(self, openPin, alarmPin):
		self.opPin = openPin
		self.alPin = alarmPin
		GPIO.cleanup()
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.opPin,GPIO.OUT)
		GPIO.setup(self.alPin,GPIO.OUT)

	def openDoor(self):
		GPIO.output(self.opPin,GPIO.HIGH)
		time.sleep(1)
		GPIO.output(self.opPin,GPIO.LOW)

	def alarm(self):
		GPIO.output(self.alPin,GPIO.HIGH)
		time.sleep(1)
		GPIO.output(self.alPin,GPIO.LOW)

class thread_recv(threading.Thread):
	def __init__(self, connObj, sw):
		super(thread_recv, self).__init__()
		self.setDaemon(True)
		self.connObj = connObj
		self.switch = sw

	def run(self):
		while True:
			data = self.connObj.recv(1024)
			#print data
			if data == '1':
				print "OPEN"
				self.switch.openDoor()
			else:
				print "WRONG"
				self.switch.alarm()

class wifiDirectScan(threading.Thread):
	def __init__(self, conn):
		super(wifiDirectScan, self).__init__()
		self.setDaemon(True)
		self.conn = conn

	def run(self):
		while True:
			#scan wifi direct device list in range
			cell = Cell.all('wlan1')

			if cell != []:
				i = 0
				print "-----------------"
				for item in cell:
					usData = Userdata(item.ssid, item.address, item.signal)
					self.Print(i, usData)
					i = i + 1

					self.Send(usData)
					self.Log(usData)
				print "-----------------"
			else:
				print "No device found..."

	def Send(self, usData):
		self.conn.send(usData.addr)

	def Log(self, usData):
		log = open(str(usData.addr)+'.txt', 'a')
		log.write(str(datetime.now())+' '+str(usData.rssi)+'\n')
		log.close()

	def Print(self, i, usData):
		print "Cell%i"% i
		print "\tssid:"+ usData.ssid
		print "\taddress:"+ usData.addr
		print "\trssi:%i"% usData.rssi

def main():
	global s

	#GPIO setup
	sw = Switch(14,4)
	#socket setup
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, PORT))
	#start recieve thread
	recvT = thread_recv(s,sw)
	recvT.start()
	#start wifi direct scaning thread
	wifiScantask = wifiDirectScan(s,dataq)
	wifiScantask.start()

	while True:
		pass

if __name__ == '__main__':
	main()


import time
import threading
import Queue
import socket
import RPi.GPIO as GPIO
from datetime import datetime
from wifi import Cell, Scheme

HOST = '140.123.92.243'
PORT = 12346

global s

class Userdata:
	def __init__(self, ssid, addr, rssi):
		self.ssid = ssid
		self.addr = addr
		self.rssi = rssi

class StateList:
	def __init__(self, rssi):
		self.state = 'None'
		self.rssi = [rssi]


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
		self.userList = {}
		
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
					print "-----------------"
					i = i + 1

					self.Check(usData)
					self.Log(usData)
					print usData.addr
					print self.userList[usData.addr].rssi
			else:
				print "No device found..."

	def Check(self, usData):
		#if userList is null
		if not self.userList:
			userstate = StateList(usData.rssi)
			self.userList.update({usData.addr:userstate})
			return

		#if user address is not in userList
		if usData.addr not in self.userList:
			userstate = StateList(usData.rssi)
			self.userList.update({usData.addr:userstate})
			return
		#if user is out of 2 meters
		if usData.rssi < -70:
			return
		
		curState = self.userList[usData.addr].state
		curRssiList = self.userList[usData.addr].rssi
		#append rssi into userList
		self.userList[usData.addr].rssi.append(usData.rssi)

		#get at least 3 times data
		if len(curRssiList) < 3:
			return

		#if a person stay enough long to open door
		if all( x > -60 for x in curRssiList[-3:]):
			self.Send(usData)
			self.userList[usData.addr].rssi = []

	def Send(self, usData):

		addrlist = usData.addr.split(":")
		addrStr = ""

		for item in addrlist:
			addrStr += item

		reqData = "1 " + addrStr
		print reqData
		self.conn.send(reqData)

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
	wifiScantask = wifiDirectScan(s)
	wifiScantask.start()

	while True:
		pass

if __name__ == '__main__':
	main()


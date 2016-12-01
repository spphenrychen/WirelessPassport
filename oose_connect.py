
#!/usr/bin/python
# coding=UTF-8

import MySQLdb
import socket,sys,time
from thread import *

def MYSQL_Conn():
    ssid=[]
    # Open database connection
    db = MySQLdb.connect("localhost","root","ib402","oose" )

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
    except:
       print "Error: unable to fecth data"

    # disconnect from server
    db.close()
    return ssid
def Compare_DB(Door,SSID):
    if Door in SSID:
        return True
    else:
        return False

def ThreadWork(client):
    while True:
        msg = client.recv(1024)
        if not msg:
            pass
        else:
            print "Client send: " + msg
            SSID=MYSQL_Conn()
            if Compare_DB(Door,SSID) is True:
                client.send("1")
            else:
                client.send("0")
    client.close()
def Sock_Server(Host,Port):
    sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.bind((Host,Port))
    sock.listen(5)

    while True:
        connection,address=sock.accept()
        start_new_thread(ThreadWork, (connection,))

    sock.close()

def main():
    Host='140.124.92.243'
    Port=8888
    Sock_Server(Host,Port)

main()

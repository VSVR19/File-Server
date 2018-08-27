'''
Student Name: Venkata Ramana Voddam Pudi Sankar
Student ID: 1001614404
'''

import socket
#Using sockets to communicated to and fro between Client and Server

import sys
#Provides information about constants, functions and methods of Python interpreter
#https://www.python-course.eu/sys_module.php

from _thread import *
#This module provides low-level primitives for working with multiple threads (also called light-weight processes or tasks) 
#https://docs.python.org/2/library/thread.html

import os
#The OS module in Python provides a way of using operating system dependent functionality. 
#http://www.pythonforbeginners.com/os/pythons-os-module

#Client Server interaction:https://www.binarytides.com/python-socket-programming-tutorial/

HOST = '127.0.0.1'
#Using my local computer as the host
PORT = 2346
#An arbitary non specialised port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Creating a socket using AF_INET for IPv4 addressing and SOCK_STREAM for connection oriented TCP protocol.
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

print('Socket Created')
#Printing out a acknowledgement for Socket creation

'''
This part provides exception handling mechanism for binding when binding HOST to PORT.
If bind success, we print out a acknowledgement; if bind fails, we print out the error and a message
'''
try:
    s.bind((HOST, PORT))
except socket.error:
    print(socket.error)
    print("Socket Bind failed")
    sys.exit()
print("Socket bind complete")


#Setting the maximum number waiting clients to 19.
s.listen(19)
print("Socket listening")

'''
Function clientthread is for handling connections as well as to create threads.
INPUT: Connection Variable
OUTPUT: Creation of threads and file handling mechanism
'''
def clientthread(conn):
    #welcome_message = "Welcome to server"
#Message to client
    #encode_message = welcome_message.encode('utf-8')
#Sending message to cleint
    #conn.sendall(encode_message)
    
    #An infinite loop so that function do not terminate and thread do not end.
    while True:
    
        #Receiving data from client
        try:
            data = conn.recv(2346)
        except ConnectionResetError:
            print("Connection closed by client; Goodbye!")
        #reply = 'Oki.na...' + data.decode('utf-8')
		
        data = data.decode('utf-8')
#Decoding the data received from client; i.e, converting the data into strings from bytes.
        #print("Received data being printed out" + data)

        split_data = data.split('\r')
#Applying split to segregate HTTP Header and Clients' data
		
#Lines 67 to 69 splits the file name and file data and stores them in file_name and file_content variables respectively.

        file_name_content = split_data[7].split('*')
        file_name = file_name_content[0].strip()
        file_content = file_name_content[1].strip()
	
#This 'if' module deals with File Upload functionality
        
        if(os.path.isfile("C:\\Users\\Venkat\\Desktop\\DS Client Folder\\" + file_name)):
#Check the prescence of client seleted file in Client folder
#If file is present in clients folder, user is trying to upload it to Server
            
            file_path = os.path.join("C:\\Users\\Venkat\\Desktop\\DS Server Folder\\" + file_name)
#Storing the files' path in file_path variable
            
            f = open(file_path, "w")
#Function open() is taking two arguments: the file path of the selected file and 'w' as permission
#w- Create a file if it does not exist in library or directory.
#https://stackoverflow.com/questions/5104957/how-do-i-create-a-file-at-a-specific-path#
#https://www.guru99.com/reading-and-writing-files-in-python.html#1
            
            f.write(file_content)
#Writing file_content to the newly created file
#https://www.guru99.com/reading-and-writing-files-in-python.html#1
            
            f.close()
#Post write, closing the file safely.



#This 'else' module deals with File Download functionality			
        else:
#Check the prescence of client seleted file in server folder
#If file is not in clients folder; user is trying to download the file from server
            
            file_path = os.path.join("C:\\Users\\Venkat\\Desktop\\DS Client Folder\\" + file_name)
#Storing the files' path in file_path variable

            f = open(file_path, "w")
#Function open() is taking two arguments: the file path of the selected file and 'w' as permission
#w- Create a file if it does not exist in library
#https://stackoverflow.com/questions/5104957/how-do-i-create-a-file-at-a-specific-path#
#https://www.guru99.com/reading-and-writing-files-in-python.html#1

            f.write(file_content)
#Writing file_content to the newly created file
#https://www.guru99.com/reading-and-writing-files-in-python.html#1
			
            f.close()
#Post write, closing the file safely.			
        #print("Reply" + reply)
        
		
#If no data sent by client, come out of the loop
        if not data:
            break
			
		#conn.sendall(reply)
        
    
    conn.close()
#'Safe-closing' the connection


#Now keep talking with the client
while 1:

#Wait to accept a connection - blocking call
    conn, addr = s.accept()
	
    connected_clients = "Connected with " +addr[0] + ":" +str(addr[1])
	
    encode_client = connected_clients.encode('utf-8')
    conn.sendall(encode_client)
	
#Start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread, (conn,))
    
s.close()
#'Safe-closing' the socket
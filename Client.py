'''
Student Name: Venkata Ramana Voddam Pudi Sankar
Student ID: 1001614404
'''

import tkinter
#Using the standard Python GUI interface
#https://en.wikipedia.org/wiki/Tkinter

import socket
#Using sockets to communicated to and fro between Client and Server

import sys
#Provides information about constants, functions and methods of Python interpreter
#https://www.python-course.eu/sys_module.php

import os
#The OS module in Python provides a way of using operating system dependent functionality. 
#http://www.pythonforbeginners.com/os/pythons-os-module

import requests
from requests import Request, Session
#Requests allows us to send HTTP/1.1 requests using Python.
#http://www.pythonforbeginners.com/requests/using-requests-in-python


#Method def write is used to write to the Tkinter textboxes.
#GUIs reference: https://www.reddit.com/r/learnprogramming/comments/3vq0dm/python_how_can_i_print_text_out_in_the_gui_rather/
'''
Function write writes onto the text box in tkinter GUI
INPUT: string to be written on to the text box
OUTPUT: Text onto the text box
'''

def write(string):
	text_box.config(state=tkinter.NORMAL)
#State = tkinter.NORMAL makes the text box editable, using which we can write onto it.
#http://effbot.org/tkinterbook/text.htm
	
	text_box.insert("end", string + "\n")
#After writing each line, the insert automatically inserts a new line
	
	text_box.see("end")
	text_box.config(state=tkinter.DISABLED)
#State = tkinter.DISABLED makes the text box non-editable, so that it cannot be written anymore.

mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Creating a socket using AF_INET for IPv4 addressing and SOCK_STREAM for connection oriented TCP protocol.
#Client Server communication referred from https://www.binarytides.com/python-socket-programming-tutorial/

mysocket.connect(("127.0.0.1", 2346))
#Connects to 127.0.0.1, IP address of my localhost and to the port number 2346
	
#Below function connects the clients to Server and transmits data
	
'''
Function connected_clients establishes connection and sends and receives data from server
INPUT: IP address, port number and an acknowledgement to server
OUTPUT: Connection establishment with server and message transmissions
'''	
	
def connected_clients():
    mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Connects to 127.0.0.1, IP address of my localhost and to the port number 2346	
	
    mysocket.connect(("127.0.0.1", 2346))

    data = mysocket.send("Connection established".encode('utf-8'))
#Acknowledgement message converted to bytes using the encode function and send to Server
    
    receive_data = mysocket.recv(2346)
#recv method receives the data sent by Server to the Client thorough the port 2346
    
    write(str(receive_data))
#Write to the Tkinter text-box message received from Server.

'''
Function 'show_files_server' lists out files present at the Server side
INPUT : Path of server directory
OUTPUT: All files present in server directory
https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
'''
def show_files_server():
    write("FILES AT SERVER")
    file_list = os.listdir("C:\\Users\\Venkat\\Desktop\\DS Server Folder")
#Reading the files present at Server side
    
    result_list = '\n'.join(file_list)
#Storing the file names in result_list
    
    write(result_list)
#Writing out the variable to GUI

'''
Function 'show_files_client' lists out files present at the Client side
INPUT : Path of client directory
OUTPUT: All files present in client directory
https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
'''
def show_files_client():
    write("FILES AT CLIENT")
    file_list = os.listdir("C:\\Users\\Venkat\\Desktop\\DS Client Folder")
#Reading the files present at Client side
    
    result_list = '\n'.join(file_list)
#Storing the file names in result_list	
    
    write(result_list)
#Writing out the variable to GUI

'''
Function 'file_upload' transmits selected file name and contents to the server
INPUT: User selected file name
OUTPUT: Transmit user selected file name and contents to the server
'''

def file_upload():
    file_name = text_box.selection_get()

#Method selection_get gets a string out of a highlighted portion of a text
#https://stackoverflow.com/questions/4073468/how-do-i-get-a-selected-string-in-from-a-tkinter-text-box

    #print(file_name)
	
    file_read = open("C:\\Users\\Venkat\\Desktop\\DS Client Folder\\" + file_name)
	
#Open the particular file selected by user
    file_content = file_read.read()
#Read the file and store its content
    #print(file_content)	
	
    #encoded_file_name = file_name.encode('utf-8')
    #mysocket.sendall(encoded_file_name)
	
    file_name_content = file_name + '*' + file_content
#Appeding file content , separator('*')and the file name
    
    encoded_file_name_content = file_name_content.encode('utf-8')
#Encoding the above appended file content , separator('*')and the file name for transmission to the server


#This part encodes 'encoded_file_name_content' in HTTP format by adding
#headers, body, body bytes, header_bytes, content_type, content_length and host
#https://stackoverflow.com/questions/28670835/python-socket-client-post-parameters

    headers = """\
POST /auth HTTP/1.1\r
Content-Type: {content_type}\r
Content-Length: {content_length}\r
Host: {host}\r
Connection: close\r
\r\n"""

#Using the default HTTP header

#HTTP HEADER FIELDS:
#Content-Type: The Media type of the body of the request
#Content-Length: The length of the request body in octets
#Host: The domain name of the server (for virtual hosting), and the TCP port number on which the server is listening.
#Connection: Control options for the current connection and list of hop-by-hop request fields.
#https://en.wikipedia.org/wiki/List_of_HTTP_header_fields


#Giving a default body and encoding body as well as the header

    body = 'username=Venkat&password=pass\r'
    body_bytes = body.encode('ascii')
    header_bytes = headers.format(
    content_type="application/x-www-form-urlencoded",
    content_length=len(body_bytes),
    host=str('127.0.0.1') + ":" + str(2346)
).encode('iso-8859-1')

#Using encoding 'iso-8859-1'

    payload = header_bytes + body_bytes + encoded_file_name_content
#Appending body_bytes, encoded_file_name_content to header_bytes
    
    mysocket.sendall(payload)
#Sending the payload to server via socket

    '''
    def gen():
        yield encoded_file_name

    requests.post('http://127.0.0.1:2346', data = gen())	
	'''

'''
Function 'file_download' transmits selected file name and contents to the server
INPUT: User selected file name
OUTPUT: Transmit user selected file name and contents to the server
'''	
	
def file_download():
    file_name_d = text_box.selection_get()

#Method selection_get gets a string out of a highlighted portion of a text
#https://stackoverflow.com/questions/4073468/how-do-i-get-a-selected-string-in-from-a-tkinter-text-box

    #print(file_name_d)

    file_read_d = open("C:\\Users\\Venkat\\Desktop\\DS Server Folder\\" + file_name_d)
#Open the particular file selected by user
    
    file_content_d = file_read_d.read()
#Read the file and store its content
    #print(file_content_d)
	
	#encoded_file_name_d = file_name_d.encode('utf-8')
	
    file_name_content_d = file_name_d + '*' + file_content_d
#Appeding file content , separator('*')and the file name
    
    encoded_file_name_content_d = file_name_content_d.encode('utf-8')
#Encoding the above appended file content , separator('*')and the file name for transmission to the server


#This part encodes 'encoded_file_name_content' in HTTP format by adding
#headers, body, body bytes, header_bytes, content_type, content_length and host
#https://stackoverflow.com/questions/28670835/python-socket-client-post-parameters

	
    headers = """\
POST /auth HTTP/1.1\r
Content-Type: {content_type}\r
Content-Length: {content_length}\r
Host: {host}\r
Connection: close\r
\r\n"""

#Using the default HTTP header

#HTTP HEADER FIELDS:
#Content-Type: The Media type of the body of the request
#Content-Length: The length of the request body in octets
#Host: The domain name of the server (for virtual hosting), and the TCP port number on which the server is listening.
#Connection: Control options for the current connection and list of hop-by-hop request fields.
#https://en.wikipedia.org/wiki/List_of_HTTP_header_fields


#Giving a default body and encoding body as well as the header

    body = 'username=Venkat&password=pass\r'
    body_bytes = body.encode('ascii')
    header_bytes = headers.format(
    content_type="application/x-www-form-urlencoded",
    content_length=len(body_bytes),
    host=str('127.0.0.1') + ":" + str(2346)
).encode('iso-8859-1')

#Using encoding 'iso-8859-1'

    payload = header_bytes + body_bytes + encoded_file_name_content_d
#Appending body_bytes, encoded_file_name_content to header_bytes
    
    mysocket.sendall(payload)
#Sending the payload to server via socket
	
'''
Function 'client_disconnect' disconnects the connected client from server
INPUT: Button click
OUTPUT: Client and server are no longer connected
'''	
def client_disconnect():
    mysocket.close()
#Closing the socket to close the connection between client and server	
    
    write("Client disconnected")
#Printing to GUI.
	
'''
Function 'close_gui' closes the GUI
INPUT: Button click
OUTPUT: GUI closes

'''	
def close_gui():
    write("Goodbye!")
    root.destroy()
#Destroy method closes the Tkinter window(GUI)	

root = tkinter.Tk()
#Sets up the GUI.

root.title("Voddam Pudi Sankar_1001614404_Lab_1")
#The title for GUI window

text_box = tkinter.Text(root, state = tkinter.DISABLED)
#Creating a text box; state = tkinter.DISABLED makes it non-writable by default
#This text box will the made editable only during write operations by def write()

text_box.grid(row = 0, column = 0, columnspan = 1)
#Location of the text box

button_1 = tkinter.Button(root, text = "Connected Clients", command = connected_clients)
button_1.grid(row = 1, column = 1)

button_2 = tkinter.Button(root, text = "Files at Server", command = show_files_server)
button_2.grid(row = 1, column = 2)

button_2 = tkinter.Button(root, text = "Files at Client", command = show_files_client)
button_2.grid(row = 1, column = 3)

button_2 = tkinter.Button(root, text = "Select Upload", command = file_upload)
button_2.grid(row = 1, column = 4)

button_2 = tkinter.Button(root, text = "Select Download", command = file_download)
button_2.grid(row = 1, column = 5)

button_2 = tkinter.Button(root, text = "Disconnect Client", command = client_disconnect)
button_2.grid(row = 1, column = 6)

button_2 = tkinter.Button(root, text = "Close", command = close_gui)
button_2.grid(row = 1, column = 7)

#Creating required buttons at the afore-mentioned positions

root.mainloop()
#Closing the Tkinter window
#mysocket.close()
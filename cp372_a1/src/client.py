'''
---------------------------------
CP372 client.py file
---------------------------------
Author: Maxwell Forster, Kevin Chisholm
ID: 180662180, 181717310
Email: fors2180@mylaurier.ca, chis7310@mylaurier.ca
----
'''
# Import socket module
from socket import * 
import sys 

serverName = 'www.example.com' 
# Assign a port number
serverPort = 80

# Bind the socket to server address and server port
clientSocket = socket(AF_INET, SOCK_STREAM)

clientSocket.connect((serverName, serverPort))
sentence = 'GET / HTTP/1.1\r\nHost:%s\r\n\r\n' % serverName
clientSocket. send(sentence.encode())
modifiedSentence = clientSocket.recv(1024)

print('From server: ', modifiedSentence.decode())
clientSocket.close()


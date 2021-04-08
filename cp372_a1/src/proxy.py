'''
---------------------------------
CP372 class
---------------------------------
Author: Maxwell Forster, Kevin Chisholm
ID: 180662180, 181717310
Email: fors2180@mylaurier.ca, chis7310@mylaurier.ca
---------------------------------
'''
from socket import *
import multiprocessing
import os
import sys



if len(sys.argv) <= 1:
    print('Usage : python proxy.py server_port\n')
    sys.exit(2)

'''
The ReAll function is and extension of the recv function. What this does is takes the
recv function and sends it through a while loop that closes upon reaching the end of 
the information being sent from the server. This function breaks from the while loop
when the information being sent ends returning the full information back to the user.
'''


def ReAll(CS):
    buffer = CS.recv(1024)
    message = buffer
    if message.find(b'</html') != -1:
        return message
    while True:
        buffer = CS.recv(1024)
        message += buffer
        if message.find(b'</html') != -1:
            break
    return message


'''
The Stats function is the initalization of the important elelment in the program. To start the function will assign the tcpSerSock or server socket that
the rest of the program uses to function. next it initializes the SerSock with the 
input port and makes it listen to the localhost for information being sent.
'''


def Starts():
    tcpSerSock = socket(AF_INET, SOCK_STREAM)
    PORT = int(sys.argv[1])
    tcpSerSock.bind(('', PORT))
    tcpSerSock.listen(5)

    # sys.exit(2)
    path = os.getcwd() + "/cache"
    '''
    Next the function will create the cache for the program. This is done in two steps.
    First the program will try and create a file called cache where the proxy file is 
    located. If the file is already made then the exception happens assigning the cache
    as the location all the information will be stored. Once this is done it will delete
    all the information stored inside of the cache. This is done at the start every time
    the program is run meaning the cache will always be empty at the start of the program.
    '''
    try:
        for filename in os.listdir(path):
            os.remove(path + "/" + filename)
        os.rmdir(path)
    except OSError:
        path = os.getcwd() + "/cache"
    try:
        os.mkdir(path)
    except OSError:
        print("Cache already made")
    else:
        print("Cache creation worked")

    os.chdir(path)
    return(tcpSerSock)


'''
The RProxy server is the core of the program, this function holds all elements of the
proxy servers. This is the function that will be continuously called by the main function
until the program is terminated. 
'''


def RProxy(tcpCliSock, addr):
    '''
    To start the program will tell the user when a connection has been made. Once done
    the program will determine the begining message of the website will be sent. 
    Included in this is the filename which is the website URL, this will be used to get
    more information from the site later. Once the program has found the name of the website
    for example www.example.com it will make a copy of it with a / in front and send it to a
    try and catch.
    '''
    print('Received a connection from:', addr)
    message = tcpCliSock.recv(4096).decode()
    print(message)
    filename = message.split()[1].partition("/")[2]
    SPLIT = message.split()
    filename = SPLIT[1]
    filename = filename[1:]
    print(filename)
    fileExist = "false"
    filetouse = '/' + filename
    print(filetouse)
    '''
    The try statement will check to see if the website information has already been saved
    in the cache file. If it is the file will then be read and used to send the website 
    information to the localhost through the file in the cache. If the file is not already
    made however it will be caught by the exception. The exception will do the real work 
    grabbing the website information from online. It will start by comparing the file to see
    if the website has an error. This means that it will check for the error code at the top
    of the information. If a code other than 200 is sent then the code will check which code
    is being sent with the badReq function then print the error code to the website the user
    is tring to access.
    '''
    try:
        print("Checking to see if file exists")
        f = open(filetouse[1:], "r", encoding='ISO-8859-1')
        outputdata = f.readlines()
        fileExist = "true"
        print(outputdata[0])
        if(outputdata[0].encode() != b'200'):
            request = badReq(outputdata[0])
            tcpCliSock.send(b"HTTP/1.0 200 OK\r\n")
            tcpCliSock.send(b"Content-Type:text/html\r\n")
            tcpCliSock.send(request)
        else:
            tcpCliSock.send(b"HTTP/1.0 200 OK\r\n")
            tcpCliSock.send(b"Content-Type:text/html\r\n")
        for i in range(0, len(outputdata)):
            tcpCliSock.send(bytes(outputdata[i], encoding="utf-8"))
        print('Read from cache')
    except IOError:
        if fileExist == "false":
            serv_proxy = socket(AF_INET, SOCK_STREAM)
            hostname = filename
            hostn = hostname.replace("www.", "", 1)
            try:
                serv_proxy.connect((hostn, 80))
                print('Socket connected to port 80 of the host')
                request = ("GET / HTTP/1.1\r\nHost:%s\r\n\r\n" %
                           hostname).encode()

                serv_proxy.sendall(request)
                check = serv_proxy.recv(2048)
                temp = check
                check = check.decode().split(" ")
                if(b'200' not in check[1].encode()):
                    request = badReq(check[1])
                    tmpFile = open("./" + hostname, 'wb')

                    tmpFile.write(temp)
                    print(request)
                    tcpCliSock.send(b"HTTP/1.0 200 OK\r\n")
                    tcpCliSock.send(b"Content-Type:text/html\r\n\r\n")
                    tcpCliSock.send(
                        '<html><body><h1>{0}</body></html>'.format(request).encode())
                else:
                    response = temp + ReAll(serv_proxy)
                    tmpFile = open("./" + hostname, 'wb')
                    tmpFile.write(response)
                    check = response.decode()
                    tcpCliSock.send(response)

            except error as e:
                print(e)
                print("Illegal request")
        else:
            serv_proxy.close()
    tcpCliSock.close()


'''
The badReq function will determine which error code is being sent by the website and return
the error type to the Rproxy function to display. This is doen using if statements to check
from the list of accepted error codes. If the error is not part of the list a Bad Request 
statement will be set instead.
'''


def badReq(data):
    if ('301' in data):
        request = "301 Moved Permanently"
        request = request.encode()
    elif('302' in data):
        request = "302 Found"
        request = request.encode()
    elif('400' in data):
        request = "Bad Request"
        request = request.encode()
    elif('404' in data):
        request = "404 Not Found"
        request = request.encode()
    elif('500' in data):
        request = "500 Internal Server Error"
        request = request.encode()
    else:
        request = "Bad Request"
        request = request.encode()
    return request


'''
The main function contains the multi-processing portion of the code.This function starts
code by calling the Starts function explained above. Once done the a while loop will run
allowing the Process to run. useing multiprocessing allows multiple requests to be run
at once so this was used instead of threads.
'''
if __name__ == "__main__":
    tcpSerSock = Starts()
    print("Ready to serve...")
    while 1:
        tcpCliSock, addr = tcpSerSock.accept()
        process = multiprocessing.Process(
            target=RProxy, args=(tcpCliSock, addr))
        process.daemon = True
        process.start()
    for process in multiprocessing.active_children():
        process.terminate()
        process.join()

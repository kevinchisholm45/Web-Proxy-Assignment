
---------------------------------
CP372 Read Me Documentation
---------------------------------
Author: Kevin Chisholm, Maxwell Forster
---------------------------------

How to run our Proxy
_______________________________________
To begin, find the correct pathway to proxy.py in your directory which will 
used to run the proxy from the commandline. One you have found the correct directory
pathway, insert python proxy.py (port number) into the command line. In this case 
(port number) will be a four digit number (0000 to 9999) which will be your server port
number while using the proxy. "Ready to serve..." along with the status of your cache will appear.

From here open up a browser (empty your browser history/cache) and insert into the address bar:
http://localhost:8888/www.google.com. In this case, 8888 will be the port number you previously 
entered into the command line and www.google.com will be the web server you are sending the request to.
Our proxy is not to designed to work with HTTPS servers such as YouTube.com or GoogleMaps.com.
After the web page has loaded, the information regarding the sites objects/layouts will be stored in a cache folder. 
If one is not already present it will be created and if a cache folder already existed the previous one will be deleted.
When stored in cache a web server, when attempted to be accessed an additional time will be accessed from the
cache instead, however if you restart the web server it will be deleted.


Design Decisions
_________________________________________

For the multiprocessing portion of our code we applied the process work work within our "Main" function 
to allow for multiple processes to utilize the same code at the same moment. Caching in our code works by the calling of the program 
to initialize a cache folder in memory. If it is the file will then be read and used to send the website information to the localhost 
through the file in the cache. If the file is not already made however it will be caught by the exception. The exception will do the real work 
grabbing the website information from online. It will start by comparing the file to see if the website has an error. This means
that it will check for the error code at the top  of the information. If a code other than 200 is sent then the code will check which code
is being sent with the badReq function then print the error code to the website the user is trying to access. The badReq function will 
determine which error code is being sent by the website and return the error type to the Rproxy function to display. This is doen using 
if statements to check from the list of accepted error codes. If the error is not part of the list a Bad Request statement will be set instead.

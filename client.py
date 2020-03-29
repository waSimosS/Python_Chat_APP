
import socket
SERVER = "192.168.43.96"
PORT = 8099
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))  
while True :
       msg=client.recv(1024)
       print msg
       if  msg=="exit":
           break
       ch=raw_input(">")
       client.send(ch)
       

                   
client.close()


from dataclasses import dataclass
from socket import *
serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)

waitingForUsername = True
while waitingForUsername:
    print('Enter username:')
    usernameInput = input()
    clientSocket.sendto(usernameInput.encode(), (serverName, serverPort))
    loginResponse, serverAddress = clientSocket.recvfrom(2048)
    if loginResponse.decode() == "Username found!":
        waitingForUsername = False
    else:
        print(loginResponse.decode())

waitingForPassword = True
while waitingForPassword:
    print('Enter password:')
    passwordInput = input()
    clientSocket.sendto(passwordInput.encode(), (serverName, serverPort))
    loginResponse, serverAddress = clientSocket.recvfrom(2048)
    if loginResponse.decode() == "Password correct!":
        waitingForPassword = False
    else:
        print(loginResponse.decode())

#message = input('Input lowercase sentence:')
#clientSocket.sendto(message.encode(),(serverName, serverPort))
#modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
#print (modifiedMessage.decode())
clientSocket.close()

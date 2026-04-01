from dataclasses import dataclass
from socket import *
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
@dataclass #warrior class
class Warrior:
    username: str
    password: str
    lives: int = 2
    #avatar
    sword: int = -1
    sheild: int = -1
    slayingPotion: int = -1
    healingPotion: int = -1

users = {
    "A": Warrior("A", "A"),
    "B": Warrior("B", "B"),
    "C": Warrior("C", "C"),
    "D": Warrior("D", "D")
}
fightRequests = []
#print ('The server is ready to receive')
waitingForUsername = True
while waitingForUsername:
    usernameInput, clientAddress = serverSocket.recvfrom(2048)
    if usernameInput.decode() in users:
        warriorLoggingIn = users[usernameInput.decode()]
        loginResponse = "Username found!"
        serverSocket.sendto(loginResponse.encode(), clientAddress)
        waitingForUsername = False
    else:
        loginResponse = "Username not found, try again"
        serverSocket.sendto(loginResponse.encode(), clientAddress)

waitingForPassword = True
while waitingForPassword:
    passwordInput, clientAddress = serverSocket.recvfrom(2048)
    if passwordInput.decode() == warriorLoggingIn.password:
        loginResponse = "Password correct!"
        serverSocket.sendto(loginResponse.encode(), clientAddress)
        waitingForPassword = False
    else:
        loginResponse = "Password incorrect, try again"
        serverSocket.sendto(loginResponse.encode(), clientAddress)
    #message, clientAddress = serverSocket.recvfrom(2048)
    #modifiedMessage = message.decode().upper()
    #serverSocket.sendto(modifiedMessage.encode(), clientAddress)

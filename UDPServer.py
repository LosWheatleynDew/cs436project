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
    firstTimeLogin: bool = True

users = {
    "A": Warrior("A", "A"),
    "B": Warrior("B", "B", lives = 1, sword = 1),
    "C": Warrior("C", "C"),
    "D": Warrior("D", "D")
}
fightRequests = []
print ('The server is ready to receive')

def login():
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

    if warriorLoggingIn.firstTimeLogin:
        serverSocket.sendto("First time login".encode(), clientAddress)
    while warriorLoggingIn.firstTimeLogin:
        serverSocket.sendto("Input sword strength:".encode(), clientAddress)
        swordSetup = False
        while not swordSetup:
            swordInput, clientAddress = serverSocket.recvfrom(2048)
            if swordInput.decode().isdigit() and 0 <= int(swordInput.decode()) <= 3:
                warriorLoggingIn.sword = int(swordInput.decode())
                swordSetup = True
            else:
                serverSocket.sendto("Invalid sword strength. Please enter a number between 0 and 3:".encode(), clientAddress)
        sheildSetup = False
        while not sheildSetup:
            serverSocket.sendto("Input sheild strength:".encode(), clientAddress)
            sheildInput, clientAddress = serverSocket.recvfrom(2048)
            if sheildInput.decode().isdigit() and 0 <= int(sheildInput.decode()) <= 3:
                warriorLoggingIn.sheild = int(sheildInput.decode())
                sheildSetup = True
            else:
                serverSocket.sendto("Invalid sheild strength. Please enter a number between 0 and 3:".encode(), clientAddress)
        slayingPotionSetup = False
        while not slayingPotionSetup:
            serverSocket.sendto("Input slaying potion strength:".encode(), clientAddress)
            slayingPotionInput, clientAddress = serverSocket.recvfrom(2048)
            if slayingPotionInput.decode().isdigit() and 0 <= int(slayingPotionInput.decode()) <= 3:
                warriorLoggingIn.slayingPotion = int(slayingPotionInput.decode())
                slayingPotionSetup = True
            else:
                serverSocket.sendto("Invalid slaying potion strength. Please enter a number between 0 and 3:".encode(), clientAddress)
        healingPotionSetup = False
        while not healingPotionSetup:
            serverSocket.sendto("Input healing potion strength:".encode(), clientAddress)
            healingPotionInput, clientAddress = serverSocket.recvfrom(2048)
            if healingPotionInput.decode().isdigit() and 0 <= int(healingPotionInput.decode()) <= 3:
                warriorLoggingIn.healingPotion = int(healingPotionInput.decode())
                healingPotionSetup = True
            else:
                serverSocket.sendto("Invalid healing potion strength. Please enter a number between 0 and 3:".encode(), clientAddress)
        if warriorLoggingIn.sword + warriorLoggingIn.sheild + warriorLoggingIn.slayingPotion + warriorLoggingIn.healingPotion != 10:
            serverSocket.sendto("Total strength is not 10. Please re-enter your strengths.".encode(), clientAddress)
            continue
        else:
            warriorLoggingIn.firstTimeLogin = False
            serverSocket.sendto("Total strength is 10. Setup complete.".encode(), clientAddress)
            break

def listUsers(clientAddress):
    for x in users:
        if(users[x].lives > 0 and users[x].sword != -1):
            serverSocket.sendto(x.encode(), clientAddress)
    serverSocket.sendto("No more users".encode(), clientAddress)
        
while True:
    message, clientAddress = serverSocket.recvfrom(2048)
    command = message.decode()
    if command == "login":
        login()
    elif command == "1":
        listUsers(clientAddress)
    


    #message, clientAddress = serverSocket.recvfrom(2048)
    #modifiedMessage = message.decode().upper()
    #serverSocket.sendto(modifiedMessage.encode(), clientAddress)

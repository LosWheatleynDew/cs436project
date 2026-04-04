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
    shield: int = -1
    slayingPotion: int = -1
    healingPotion: int = -1
    firstTimeLogin: bool = True

users = {
    "A": Warrior("A", "A"),
    "B": Warrior("B", "B", lives=1, sword=1, shield = 3, slayingPotion=1, healingPotion = 1, firstTimeLogin=False),
    "C": Warrior("C", "C"),
    "D": Warrior("D", "D")
}
fightRequests = []
print ('The server is ready to receive')

def login():
    waitingForUsername = True
    while waitingForUsername:
        usernameInput, clientAddress = serverSocket.recvfrom(2048)
        username = usernameInput.decode().strip()
        warriorLoggingIn = None
        for warrior in users.values():
            if warrior.username == username:
                warriorLoggingIn = warrior
                break
        if warriorLoggingIn is not None:
            loginResponse = "Username found!"
            serverSocket.sendto(loginResponse.encode(), clientAddress)
            waitingForUsername = False
        else:
            loginResponse = "Username not found, try again"
            serverSocket.sendto(loginResponse.encode(), clientAddress)

    waitingForPassword = True
    while waitingForPassword:
        passwordInput, clientAddress = serverSocket.recvfrom(2048)
        if passwordInput.decode().strip() == warriorLoggingIn.password:
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
            if swordInput.decode().strip().isdigit() and 0 <= int(swordInput.decode().strip()) <= 3:
                warriorLoggingIn.sword = int(swordInput.decode())
                swordSetup = True
            else:
                serverSocket.sendto("Invalid sword strength. Please enter a number between 0 and 3:".encode(), clientAddress)
        shieldSetup = False
        while not shieldSetup:
            serverSocket.sendto("Input shield strength:".encode(), clientAddress)
            shieldInput, clientAddress = serverSocket.recvfrom(2048)
            if shieldInput.decode().strip().isdigit() and 0 <= int(shieldInput.decode().strip()) <= 3:
                warriorLoggingIn.shield = int(shieldInput.decode())
                shieldSetup = True
            else:
                serverSocket.sendto("Invalid shield strength. Please enter a number between 0 and 3:".encode(), clientAddress)
        slayingPotionSetup = False
        while not slayingPotionSetup:
            serverSocket.sendto("Input slaying potion strength:".encode(), clientAddress)
            slayingPotionInput, clientAddress = serverSocket.recvfrom(2048)
            if slayingPotionInput.decode().strip().isdigit() and 0 <= int(slayingPotionInput.decode().strip()) <= 3:
                warriorLoggingIn.slayingPotion = int(slayingPotionInput.decode())
                slayingPotionSetup = True
            else:
                serverSocket.sendto("Invalid slaying potion strength. Please enter a number between 0 and 3:".encode(), clientAddress)
        healingPotionSetup = False
        while not healingPotionSetup:
            serverSocket.sendto("Input healing potion strength:".encode(), clientAddress)
            healingPotionInput, clientAddress = serverSocket.recvfrom(2048)
            if healingPotionInput.decode().strip().isdigit() and 0 <= int(healingPotionInput.decode().strip()) <= 3:
                warriorLoggingIn.healingPotion = int(healingPotionInput.decode())
                healingPotionSetup = True
            else:
                serverSocket.sendto("Invalid healing potion strength. Please enter a number between 0 and 3:".encode(), clientAddress)
        if warriorLoggingIn.sword + warriorLoggingIn.shield + warriorLoggingIn.slayingPotion + warriorLoggingIn.healingPotion != 10:
            serverSocket.sendto("Total strength is not 10. Please re-enter your strengths.".encode(), clientAddress)
            continue
        else:
            warriorLoggingIn.firstTimeLogin = False
            serverSocket.sendto("Total strength is 10. Setup complete.".encode(), clientAddress)
            break

def listUsers(clientAddress):
    for x in users:
        if(users[x].lives > 0 and users[x].sword != -1):
            serverSocket.sendto(users[x].username.encode(), clientAddress)
    serverSocket.sendto("No more users".encode(), clientAddress)

def fight(clientAddress):
    initiatorResponse, clientAddress = serverSocket.recvfrom(2048)
    initiatorUsername = initiatorResponse.decode().strip()
    initiator = None
    for warrior in users.values():
        if warrior.username == initiatorUsername:
            initiator = warrior
            break
    if initiator is None or initiator.lives <= 0:
        serverSocket.sendto("Cannot initiate fight".encode(), clientAddress)
        return
    #receive opponent username
    opponentUsername, clientAddress = serverSocket.recvfrom(2048)
    opponentUsername = opponentUsername.decode().strip()
    opponent = None
    for warrior in users.values():
        if warrior.username == opponentUsername:
            opponent = warrior
            break
    if opponent is None or opponent.lives <= 0:
        serverSocket.sendto("Cannot initiate fight".encode(), clientAddress)
        return
    else:
        fightRequests.append((initiator, opponent))
        serverSocket.sendto("Fight request sent".encode(), clientAddress)
    weaponResponse, clientAddress = serverSocket.recvfrom(2048)
    weaponChoice = weaponResponse.decode().strip()
    newPowerType = None
    newPowerValue = 0
    if weaponChoice == "1":
        if initiator.sword < 0 or opponent.shield < 0:
            serverSocket.sendto("Cannot initiate fight".encode(), clientAddress)
            return
        initiatorPower = initiator.sword
        opponentPower = opponent.shield
        if initiatorPower == opponentPower:
            initiator.lives -= 1
            opponent.lives -= 1
            serverSocket.sendto("Tie".encode(), clientAddress)
        elif initiatorPower > opponentPower:
            initiator.lives += 1
            opponent.lives -= 1
            serverSocket.sendto("Win".encode(), clientAddress)
        else:
            initiator.lives -= 1
            opponent.lives += 1
            serverSocket.sendto("Lose".encode(), clientAddress)
        initiator.sword -= opponentPower
        if initiator.sword < 0:
            initiator.sword = 0
        opponent.shield -= initiatorPower
        if opponent.shield < 0:
            opponent.shield = 0
        newPowerType = "sword"
        newPowerValue = initiator.sword
    elif weaponChoice == "2":
        if initiator.slayingPotion < 0 or opponent.healingPotion < 0:
            serverSocket.sendto("Cannot initiate fight".encode(), clientAddress)
            return
        initiatorPower = initiator.slayingPotion
        opponentPower = opponent.healingPotion
        if initiatorPower == opponentPower:
            initiator.lives -= 1
            opponent.lives -= 1
            serverSocket.sendto("Tie".encode(), clientAddress)
        elif initiatorPower > opponentPower:
            initiator.lives += 1
            opponent.lives -= 1
            serverSocket.sendto("Win".encode(), clientAddress)
        else:
            initiator.lives -= 1
            opponent.lives += 1
            serverSocket.sendto("Lose".encode(), clientAddress)
        initiator.slayingPotion -= opponentPower
        if initiator.slayingPotion < 0:
            initiator.slayingPotion = 0
        opponent.healingPotion -= initiatorPower
        if opponent.healingPotion < 0:
            opponent.healingPotion = 0
        newPowerType = "slaying"
        newPowerValue = initiator.slayingPotion
    else:
        serverSocket.sendto("Invalid weapon choice".encode(), clientAddress)
        return
    serverSocket.sendto(f"{newPowerType}:{newPowerValue}".encode(), clientAddress)
    return

while True:
    message, clientAddress = serverSocket.recvfrom(2048)
    command = message.decode().strip()
    if command == "login":
        login()
    elif command == "1":
        listUsers(clientAddress)
    elif command == "3":
        fight(clientAddress)

    


    #message, clientAddress = serverSocket.recvfrom(2048)
    #modifiedMessage = message.decode().upper()
    #serverSocket.sendto(modifiedMessage.encode(), clientAddress)


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

users = { #list of users
    "A": Warrior("A", "A"),
    "B": Warrior("B", "B", lives=1, sword=1, shield = 1, slayingPotion=1, healingPotion = 1, firstTimeLogin=False),
    "C": Warrior("C", "C"),
    "D": Warrior("D", "D")
}
fightRequests = [] #list of fight requests (currently not really used)
print ('The server is ready to receive')

def login(): #function to handle user login and avatar setup.
    waitingForUsername = True
    while waitingForUsername: #loop until valid username is received
        usernameInput, clientAddress = serverSocket.recvfrom(2048)
        username = usernameInput.decode().strip()
        warriorLoggingIn = None
        for warrior in users.values(): #loop through users to find matching username
            if warrior.username == username: #if matching username is found, set warriorLoggingIn to that user and break loop
                warriorLoggingIn = warrior
                break
        if warriorLoggingIn is not None: #if matching username is found, send success message and break loop
            loginResponse = "Username found!"
            serverSocket.sendto(loginResponse.encode(), clientAddress)
            waitingForUsername = False
        else: #if no matching username is found, send error message and loop again for new username input
            loginResponse = "Username not found, try again"
            serverSocket.sendto(loginResponse.encode(), clientAddress)

    waitingForPassword = True
    while waitingForPassword: #loop until correct password is received for the username.
        passwordInput, clientAddress = serverSocket.recvfrom(2048)
        if passwordInput.decode().strip() == warriorLoggingIn.password: #if password input matches password for the username, send success message and break loop
            loginResponse = "Password correct!"
            serverSocket.sendto(loginResponse.encode(), clientAddress)
            waitingForPassword = False
        else: #if password input does not match password for the username, send error message and loop again for new password input
            loginResponse = "Password incorrect, try again"
            serverSocket.sendto(loginResponse.encode(), clientAddress)

    if warriorLoggingIn.firstTimeLogin: #if this is the user's first time logging in, send message and loop through receiving avatar stat inputs until valid input is received and total strength is 10
        serverSocket.sendto("First time login".encode(), clientAddress)
    else: #if not first time login, send current stats. Format is "sword:shield:slayingPotion:healingPotion"
        stats = f"sword:{warriorLoggingIn.sword},shield:{warriorLoggingIn.shield},slayingPotion:{warriorLoggingIn.slayingPotion},healingPotion:{warriorLoggingIn.healingPotion}"
        serverSocket.sendto(stats.encode(), clientAddress)
    while warriorLoggingIn.firstTimeLogin: #loop until valid avatar stat inputs are received and total strength is 10
        serverSocket.sendto("Input sword strength:".encode(), clientAddress)
        swordSetup = False
        while not swordSetup: #loop until valid sword strength input is received
            swordInput, clientAddress = serverSocket.recvfrom(2048)
            if swordInput.decode().strip().isdigit() and 0 <= int(swordInput.decode().strip()) <= 3: #if sword strength input is a digit between 0 and 3, set sword strength for the user and break loop
                warriorLoggingIn.sword = int(swordInput.decode())
                swordSetup = True
            else: #if sword strength input is not a digit between 0 and 3, send error message and loop again for new sword strength input
                serverSocket.sendto("Invalid sword strength. Please enter a number between 0 and 3:".encode(), clientAddress)
        shieldSetup = False
        serverSocket.sendto("Input shield strength:".encode(), clientAddress)
        while not shieldSetup: #loop until valid shield strength input is received
            shieldInput, clientAddress = serverSocket.recvfrom(2048)
            if shieldInput.decode().strip().isdigit() and 0 <= int(shieldInput.decode().strip()) <= 3: #if shield strength input is a digit between 0 and 3, set shield strength for the user and break loop
                warriorLoggingIn.shield = int(shieldInput.decode())
                shieldSetup = True
            else: #if shield strength input is not a digit between 0 and 3, send error message and loop again for new shield strength input
                serverSocket.sendto("Invalid shield strength. Please enter a number between 0 and 3:".encode(), clientAddress)
        slayingPotionSetup = False
        serverSocket.sendto("Input slaying potion strength:".encode(), clientAddress)
        while not slayingPotionSetup: #loop until valid slaying potion strength input is received
            slayingPotionInput, clientAddress = serverSocket.recvfrom(2048)
            if slayingPotionInput.decode().strip().isdigit() and 0 <= int(slayingPotionInput.decode().strip()) <= 3: #if slaying potion strength input is a digit between 0 and 3, set slaying potion strength for the user and break loop
                warriorLoggingIn.slayingPotion = int(slayingPotionInput.decode())
                slayingPotionSetup = True
            else: #if slaying potion strength input is not a digit between 0 and 3, send error message and loop again for new slaying potion strength input
                serverSocket.sendto("Invalid slaying potion strength. Please enter a number between 0 and 3:".encode(), clientAddress)
        healingPotionSetup = False
        serverSocket.sendto("Input healing potion strength:".encode(), clientAddress)
        while not healingPotionSetup: #loop until valid healing potion strength input is received
            healingPotionInput, clientAddress = serverSocket.recvfrom(2048)
            if healingPotionInput.decode().strip().isdigit() and 0 <= int(healingPotionInput.decode().strip()) <= 3: #if healing potion strength input is a digit between 0 and 3, set healing potion strength for the user and break loop
                warriorLoggingIn.healingPotion = int(healingPotionInput.decode())
                healingPotionSetup = True
            else: #if healing potion strength input is not a digit between 0 and 3, send error message and loop again for new healing potion strength input
                serverSocket.sendto("Invalid healing potion strength. Please enter a number between 0 and 3:".encode(), clientAddress)
        if warriorLoggingIn.sword + warriorLoggingIn.shield + warriorLoggingIn.slayingPotion + warriorLoggingIn.healingPotion != 10: #if total strength of the avatar is not 10, send error message and loop again for new avatar stat inputs
            serverSocket.sendto("Total strength is not 10. Please re-enter your strengths.".encode(), clientAddress)
            continue
        else: #if total strength of the avatar is 10, send success message and break loop
            warriorLoggingIn.firstTimeLogin = False
            serverSocket.sendto("Total strength is 10. Setup complete.".encode(), clientAddress)
            break
    else: #if not first time login, just send current stats
        serverSocket.sendto(f"{warriorLoggingIn.sword}:{warriorLoggingIn.shield}:{warriorLoggingIn.slayingPotion}:{warriorLoggingIn.healingPotion}".encode(), clientAddress)

def listUsers(clientAddress): #function to send list of active users to client.
    for x in users: #loop through users and send username of each user with lives > 0 and sword != -1
        if(users[x].lives > 0 and users[x].sword != -1): #if user has more than 0 lives and has set up avatar (sword strength is not -1), send username to client
            serverSocket.sendto(users[x].username.encode(), clientAddress)
    serverSocket.sendto("No more users".encode(), clientAddress)

def fight(clientAddress): #function to handle fight requests
    initiatorResponse, clientAddress = serverSocket.recvfrom(2048)
    initiatorUsername = initiatorResponse.decode().strip()
    initiator = None
    for warrior in users.values(): #loop through users to find matching username for initiator
        if warrior.username == initiatorUsername: #if matching username is found, set initiator to that user and break loop
            initiator = warrior
            break
    if initiator is None or initiator.lives <= 0: #if no matching username is found or initiator has 0 or less lives, send error message and return
        serverSocket.sendto("Cannot initiate fight".encode(), clientAddress)
        return
    printTable(clientAddress)
    #receive opponent username
    opponentUsername, clientAddress = serverSocket.recvfrom(2048)
    opponentUsername = opponentUsername.decode().strip()
    opponent = None
    for warrior in users.values(): #loop through users to find matching username for opponent
        if warrior.username == opponentUsername: #if matching username is found, set opponent to that user and break loop
            opponent = warrior
            break
    if opponent is None or opponent.lives <= 0: #if no matching username is found or opponent has 0 or less lives, send error message and return
        serverSocket.sendto("Cannot initiate fight".encode(), clientAddress)
        return
    else: #if valid opponent is found, add fight request to list of fight requests and send success message to client. 
        serverSocket.sendto("Fight request sent".encode(), clientAddress)
    weaponResponse, clientAddress = serverSocket.recvfrom(2048)
    weaponChoice = weaponResponse.decode().strip()
    strengthResponse, clientAddress = serverSocket.recvfrom(2048)
    initiatorPowerRaw = strengthResponse.decode().strip()
    if not initiatorPowerRaw.isdigit(): #if strength input is not a digit, send error message and return
        serverSocket.sendto("Invalid strength".encode(), clientAddress)
        return
    initiatorPower = int(initiatorPowerRaw)
    newPowerType = None
    newPowerValue = 0
    if weaponChoice == "1": #if weapon choice is sword, compare sword strength of initiator and opponent to determine fight outcome, update stats accordingly, and set new power update message for initiator
        if opponent.shield < 0:
            serverSocket.sendto("Cannot initiate fight".encode(), clientAddress)
            return
        opponentPower = opponent.shield
        if initiatorPower == opponentPower: # if initiator and opponent power are equal, it's a tie and both users lose a life
            initiator.lives -= 1
            opponent.lives -= 1
            serverSocket.sendto("Tie".encode(), clientAddress)
        elif initiatorPower > opponentPower: # if initiator power is greater than opponent power, initiator wins and gains a life while opponent loses a life
            initiator.lives += 1
            opponent.lives -= 1
            serverSocket.sendto("Win".encode(), clientAddress)
        else: # if opponent power is greater than initiator power, opponent wins and gains a life while initiator loses a life
            initiator.lives -= 1
            opponent.lives += 1
            serverSocket.sendto("Lose".encode(), clientAddress)
        initiator.sword = initiatorPower - opponentPower
        if initiator.sword < 0: #if initiator sword strength is less than 0 after the fight, set it to 0
            initiator.sword = 0
        opponent.shield -= initiatorPower
        if opponent.shield < 0: #if opponent shield strength is less than 0 after the fight, set it to 0
            opponent.shield = 0
        newPowerType = "sword"
        newPowerValue = initiator.sword
    elif weaponChoice == "2": #if weapon choice is slaying potion, compare slaying potion strength of initiator and opponent to determine fight outcome, update stats accordingly, and set new power update message for initiator
        if opponent.healingPotion < 0: #if opponent healing potion strength is less than 0, cannot initiate fight so send error message and return
            serverSocket.sendto("Cannot initiate fight".encode(), clientAddress)
            return
        opponentPower = opponent.healingPotion
        if initiatorPower == opponentPower: # if initiator and opponent power are equal, it's a tie and both users lose a life
            initiator.lives -= 1
            opponent.lives -= 1
            serverSocket.sendto("Tie".encode(), clientAddress)
        elif initiatorPower > opponentPower: # if initiator power is greater than opponent power, initiator wins and gains a life while opponent loses a life
            initiator.lives += 1
            opponent.lives -= 1
            serverSocket.sendto("Win".encode(), clientAddress)
        else: #if opponent power is greater than initiator power, opponent wins and gains a life while initiator loses a life
            initiator.lives -= 1
            opponent.lives += 1
            serverSocket.sendto("Lose".encode(), clientAddress)
        initiator.slayingPotion -= opponentPower
        if initiator.slayingPotion < 0: #if initiator slaying potion strength is less than 0 after the fight, set it to 0
            initiator.slayingPotion = 0
        opponent.healingPotion -= initiatorPower
        if opponent.healingPotion < 0: #if opponent healing potion strength is less than 0 after the fight, set it to 0
            opponent.healingPotion = 0
        newPowerType = "slaying"
        newPowerValue = initiator.slayingPotion
    else: #if weapon choice is not recognized, send error message and return
        serverSocket.sendto("Invalid weapon choice".encode(), clientAddress)
        return
    serverSocket.sendto(f"{newPowerType}:{newPowerValue}".encode(), clientAddress)
    printTable(clientAddress)
    return

def printTable(clientAddress): #function to send table of active users and their stats to client
    for x in users: #loop through users and send username and stats of each user with lives > 0 and sword != -1, then send "No more users" message to indicate end of list
        if(users[x].lives > 0 and users[x].sword != -1): #if user has more than 0 lives and has set up avatar (sword strength is not -1), send username and stats to client
            tableRow = f"| {users[x].username}           | {users[x].sword}      | {users[x].shield}     | {users[x].slayingPotion}              | {users[x].healingPotion}             | {users[x].lives}     |"
            serverSocket.sendto(tableRow.encode(), clientAddress)
    serverSocket.sendto("No more users".encode(), clientAddress)


while True: #main server loop to receive commands from clients and call appropriate functions based on the command received
    message, clientAddress = serverSocket.recvfrom(2048)
    command = message.decode().strip()
    if command == "login": #if command is "login", call login function
        login()
    elif command == "1": #if command is "1", call listUsers function
        listUsers(clientAddress)
    elif command == "4": #if command is "4", call fight function
        fight(clientAddress)
    elif command == "5": #if command is "5", call printTable function
        printTable(clientAddress)


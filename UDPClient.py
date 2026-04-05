from dataclasses import dataclass
from socket import *
serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)

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

warrior = Warrior()

clientSocket.sendto("login".encode(), (serverName, serverPort))
waitingForUsername = True
while waitingForUsername:
    print('Enter username:')
    usernameInput = input()
    clientSocket.sendto(usernameInput.encode(), (serverName, serverPort))
    loginResponse, serverAddress = clientSocket.recvfrom(2048)
    if loginResponse.decode() == "Username found!":
        warrior.username = usernameInput
        waitingForUsername = False
    else:
        print(loginResponse.decode())

waitingForPassword = True
while waitingForPassword:
    print('Enter password:')
    passwordInput = input()
    warrior.password = passwordInput
    clientSocket.sendto(passwordInput.encode(), (serverName, serverPort))
    loginResponse, serverAddress = clientSocket.recvfrom(2048)
    if loginResponse.decode() == "Password correct!":
        waitingForPassword = False
    else:
        print(loginResponse.decode())

firstTimeLoginResponse, serverAddress = clientSocket.recvfrom(2048)
if firstTimeLoginResponse.decode() == "First time login":
    firstTimeLogin = True
else:
    firstTimeLogin = False
while firstTimeLogin:
    # sword prompt + validation
    while True:
        prompt, serverAddress = clientSocket.recvfrom(2048)
        prompt_text = prompt.decode()
        print(prompt_text)
        swordStrength = input()
        clientSocket.sendto(swordStrength.encode(), (serverName, serverPort))
        response, serverAddress = clientSocket.recvfrom(2048)
        response_text = response.decode()
        if response_text.startswith("Invalid sword strength"):
            print(response_text)
            continue
        warrior.sword = int(swordStrength)
        # next prompt from server is shield
        shield_prompt = response_text
        break

    # shield prompt + validation
    while True:
        print(shield_prompt)
        shieldStrength = input()
        clientSocket.sendto(shieldStrength.encode(), (serverName, serverPort))
        response, serverAddress = clientSocket.recvfrom(2048)
        response_text = response.decode()
        if response_text.startswith("Invalid shield strength"):
            print(response_text)
            continue
        warrior.shield = int(shieldStrength)
        slaying_prompt = response_text
        break

    # slaying potion prompt + validation
    while True:
        print(slaying_prompt)
        slayingPotionStrength = input()
        clientSocket.sendto(slayingPotionStrength.encode(), (serverName, serverPort))
        response, serverAddress = clientSocket.recvfrom(2048)
        response_text = response.decode()
        if response_text.startswith("Invalid slaying potion strength"):
            print(response_text)
            continue
        warrior.slayingPotion = int(slayingPotionStrength)
        healing_prompt = response_text
        break

    # healing potion prompt + validation
    while True:
        print(healing_prompt)
        healingPotionStrength = input()
        clientSocket.sendto(healingPotionStrength.encode(), (serverName, serverPort))
        response, serverAddress = clientSocket.recvfrom(2048)
        response_text = response.decode()
        if response_text.startswith("Invalid healing potion strength"):
            print(response_text)
            continue
        warrior.healingPotion = int(healingPotionStrength)

        # reached final verification response (total strength check)
        if response_text.startswith("Total strength is not 10"):
            print(response_text)
            break
        if response_text.startswith("Total strength is 10"):
            print(response_text)
            firstTimeLogin = False
            break

        # If we get an unexpected reply, print and exit loop.
        print(response_text)
        firstTimeLogin = False
        break

def listUsers():
    nextUser, serverAddress = clientSocket.recvfrom(2048)
    while nextUser.decode() != "No more users":
        print(nextUser.decode())
        nextUser, serverAddress = clientSocket.recvfrom(2048)




def fight():
    initiator = warrior.username
    clientSocket.sendto(initiator.encode(), (serverName, serverPort))
    print(f'''
__________________________________________________________________________
| Active User | sword | shield | slaying-potion | healing-potion | lives |      
| A           | {warrior.sword}      | {warrior.shield}     | {warrior.slayingPotion}              | {warrior.healingPotion}             | {warrior.lives}     |
| B           |
| C           |
|_________________________________________________________________________
''')
    print("Enter username of player you want to fight:")
    opponent = input()
    clientSocket.sendto(opponent.encode(), (serverName, serverPort))
    fightResponse, serverAddress = clientSocket.recvfrom(2048)
    fightResponseText = fightResponse.decode()
    
    if fightResponseText == "Fight request sent":
        print("Select weapon:\n 1. Sword\n 2. Slaying Potion")
        weaponChoice = input().strip()
        clientSocket.sendto(weaponChoice.encode(), (serverName, serverPort))
        fightOutcome, serverAddress = clientSocket.recvfrom(2048)
        fightOutcomeText = fightOutcome.decode()
        
        if fightOutcomeText == "Tie":
            warrior.lives -= 1
        elif fightOutcomeText == "Win":
            warrior.lives += 1
        elif fightOutcomeText == "Lose":
            warrior.lives -= 1
        
        print(fightOutcomeText, "You have " + str(warrior.lives) + " lives remaining.")
        newPowerMessage, serverAddress = clientSocket.recvfrom(2048)
        newPowerText = newPowerMessage.decode()
        if newPowerText.startswith("sword:"):
            warrior.sword = int(newPowerText.split(":", 1)[1])
            print("Your sword strength is now", warrior.sword)
        elif newPowerText.startswith("slaying:"):
            warrior.slayingPotion = int(newPowerText.split(":", 1)[1])
            print("Your slaying potion strength is now", warrior.slayingPotion)
        else:
            print(newPowerText)
    else:
        print(fightResponseText)
    print(f'''
__________________________________________________________________________
| Active User | sword | shield | slaying-potion | healing-potion | lives |      
| A           | {warrior.sword}      | {warrior.shield}     | {warrior.slayingPotion}              | {warrior.healingPotion}             | {warrior.lives}     |
| B           |
| C           |
|_________________________________________________________________________
''')
    return


while True:
    print("Type number to select choice \n1. List active users \n2. Download another player's avatar \n3. Request a fight\n4. List users and their states")
    choice = input()
    clientSocket.sendto(choice.encode(), (serverName, serverPort))
    if choice == "1":
        listUsers()
    if choice == "3":
        fight()
        

#message = input('Input lowercase sentence:')
#clientSocket.sendto(message.encode(),(serverName, serverPort))
#modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
#print (modifiedMessage.decode())
clientSocket.close()


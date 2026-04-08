from dataclasses import dataclass
from socket import *
serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)

class Warrior: #warrior class
    username: str
    password: str
    lives: int = 2
    #avatar
    sword: int = -1
    shield: int = -1
    slayingPotion: int = -1
    healingPotion: int = -1
    firstTimeLogin: bool = True

warrior = Warrior() #warrior that the client is using

#login process
clientSocket.sendto("login".encode(), (serverName, serverPort))
waitingForUsername = True
while waitingForUsername: #Getting username
    print('Enter username:')
    usernameInput = input()
    clientSocket.sendto(usernameInput.encode(), (serverName, serverPort))
    loginResponse, serverAddress = clientSocket.recvfrom(2048)
    if loginResponse.decode() == "Username found!": #if username is found, break loop and move to password input
        warrior.username = usernameInput
        waitingForUsername = False
    else: #otherwise, print response and loop again for new username input
        print(loginResponse.decode())

waitingForPassword = True
while waitingForPassword: #Getting password
    print('Enter password:')
    passwordInput = input()
    warrior.password = passwordInput
    clientSocket.sendto(passwordInput.encode(), (serverName, serverPort))
    loginResponse, serverAddress = clientSocket.recvfrom(2048)
    if loginResponse.decode() == "Password correct!": #If password is correct, break loop and move on to first time login setup if necessary
        waitingForPassword = False
    else: #if password is incorrect, print response and loop again for new password input
        print(loginResponse.decode())

#Setting stats for first time login
firstTimeLoginResponse, serverAddress = clientSocket.recvfrom(2048)
if firstTimeLoginResponse.decode() == "First time login": #if first time login, enter setup loop. Otherwise, skip setup
    firstTimeLogin = True
else: #if not first time login, set warrior stats based on server data and skip setup
    firstTimeLogin = False
    statsText = firstTimeLoginResponse.decode()
    statsParts = statsText.split(",")
    warrior.sword = int(statsParts[0].split(":")[1])
    warrior.shield = int(statsParts[1].split(":")[1])
    warrior.slayingPotion = int(statsParts[2].split(":")[1])
    warrior.healingPotion = int(statsParts[3].split(":")[1])
    clientSocket.recvfrom(2048) # flush the value after putting in the values
while firstTimeLogin: #setting stats
    while True: #sword prompt + validation
        prompt, serverAddress = clientSocket.recvfrom(2048)
        prompt_text = prompt.decode()
        print(prompt_text)
        swordStrength = input()
        clientSocket.sendto(swordStrength.encode(), (serverName, serverPort))
        response, serverAddress = clientSocket.recvfrom(2048)
        response_text = response.decode()
        if response_text.startswith("Invalid sword strength"): #if invalid sword strength, print response and loop again for new input
            print(response_text)
            continue
        warrior.sword = int(swordStrength)
        # next prompt from server is shield
        shield_prompt = response_text
        break

    while True: # sword prompt + validation
        print(shield_prompt)
        shieldStrength = input()
        clientSocket.sendto(shieldStrength.encode(), (serverName, serverPort))
        response, serverAddress = clientSocket.recvfrom(2048)
        response_text = response.decode()
        if response_text.startswith("Invalid shield strength"): #if invalid shield strength, print response and loop again for new input
            print(response_text)
            continue
        warrior.shield = int(shieldStrength)
        slaying_prompt = response_text
        break

    # slaying potion prompt + validation
    while True: # slaying potion prompt + validation
        print(slaying_prompt)
        slayingPotionStrength = input()
        clientSocket.sendto(slayingPotionStrength.encode(), (serverName, serverPort))
        response, serverAddress = clientSocket.recvfrom(2048)
        response_text = response.decode()
        if response_text.startswith("Invalid slaying potion strength"): #if invalid slaying potion strength, print response and loop again for new input
            print(response_text)
            continue
        warrior.slayingPotion = int(slayingPotionStrength)
        healing_prompt = response_text
        break

    # healing potion prompt + validation
    while True: # healing potion prompt + validation
        print(healing_prompt)
        healingPotionStrength = input()
        clientSocket.sendto(healingPotionStrength.encode(), (serverName, serverPort))
        response, serverAddress = clientSocket.recvfrom(2048)
        response_text = response.decode()
        if response_text.startswith("Invalid healing potion strength"): #if invalid healing potion strength, print response and loop again for new input
            print(response_text)
            continue
        warrior.healingPotion = int(healingPotionStrength)

        # reached final verification response (total strength check)
        if response_text.startswith("Total strength is not 10"): #if total strength is not 10, print response and loop back to sword prompt for new input
            print(response_text)
            break
        if response_text.startswith("Total strength is 10"): #if total strength is 10, print response and break out of setup loop
            print(response_text)
            firstTimeLogin = False
            break

        # If we get an unexpected reply, print and exit loop.
        print(response_text)
        firstTimeLogin = False
        break

def listUsers(): #function to list active users
    printTable()
    ''' #I believe you don't need this anymore as you can just call print table of active users
    nextUser, serverAddress = clientSocket.recvfrom(2048)
    while nextUser.decode() != "No more users": #if next user message is not "No more users", print user data and loop again for next user message
        print(nextUser.decode())
        nextUser, serverAddress = clientSocket.recvfrom(2048)
    '''



def fight(): #function to request a fight with another player
    initiator = warrior.username
    clientSocket.sendto(initiator.encode(), (serverName, serverPort))
    printTable()
    print("Enter username of player you want to fight:")
    opponent = input()
    clientSocket.sendto(opponent.encode(), (serverName, serverPort))
    fightResponse, serverAddress = clientSocket.recvfrom(2048)
    fightResponseText = fightResponse.decode()
    
    if fightResponseText == "Fight request sent": #if fight request is sent, proceed with weapon and strength selection
        choosingWeapon = True
        while choosingWeapon: #weapon selection loop with validation
            print("Select weapon:\n 1. Sword\n 2. Slaying Potion")
            weaponChoice = input().strip()
            if weaponChoice not in ["1", "2"]: #if weapon choice is not 1 or 2, print error and loop again for new input
                print("Invalid choice. Please enter 1 or 2.")
            else: #valid weapon choice, break loop and proceed to strength selection
                choosingWeapon = False
        clientSocket.sendto(weaponChoice.encode(), (serverName, serverPort))
        choosingStrength = True
        while choosingStrength: #strength selection loop with validation based on weapon choice and available strength for that weapon
            print("Select strength (0-3):")
            strengthChoice = input().strip()
            if strengthChoice not in ["0", "1", "2", "3"] or int(strengthChoice) > warrior.sword if weaponChoice == "1" else int(strengthChoice) > warrior.slayingPotion: #if strength choice is not 0-3 or exceeds available strength for chosen weapon, print error and loop again for new input
                print("Invalid strength. Please enter a number between 0 and 3.")
            else: #valid strength choice, break loop and proceed to send choice to server
                choosingStrength = False
        clientSocket.sendto(strengthChoice.encode(), (serverName, serverPort))
        fightOutcome, serverAddress = clientSocket.recvfrom(2048)
        fightOutcomeText = fightOutcome.decode()
        
        if fightOutcomeText == "Tie": #if fight is a tie, no stat changes
            warrior.lives -= 1
        elif fightOutcomeText == "Win": #if fight is a win, gain a life
            warrior.lives += 1
        elif fightOutcomeText == "Lose": #if fight is a loss, lose a life
            warrior.lives -= 1
        
        print(fightOutcomeText, "You have " + str(warrior.lives) + " lives remaining.")
        newPowerMessage, serverAddress = clientSocket.recvfrom(2048)
        newPowerText = newPowerMessage.decode()
        if newPowerText.startswith("sword:"): #if new power update is for sword, update sword strength and print new strength
            warrior.sword = int(newPowerText.split(":", 1)[1])
            print("Your sword strength is now", warrior.sword)
        elif newPowerText.startswith("slaying:"): #if new power update is for slaying potion, update slaying potion strength and print new strength
            warrior.slayingPotion = int(newPowerText.split(":", 1)[1])
            print("Your slaying potion strength is now", warrior.slayingPotion)
        else: #if new power update is not recognized, just print the message
            print(newPowerText)
    else: #if fight request is not sent successfully, just print the response message
        print(fightResponseText)
    printTable()
    return

def printTable(): #function to print table of active users and their stats
    print(f'''
__________________________________________________________________________
| Active User | sword | shield | slaying-potion | healing-potion | lives |''')
    tableMessage, serverAddress = clientSocket.recvfrom(2048)
    #print("Debug: received", repr(tableMessage.decode()))
    while tableMessage.decode() != "No more users": #if table message is not "No more users", print user data and loop again for next table message
        print(tableMessage.decode())
        tableMessage, serverAddress = clientSocket.recvfrom(2048)
        #print("Debug: received", repr(tableMessage.decode()))
    print("|_________________________________________________________________________")


while True: #main menu loop
    print("Type number to select choice \n1. List active users \n2. Download another player's avatar \n3. List active fight requests \n4. Request a fight \n5. List users and their states and logout")
    choice = input()
    clientSocket.sendto(choice.encode(), (serverName, serverPort))
    if choice == "1": #if choice is "1", call listUsers function
        listUsers()
    if choice == "4": #if choice is "4", call fight function
        fight()
    if choice == "5": #if choice is "5", call printTable function
        printTable()
        break

#message = input('Input lowercase sentence:')
#clientSocket.sendto(message.encode(),(serverName, serverPort))
#modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
#print (modifiedMessage.decode())
clientSocket.close()


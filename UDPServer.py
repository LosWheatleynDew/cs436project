from socket import *
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)


class Warrior: #warrior class
    username: str = ""
    password: str = ""
    lives: int = 2
    sword: int = -1
    shield: int = -1
    slayingPotion: int = -1
    healingPotion: int = -1
    firstTimeLogin: bool = True


warrior = Warrior() #warrior that the client is using


def uploadAvatar(): #function to upload avatar image to server
    print("\nAvatar Upload")

    while True:
        print("Select an image file (PNG or JPG only):")
        filepath = input("Enter the path to your avatar image: ").strip().strip('"')

        if not os.path.isfile(filepath):
            print("File not found. Please try again.")
            continue

        lowerPath = filepath.lower()
        if not (lowerPath.endswith('.png') or lowerPath.endswith('.jpg') or lowerPath.endswith('.jpeg')):
            print("Invalid format. Only PNG and JPG files are allowed. Please try again.")
            continue

        filesize = os.path.getsize(filepath)
        if filesize > 1000000:
            print("File is too large. Maximum size is 1 MB. Please try again.")
            continue

        break

    filepath = os.path.abspath(filepath)
    filename = os.path.basename(filepath)
    metadata = f"{filename}|{filesize}"
    clientSocket.sendto(metadata.encode(), (serverName, serverPort))

    response, _ = clientSocket.recvfrom(2048)
    responseText = response.decode()
    print(responseText)
    if responseText != "Ready to receive":
        return

    with open(filepath, 'rb') as fileHandle:
        chunk = fileHandle.read(2000)
        while chunk:
            clientSocket.sendto(chunk, (serverName, serverPort))
            chunk = fileHandle.read(2000)

    confirmation, _ = clientSocket.recvfrom(2048)
    print(confirmation.decode())


def downloadAvatar(): #function to download another player's avatar
    print("Enter the username of the player whose avatar you want to download:")
    targetUsername = input().strip()
    clientSocket.sendto(targetUsername.encode(), (serverName, serverPort))

    sizeResponse, _ = clientSocket.recvfrom(2048)
    metadataText = sizeResponse.decode().strip()

    if metadataText in ["Avatar not found", "Avatar file not found"]:
        print(metadataText)
        return

    avatarFilename, filesizeText = metadataText.split("|", 1)
    filesize = int(filesizeText)
    clientSocket.sendto("Ready".encode(), (serverName, serverPort))

    downloadDir = os.path.join(BASE_DIR, warrior.username)
    os.makedirs(downloadDir, exist_ok=True)
    filename = os.path.join(downloadDir, avatarFilename)

    receivedSize = 0
    with open(filename, 'wb') as fileHandle:
        while receivedSize < filesize:
            chunk, _ = clientSocket.recvfrom(2048)
            fileHandle.write(chunk)
            receivedSize += len(chunk)

    print(f"Avatar downloaded and saved to {filename}")


def tryHandleAvatarPrompt():
    previousTimeout = clientSocket.gettimeout()
    clientSocket.settimeout(0.5)

    try:
        for _ in range(3):
            message, _ = clientSocket.recvfrom(2048)
            messageText = message.decode().strip()

            if messageText == "Upload avatar? (y/n)":
                while True:
                    choice = input("Upload avatar? (y/n): ").strip().lower()
                    if choice in ["y", "n"]:
                        clientSocket.sendto(choice.encode(), (serverName, serverPort))
                        break
                    print("Please enter y or n.")

                followup, _ = clientSocket.recvfrom(2048)
                followupText = followup.decode().strip()
                if followupText == "Upload avatar":
                    uploadAvatar()
                    return
                print(followupText)
                return

            if messageText == "Upload avatar":
                uploadAvatar()
                return

            if "," in messageText or messageText.count(":") >= 3:
                continue

            break
    except timeout:
        pass
    finally:
        clientSocket.settimeout(previousTimeout)


def handleFirstTimeSetup():
    firstTimeLogin = True

    while firstTimeLogin:
        while True: #sword prompt + validation
            prompt, _ = clientSocket.recvfrom(2048)
            print(prompt.decode())
            swordStrength = input().strip()
            clientSocket.sendto(swordStrength.encode(), (serverName, serverPort))
            response, _ = clientSocket.recvfrom(2048)
            responseText = response.decode()
            if responseText.startswith("Invalid sword strength"):
                print(responseText)
                continue
            warrior.sword = int(swordStrength)
            shieldPrompt = responseText
            break

        while True: #shield prompt + validation
            print(shieldPrompt)
            shieldStrength = input().strip()
            clientSocket.sendto(shieldStrength.encode(), (serverName, serverPort))
            response, _ = clientSocket.recvfrom(2048)
            responseText = response.decode()
            if responseText.startswith("Invalid shield strength"):
                print(responseText)
                continue
            warrior.shield = int(shieldStrength)
            slayingPrompt = responseText
            break

        while True: #slaying potion prompt + validation
            print(slayingPrompt)
            slayingPotionStrength = input().strip()
            clientSocket.sendto(slayingPotionStrength.encode(), (serverName, serverPort))
            response, _ = clientSocket.recvfrom(2048)
            responseText = response.decode()
            if responseText.startswith("Invalid slaying potion strength"):
                print(responseText)
                continue
            warrior.slayingPotion = int(slayingPotionStrength)
            healingPrompt = responseText
            break

        while True: #healing potion prompt + validation
            print(healingPrompt)
            healingPotionStrength = input().strip()
            clientSocket.sendto(healingPotionStrength.encode(), (serverName, serverPort))
            response, _ = clientSocket.recvfrom(2048)
            responseText = response.decode()
            if responseText.startswith("Invalid healing potion strength"):
                print(responseText)
                continue

            warrior.healingPotion = int(healingPotionStrength)

            if responseText.startswith("Total strength is not 10"):
                print(responseText)
                break

            if responseText.startswith("Total strength is 10"):
                print(responseText)
                firstTimeLogin = False
                break

            print(responseText)
            firstTimeLogin = False
            break

    return


def handleExistingStats(firstMessageText):
    statsParts = firstMessageText.split(",")
    warrior.lives = int(statsParts[0].split(":")[1])
    warrior.sword = int(statsParts[1].split(":")[1])
    warrior.shield = int(statsParts[2].split(":")[1])
    warrior.slayingPotion = int(statsParts[3].split(":")[1])
    warrior.healingPotion = int(statsParts[4].split(":")[1])
    tryHandleAvatarPrompt()


def listUsers(): #function to list active users
    printTable()


def fight(): #function to request a fight with another player
    initiator = warrior.username
    clientSocket.sendto(initiator.encode(), (serverName, serverPort))
    printTable()

    print("Enter username of player you want to fight:")
    opponent = input().strip()
    clientSocket.sendto(opponent.encode(), (serverName, serverPort))

    fightResponse, _ = clientSocket.recvfrom(2048)
    fightResponseText = fightResponse.decode()

    if fightResponseText != "Fight request sent":
        print(fightResponseText)
        printTable()
        return

    while True:
        print("Select weapon:\n 1. Sword\n 2. Slaying Potion")
        weaponChoice = input().strip()
        if weaponChoice in ["1", "2"]:
            break
        print("Invalid choice. Please enter 1 or 2.")

    clientSocket.sendto(weaponChoice.encode(), (serverName, serverPort))

    maxStrength = warrior.sword if weaponChoice == "1" else warrior.slayingPotion
    while True:
        print(f"Select strength (0-{maxStrength}):")
        strengthChoice = input().strip()
        if strengthChoice.isdigit() and 0 <= int(strengthChoice) <= maxStrength:
            break
        print("Invalid strength. Please enter a valid number for your chosen weapon.")

    clientSocket.sendto(strengthChoice.encode(), (serverName, serverPort))

    fightOutcome, _ = clientSocket.recvfrom(2048)
    fightOutcomeText = fightOutcome.decode()

    if fightOutcomeText == "Tie":
        warrior.lives -= 1
    elif fightOutcomeText == "Win":
        warrior.lives += 1
    elif fightOutcomeText == "Lose":
        warrior.lives -= 1

    print(fightOutcomeText, "You have " + str(warrior.lives) + " lives remaining.")

    newPowerMessage, _ = clientSocket.recvfrom(2048)
    newPowerText = newPowerMessage.decode()
    if newPowerText.startswith("sword:"):
        warrior.sword = int(newPowerText.split(":", 1)[1])
        print("Your sword strength is now", warrior.sword)
    elif newPowerText.startswith("slaying:"):
        warrior.slayingPotion = int(newPowerText.split(":", 1)[1])
        print("Your slaying potion strength is now", warrior.slayingPotion)
    else:
        print(newPowerText)

    printTable()


def printTable(): #function to print table of active users and their stats
    print(
        """
__________________________________________________________________________
| Active User | sword | shield | slaying-potion | healing-potion | lives |"""
    )
    tableMessage, _ = clientSocket.recvfrom(2048)
    while tableMessage.decode() != "No more users":
        print(tableMessage.decode())
        tableMessage, _ = clientSocket.recvfrom(2048)
    print("|_________________________________________________________________________")


def printFightRequests(): #function to print active fight requests
    print("Active fight requests:")
    fightRequestsMessage, _ = clientSocket.recvfrom(2048)
    while fightRequestsMessage.decode() != "No more fight requests":
        print(fightRequestsMessage.decode())
        fightRequestsMessage, _ = clientSocket.recvfrom(2048)


#login process
clientSocket.sendto("login".encode(), (serverName, serverPort))

waitingForUsername = True
while waitingForUsername:
    print('Enter username:')
    usernameInput = input().strip()
    clientSocket.sendto(usernameInput.encode(), (serverName, serverPort))
    loginResponse, _ = clientSocket.recvfrom(2048)
    if loginResponse.decode() == "Username found!":
        warrior.username = usernameInput
        waitingForUsername = False
    else:
        print(loginResponse.decode())
        retryPrompt, _ = clientSocket.recvfrom(2048)
        while True:
            retryChoice = input(f"{retryPrompt.decode()} ").strip().lower()
            if retryChoice in ["y", "n"]:
                break
            print("Please enter y or n.")
        clientSocket.sendto(retryChoice.encode(), (serverName, serverPort))
        if retryChoice == "n":
            cancelMessage, _ = clientSocket.recvfrom(2048)
            print(cancelMessage.decode())
            clientSocket.close()
            raise SystemExit

waitingForPassword = True
while waitingForPassword:
    print('Enter password:')
    passwordInput = input().strip()
    warrior.password = passwordInput
    clientSocket.sendto(passwordInput.encode(), (serverName, serverPort))
    loginResponse, _ = clientSocket.recvfrom(2048)
    if loginResponse.decode() == "Password correct!":
        waitingForPassword = False
    else:
        print(loginResponse.decode())
        retryPrompt, _ = clientSocket.recvfrom(2048)
        while True:
            retryChoice = input(f"{retryPrompt.decode()} ").strip().lower()
            if retryChoice in ["y", "n"]:
                break
            print("Please enter y or n.")
        clientSocket.sendto(retryChoice.encode(), (serverName, serverPort))
        if retryChoice == "n":
            cancelMessage, _ = clientSocket.recvfrom(2048)
            print(cancelMessage.decode())
            clientSocket.close()
            raise SystemExit

loginStateResponse, _ = clientSocket.recvfrom(2048)
loginStateText = loginStateResponse.decode()

if loginStateText == "First time login":
    tryHandleAvatarPrompt()
    handleFirstTimeSetup()
else:
    handleExistingStats(loginStateText)

while True: #main menu loop
    if(warrior.lives <= 0):
        print("You have no lives remaining. Logging out.")
        break
    print("Type number to select choice \n1. List active users \n2. Download another player's avatar \n3. List active fight requests \n4. Request a fight \n5. List users and their states and logout")
    choice = input().strip()
    clientSocket.sendto(choice.encode(), (serverName, serverPort))

    if choice == "1":
        listUsers()
    elif choice == "2":
        downloadAvatar()
    elif choice == "3":
        printFightRequests()
    elif choice == "4":
        fight()
    elif choice == "5":
        printTable()
        break
    else:
        print("Invalid choice.")

clientSocket.close()

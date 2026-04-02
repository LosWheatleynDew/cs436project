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
        # next prompt from server is shield
        sheild_prompt = response_text
        break

    # sheild prompt + validation
    while True:
        print(sheild_prompt)
        sheildStrength = input()
        clientSocket.sendto(sheildStrength.encode(), (serverName, serverPort))
        response, serverAddress = clientSocket.recvfrom(2048)
        response_text = response.decode()
        if response_text.startswith("Invalid sheild strength"):
            print(response_text)
            continue
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

#message = input('Input lowercase sentence:')
#clientSocket.sendto(message.encode(),(serverName, serverPort))
#modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
#print (modifiedMessage.decode())
clientSocket.close()

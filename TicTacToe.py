import random
import math
import os
import time
import socket
#from network import Network

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

game_list = [1,2,3,4,5,6,7,8,9]

location = [ [1,2,3] , [4,5,6] , [7,8,9] ]

def display_board():
    cls()  ##############################################################################
    print("\r\n")

    for row in range(3):
        print("+---+---+---+")
        line = ""
        for column in range(3):
            line += "| " + str(location[row][column]) + " " 
        line += "|"
        print(line)       
    print("+---+---+---+")

def check_score():
    # Checking columns
    if location[0][0] == location [0][1] == location[0][2]:
        game = False 
        return (location[0][0] + " wins ! TaDaaa !") 
    if location[1][0] == location [1][1] == location[1][2]:
        game = False 
        return (location[1][0] + " wins ! TaDaaa !") 
        
    if location[2][0] == location [2][1] == location[2][2]:
        game = False 
        return (location[2][0] + " wins ! TaDaaa !") 
        
    # Checking rows
    if location[0][0] == location [1][0] == location[2][0]:
        game = False 
        return (location[0][0] + " wins ! TaDaaa !") 
        
    if location[0][1] == location [1][1] == location[2][1]:
        game = False 
        return (location[0][1] + " wins ! TaDaaa !") 
        
    if location[0][2] == location [1][2] == location[2][2]:
        game = False 
        return (location[0][2] + " wins ! TaDaaa !") 
        
    # Checking middle cross
    if (location[0][0] == location [1][1] == location[2][2]) or location[0][2] == location [1][1] == location[2][0]:
        game = False 
        return (location[1][1] + " wins ! TaDaaa !")   
    
    return True


#Initial Setup

user_choice = ""
user = True
game = True
multiplayer = False
mark = ["o", "X"]

HOST = '192.168.1.20'
PORT = 5555

cls()

while not (user_choice.lower() == "x" or user_choice.lower() == "s" or user_choice.lower() == "c"):
        
    user_choice = input("\nX for singleplayer mode, \nS / C for Server Side or Client Side multiplayer mode.\nYour choice -> ")
    if user_choice.lower() == "s":  # server side
        multiplayer = True
        
        print("Awaiting connection from a client...")
        
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.bind((HOST, PORT))

        connection.listen(1)

        server, address = connection.accept()
        print(f'Connected with{str(address)}')

        #while True:

        #    message = communication_socket.recv(1024).decode('utf-8')
        #    print(f"Message from client is {message}")
        #    communication_socket.send(f"Hello from the server !".encode('utf-8'))


    if user_choice.lower() == "c":  # client side
        multiplayer = True
        user = False


        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.connect((HOST, PORT))

        #socket.send("Hello from the client ! ".encode('utf-8'))
        #print(socket.recv(1024).decode('utf-8'))
        

while game:    
    display_board()

    while user and game:
        #making sure user's input is valid
        while user_choice not in game_list:


            user_choice = input(f"Select field for {mark[len(game_list)%2]}\n")
            try:
                user_choice = int(user_choice)
            except ValueError:
                print("Geez - that is not even a single digit... Tst, tst... ")
            
        
        location[math.floor((user_choice-1)/3)][(user_choice-1)%3] = mark[len(game_list)%2]
        game_list.remove(user_choice)
        if multiplayer:
            server.send(str(user_choice).encode('utf-8'))

        user = False

    while not user and multiplayer:
        display_board()

        print("Awaiting oponent's move...")
        
        #print(server.recv(1024).decode('utf-8'))
        user_choice = int(server.recv(1024).decode('utf-8'))
        location[math.floor((user_choice-1)/3)][(user_choice-1)%3] =  mark[len(game_list)%2]
        game_list.remove(user_choice)
        user = True

    if len(game_list) == 0:
        game = False
        print("Looks like it is a draw !")

    while not user and game and not multiplayer:
        print("Awaiting oponent's move...")
        time.sleep(random.randint(1,30)/10)
        user_choice = random.choice(game_list) 
        if (user_choice in game_list):
            location[math.floor((user_choice-1)/3)][(user_choice-1)%3] = "o"
            game_list.remove(user_choice)
            user = True

    if not (check_score() == True):
        display_board()
        print(check_score())
        game = False
   
if multiplayer:
    client.close()
    print(f"Connection with {address} ended !")

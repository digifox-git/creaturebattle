import time
import sys
import json
import random
import os

def typewrite(text):
    
    punctuationArray = [".", "!", "?", ",", ":", ";"] # List of punctuation that will pause the text
    
    for char in text: # Write the line character-by-character until done.
        sys.stdout.write(char)
        sys.stdout.flush()
        if (char in punctuationArray):
            time.sleep(0.25)
        else:
            time.sleep(0.025)
    print() 
    
moveDirectory = {
    0: {
        "name": "Scratch",
        "target": 0,
        "power": 10, 
        "accuracy": 90,
        "effect": 0,
        "charge": 0
    },
    1: {
        "name": "Chomp",
        "target": 0,
        "power": 30, 
        "accuracy": 80,
        "effect": 1,
        "charge": 10
    },
    2: {
        "name": "Energize",
        "target": 1,
        "power": 0, 
        "accuracy": 100,
        "effect": 2,
        "charge": 5
    },
    3: {
        "name": "Mind Matrix",
        "target": 0,
        "power": 75, 
        "accuracy": 85,
        "effect": 3,
        "charge": 25
    },
    4: {
        "name": "Gymnastic Punch",
        "target": 0,
        "power": 60, 
        "accuracy": 65,
        "effect": 4,
        "charge": 12
    },
    5: {
        "name": "Backhand",
        "target": 0,
        "power": 30, 
        "accuracy": 85,
        "effect": 4,
        "charge": 5
    },
    6: {
        "name": "Ritual",
        "target": 1,
        "power": 0, 
        "accuracy": 100,
        "effect": 2,
        "charge": 8
    },
    7: {
        "name": "Power Blast",
        "target": 0,
        "power": 80, 
        "accuracy": 80,
        "effect": 0,
        "charge": 20
    },
}

turnOrder = "none"

playerStats = {
    "health": 80,
    "attack": 1.0,
    "defense": 1.2,
    "moves": [0, 1, 5, 7],
    "charge": 0,
    "gain": 4
}

enemyStats = {
    "health": 80,
    "attack": 1.1,
    "defense": 0.9,
    "moves": [0, 6, 3, 4],
    "charge": 0,
    "gain": 4
}

playerHealth = 80
playerMoves = [0, 1, 5, 7]
enemyHealth = 80
enemyMoves = [0, 6, 3, 4]

def refresh():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"YOU: {playerStats['health']}hp.\nENEMY: {enemyStats['health']}hp.\n")

def end_battle(outcome):

    if (outcome == "win"):
        typewrite("The enemy creature has been mortally wounded...")
        typewrite("You win!")
    elif (outcome == "lose"):
        typewrite("Your creature has been mortally wounded...")
        typewrite("You lose!")  

def effect(id, target):

    targetReference = "none"

    if (target == 0):
        targetReference = "The enemy"
    elif (target == 1):
        targetReference = "Your creature"


    if (id == 0):
        pass
    elif (id == 1):
        typewrite(f"{targetReference} creature became mangled!")
    elif (id == 2):
        typewrite(f"{targetReference}'s Charge gain increased!")
    elif (id == 3):
        typewrite(f"{targetReference} is bewildered!")
    elif (id == 4):
        typewrite(f"{targetReference} became dazed!")

def use_move(id):
    global playerHealth
    global enemyHealth

    refresh()

    damageDealt = round(random.randint(moveDirectory[id]['power'] - 10, moveDirectory[id]['power'] + 5) * playerStats['attack']) # Calculate damage with some variation
    accuracyCheck = random.randint(1, 100)

    typewrite(f"Your creature used {moveDirectory[id]['name']}.")

    if (accuracyCheck > moveDirectory[id]['accuracy']): # If move misses
        if (moveDirectory[id]['target'] == 0): # If target is opponent
            typewrite(f"...But it missed!\n")
        elif (moveDirectory[id]['target'] == 1): # If target is self
            typewrite(f"...But it failed!\n")
    elif (accuracyCheck < moveDirectory[id]['accuracy']): # If attack hits
        if (moveDirectory[id]['power'] > 0): # If attack does damage
            if (moveDirectory[id]['target'] == 0): # If target is opponent
                enemyStats['health'] -= damageDealt
                typewrite(f"The enemy creature took {damageDealt}hp of damage. Reduced hp to {enemyStats['health']}!")
            elif (moveDirectory[id]['target'] == 1): # If target is self
                playerStats['health'] -= damageDealt
                typewrite(f"Your creature took {damageDealt}hp of damage. Reduced hp to {playerStats['health']}!")
        effect(moveDirectory[id]['effect'], moveDirectory[id]['target']) # Apply effect to target (0 == no effect)

def player_turn():
    global playerHealth
    global enemyHealth
    
    typewrite(f"Select a move number:")
    for index, move in enumerate(playerMoves):
        print(f"{index}. {moveDirectory[playerMoves[index]]['name']}")
        time.sleep(0.2)
    moveChoicer = input("> ")
    moveInteger = int(moveChoicer)
    selectedMoveID = playerMoves[moveInteger]

    use_move(selectedMoveID)
    
    input("\nPress any key to continue.")
    next_turn()

def enemy_turn():
    global playerHealth
    global enemyHealth
    
    selectedMove = random.randint(0, 3)
    typewrite(f"The enemy creature used {moveDirectory[enemyMoves[selectedMove]]['name']}.")
    damageDealt = round(random.randint(moveDirectory[enemyMoves[selectedMove]]['power'] - 5, moveDirectory[enemyMoves[selectedMove]]['power'] + 5) * enemyStats['attack'])
    playerStats["health"] -= damageDealt
    
    time.sleep(0.5)
    typewrite(f"Your creature took {damageDealt}hp of damage. Reduced hp to {playerStats["health"]}!\n")
    effect(moveDirectory[enemyMoves[selectedMove]]['effect'], moveDirectory[enemyMoves[selectedMove]]['target']) # Apply effect to target (0 == no effect)

    
    input("Press any key to continue.")
    next_turn()
    

def next_turn():
    global playerHealth
    global enemyHealth
    global turnOrder
    
    refresh()
    
    if (playerStats["health"] <= 0):
        end_battle("lose")
    elif (enemyStats["health"] <= 0):
        end_battle("win")
    elif (turnOrder == "player"):
        turnOrder = "enemy"
        enemy_turn()
    elif (turnOrder == "enemy"):
        turnOrder = "player"
        player_turn()
    elif (turnOrder == "none"):
        turnOrder = "player"
        player_turn()  

def initiate_battle():
    refresh()
    typewrite("An enemy approaches from the shadows, prepare for battle!\n")

    input("Press any key to continue.")
    next_turn()
    
initiate_battle()



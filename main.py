import time
import sys
import json
import random
import os
import rich
from rich import print
import math
    
moveDirectory = { # List of all moves. Power is the median amount of damage, accuracy is move hit probability out of 100, effect is optional, 0 is no effect. charge is required charge to use attack. 
    0: {
        "name": "Scratch",
        "power": 10, 
        "accuracy": 90,
        "effect": 4,
        "charge": 0
    },
    1: {
        "name": "Chomp",
        "power": 30, 
        "accuracy": 80,
        "effect": 1,
        "charge": 10
    },
    2: {
        "name": "Energize",
        "power": 0, 
        "accuracy": 100,
        "effect": 2,
        "charge": 5
    },
    3: {
        "name": "Mind Matrix",
        "power": 75, 
        "accuracy": 85,
        "effect": 3,
        "charge": 25
    },
    4: {
        "name": "Gymnastic Punch",
        "power": 60, 
        "accuracy": 65,
        "effect": 4,
        "charge": 12
    },
    5: {
        "name": "Backhand",
        "power": 30, 
        "accuracy": 85,
        "effect": 4,
        "charge": 5
    },
    6: {
        "name": "Ritual",
        "power": 0, 
        "accuracy": 100,
        "effect": 2,
        "charge": 8
    },
    7: {
        "name": "Power Blast",
        "power": 80, 
        "accuracy": 80,
        "effect": 0,
        "charge": 20
    },
}

playerStats = { # Used for player calculations and move selection.
    "name": "Player",
    "creatureName": "Creature",
    "health": 80,
    "attack": 1.0,
    "defense": 1.2,
    "moves": [0, 1, 5, 7],
    "charge": 0,
    "chargeGain": 2
}

enemyStats = { # Used for player calculations and move selection.
    "name": "John Mark",
    "creatureName": "Zinky",
    "health": 80,
    "attack": 1.1,
    "defense": 0.9,
    "moves": [0, 6, 3, 4],
    "charge": 0,
    "chargeGain": 2
}

turnOrder = "" # Turn order is set in next_turn().

def clear(): # Wipes the console
    os.system('cls' if os.name == 'nt' else 'clear')
    
def refresh(): # Wipes the console and displays battle stats.
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"[{playerStats['creatureName']} (You): [red]{playerStats['health']}♥[/] [yellow]{playerStats['charge']}⚡︎+{playerStats['chargeGain']}[/]] [{enemyStats['creatureName']}: [red]{enemyStats['health']}♥[/] [yellow]{enemyStats['charge']}⚡︎+{enemyStats['chargeGain']}[/]]\n")

def wait_for_input(): # Pauses the game until the player presses enter.
    input("\n[Enter]")

def typewrite(text):
    punctuationList = [".", "!", "?", ",", ":", ";"] # List of punctuation that will pause the text
    
    for char in text: # Write the line character-by-character until done.
        sys.stdout.write(char)
        sys.stdout.flush()
        if (char in punctuationList):
            time.sleep(0.25)
        else:
            time.sleep(0.03)
    print() 
    
def setup(): # Introduction, gathers player name and player creature name
    clear()
    
    typewrite("Your name:")
    playerName = input("> ")
    
    playerStats['name'] = playerName
    clear()
    
    typewrite(f"Your creature's name:")
    playerCreatureName = input("> ")
    
    playerStats['creatureName'] = playerCreatureName
    clear()

    initiate_battle()

def initiate_battle(): # Flavor text and sets battle participants.
    clear()
    
    time.sleep(0.5)
    typewrite(f"An enemy approaches from the shadows.\n{enemyStats['name']} has challenged you!")

    wait_for_input()
    next_turn()

def end_battle(outcome):

    if (outcome == "win"):
        typewrite(f"{enemyStats['creatureName']} has been mortally wounded...")
        typewrite("You win!")
    elif (outcome == "lose"):
        typewrite(f"{playerStats['creatureName']} has been mortally wounded...")
        typewrite("You lose!")  

def effect(id, target):
    
    targetReference = "The creature"
    effectReciever = {}

    if (target == 0):
        targetReference = playerStats['creatureName']
        effectReciever = playerStats 
    elif (target == 1):
        targetReference = enemyStats['creatureName']
        effectReciever = enemyStats


    if (id == 0): # No effect
        pass
    elif (id == 1): # Mangled effect, drops attack by 0.1
        effectReciever['attack'] -= 0.1
        typewrite(f"{targetReference} became mangled, attack dropped to {effectReciever['attack']}!")
    elif (id == 2): # Energized effect, increases charge gain by 1
        effectReciever['chargeGain'] += 1
        typewrite(f"{targetReference} feels energized, charge gain increased to {effectReciever['chargeGain']}!")
    elif (id == 3): # Bewildered effect, drops defense by 0.2
        effectReciever['defense'] -= 0.2
        typewrite(f"{targetReference} is bewildered, defense dropped harshly to {effectReciever['defense']}!")
    elif (id == 4): # Dazed effect, divides current charge by 1.2
        effectReciever['charge'] = math.floor(effectReciever['charge'] / 1.2)
        typewrite(f"{targetReference} became dazed, charge reduced to {effectReciever['charge']}!")
    elif (id == 5): # Emboldened effect, raises attack by 0.3, drops defense by 0.2
        effectReciever['attack'] += 0.3
        effectReciever['defense'] -= 0.2
        typewrite(f"{targetReference} felt emboldened, attack increased greatly to {effectReciever['attack']}, defense dropped harshly to {effectReciever['defense']} !")

def use_move(id, target):
    global playerHealth
    global enemyHealth

    refresh()

    damageDealt = math.floor(random.randint(moveDirectory[id]['power'] - 5, moveDirectory[id]['power'] + 5) * playerStats['attack'] ) # Calculate damage with some variation
    accuracyCheck = random.randint(1, 100)

    typewrite(f"{playerStats['creatureName']} used {moveDirectory[id]['name']}.")

    if (playerStats['charge'] < moveDirectory[id]['charge']):
        typewrite(f"But they didn't have enough charge!")
        return
    else:
        playerStats['charge'] -= moveDirectory[id]['charge']

    if (accuracyCheck > moveDirectory[id]['accuracy']): # If move misses
        if (target == 1): # If target is opponent
            typewrite(f"...But it missed!\n")
        elif (target == 0): # If target is self
            typewrite(f"...But it failed!\n")
    elif (accuracyCheck < moveDirectory[id]['accuracy']): # If attack hits
        if (moveDirectory[id]['power'] > 0): # If attack does damage
            if (target == 1): # If target is opponent
                enemyStats['health'] -= math.floor(damageDealt/enemyStats['defense'])
                typewrite(f"{enemyStats['creatureName']} took {damageDealt} damage. Reduced ♥ to {enemyStats['health']}!")
            elif (target == 0): # If target is self
                playerStats['health'] -= math.floor(damageDealt/playerStats['defense'])
                typewrite(f"{playerStats['creatureName']} took {damageDealt} damage. Reduced ♥ to {playerStats['health']}!")
        else:
            pass
        effect(moveDirectory[id]['effect'], target) # Apply effect to target (0 == no effect)

def player_turn():
    global playerHealth
    global enemyHealth
    global participants
    
    typewrite("Select a move number:")
    for index, move in enumerate(playerStats['moves']):
        moveData = moveDirectory[playerStats['moves'][index]]
        print(f"{index}. {moveData['name']} ([red]{moveData['power']}[/]/{moveData['accuracy']}/[yellow]{moveData['charge']}[/])")
        time.sleep(0.2)
    moveChoicer = input("> ")
    moveInteger = int(moveChoicer)
    selectedMoveID = playerStats['moves'][moveInteger]
    
    typewrite("\nAnd the target:")
    print(f"0. {playerStats['creatureName']}")
    time.sleep(0.2)
    print(f"1. {enemyStats['creatureName']}")
    time.sleep(0.2)
    targetChoicer = input("> ")
    targetInteger = int(targetChoicer)

    use_move(selectedMoveID, targetInteger)
    
    wait_for_input()
    next_turn()

def enemy_turn():
    global playerHealth
    global enemyHealth
    
    selectedMove = moveDirectory[enemyStats['moves'][random.randint(0, 3)]]
    typewrite(f"{enemyStats['creatureName']} used {selectedMove['name']}.")
    damageDealt = math.floor(random.randint(selectedMove['power'] - 5, selectedMove['power'] + 5) * enemyStats['attack'])
    playerStats["health"] -= damageDealt
    
    time.sleep(0.5)
    typewrite(f"{playerStats['creatureName']} took {damageDealt} damage. Reduced ♥ to {playerStats['health']}!")
    effect(selectedMove['effect'], 0) # Apply effect to target (0 == no effect)

    
    wait_for_input()
    next_turn()
    

def next_turn():
    global playerHealth
    global enemyHealth
    global turnOrder

    playerStats['charge'] += playerStats['chargeGain']
    enemyStats['charge'] += enemyStats['chargeGain']
    
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
    elif (turnOrder == ""):
        turnOrder = "player"
        player_turn()  
    
setup()


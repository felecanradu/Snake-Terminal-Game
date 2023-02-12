# Libraries import

import os
import csv
import time
from random import randint
from pytimedinput import timedInput
from colorama import Fore, init

# Functions definition

def field_draw():
    for cell in cells:
        if cell[0] in (0, field_height - 1) or cell[1] in (0, field_width - 1):
            print(Fore.BLUE + '●', end = '')
        elif cell == apple_position: 
            print(Fore.RED + '●', end = '')
        elif cell in snake_body:
            print(Fore.GREEN + '●', end = '')
        else:
            print(' ', end = '')
        if cell[1] == field_width - 1:
            print('')

def random_apple_position():
    applerow = randint(1, field_height - 2)
    applecol = randint(1, field_width - 2)
    while (applerow, applecol) in snake_body:
        applerow = randint(1, field_height - 2)
        applecol = randint(1, field_width - 2)
    return (applerow, applecol)

def update_snake():
    global ate_apple
    new_head = snake_body[0][0] + direction[0], snake_body[0][1] + direction[1]
    snake_body.insert(0, new_head)
    if not ate_apple:
        snake_body.pop(-1)
    ate_apple = False

def eats_apple():
    global ate_apple, apple_position, score
    if apple_position == snake_body[0]:
        apple_position = random_apple_position()
        ate_apple = True
        score += 1

def check_if_database_exists():
    if not os.path.exists(database_path):
        with open(database_path, "w", newline='') as database:
            fieldnames = ['username', 'highest_score']
            db = csv.DictWriter(database, fieldnames=fieldnames)
            db.writeheader()


def get_highest_score(username):
    global first_use
    with open(database_path, newline='') as database:
        db = csv.DictReader(database)
        for row in db:
            if row['username'] == username:
                first_use = False
                return int(row['highest_score'])
    return 0

def update_database(username, score):
    if first_use:
        with open(database_path, 'a', newline='') as database:
            fieldnames = ['username', 'highest_score']
            db = csv.DictWriter(database, fieldnames=fieldnames)
            db.writerow({'username': username, 'highest_score': score})
    else:
        with open(database_path, newline='') as database:
            db = csv.DictReader(database)
            new_db = []
            for row in db:
                if row['username'] == username:
                    row['highest_score'] = score
                new_db.append(row)
        with open(database_path, "w", newline='') as database:
            fieldnames = ['username', 'highest_score']
            db = csv.DictWriter(database, fieldnames=fieldnames)
            db.writeheader()
            for row in new_db:
                db.writerow(row)

init(autoreset = True)

# Setup

field_height = 16
field_width = 32
cells = [(row, col) for row in range(field_height) for col in range(field_width)]
snake_body = [(field_height // 2, field_width // 2), (field_height // 2, field_width // 2 - 1), (field_height // 2, field_width // 2 - 2)]
directions = {'w': (-1, 0), 's': (1, 0), 'a': (0, -1), 'd': (0, 1)}
direction = directions['d']
database_path = "./snake.csv"


# Running the game

apple_position = random_apple_position()
ate_apple = False
first_use = True
score = 0

check_if_database_exists()

os.system('cls')
print("\nWelcome to the classical snake terminal game 😀\n")
username = input('Username: ')
highest_score = get_highest_score(username)
if first_use:
    print('\nWelcome, ' + username + '!\n')
else:
    print('\nWelcome back, ' + username + '!\n')
print('The game will begin in 2 seconds. Have fun!\n')
time.sleep(2)

while True:
    os.system('cls')
    print("           Commands:\n")
    print("              UP\n")
    print("              w\n")
    print(" LEFT  a      s      d  RIGHT\n")
    print("             DOWN\n")
    print(" QUIT  q\n")
    print(" PAUSE x\n")
    print('  Highest score --> ' + str(highest_score) + ' points\n')
    print('     Score --> ' + str(score) + ' points\n')
    field_draw()
    command,_ = timedInput('', timeout=0.2)
    if command in directions.keys():
        direction = directions.get(command)
    elif command == "q":
        print('\n          Game exited!\n')
        break
    elif command == "x":
        resume = input("Press ENTER to resume...")
    update_snake()
    eats_apple()
    if snake_body[0][0] in (0, field_height - 1) or \
       snake_body[0][1] in (0, field_width - 1) or \
       snake_body[0] in snake_body[1:]:
        print('\n           Game Over! \n')
        break

if score > highest_score:
    print('   New highscore --> ' + str(score) + ' points!\n')
    update_database(username, score)
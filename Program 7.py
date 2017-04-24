########################################################################
#
# CS 101
# Program 7
# Christopher Hoffman
# clhd5d@mail.umkc.edu
#
# Problem:  Create a battle pet simulator, getting the information from a CSV file, and creating a creature class for
#           both the user and the computer to battle.
#
#
#
# Functions:
# 1. Play Again
#   a. Ask the user if they would like to play again.
# 2. CSV Reader
#   a. Read the CSV file and import it as a list of lists.
# 3. User Pykemon
#   a. Randomly selects 3 pykemon for the user to use.
#   b. Displays options to allow the user to select which pykemon to send into battle.
# 4. Computer Pykemon
#   a. Randomly selects 3 pykemon for the computer to use.
#   b. Randomly selects the pykemon to be sent into battle.
# 5. Battle Menu
#   a. Displays damage values for both the user and computer pykemon.
#   b. Removes any pykemon that fall in battle.
# 6. Pykemon Class
#   a. Create creature using Name, HP, Attack Value(AV), Attack Type, and Weakeness.
#   b. Reduces HP based on damage taken.
#
#
# Program:
# 1. Open CSV File
# 2. Use CSV Reader.
# 3. Close CSV File.
# 4. Use User Pykemon.
# 5. Use Computer Pykemon.
# 6. Use Pykemon Class on User/Computer Pykemon.
# 7. Use Battle Menu to display damage.
# 8. Repeat 4-7 until either User or Computer have no available Pykemon.
# 9. Display Winner/User.
# 10. Use Play Again.
#
########################################################################
import csv
import random
import copy
import time

# Function asking the user if they want to play again. Only allows specific answers, otherwise keeps asking.
def play_again():
    while True:
        print("Pykemon Creature Battle!")
        print("")
        print("")
        print("")
        print("Please select from the following responses.")
        print("1. Play against AI.")
        print("Q. Quit Game")
        result = input("==>")

        if result == "1":
            print("")
            return True
        elif result in ["q", "Q"]:
            return False
        else:
            print('You must select (1 or Q).')


# Converts information on CSV into a list of a list of pykemon.
def csv_reader(file):
    # Converts information from csv into a list
    user_file = csv.reader(file)
    file_information = []
    for line in user_file:
        row = [line[0], line[1], line[2], line[3], line[4]]
        file_information.append(row)
    return file_information


# Gets a list of the pykemon available to the user.
def user_pykemon(pykemon_list):
    user_list = []
    index = len(pykemon_list) - 1
    while len(user_list) < 3:
        random_number = random.randint(0, index)
        pykemon = copy.copy(pykemon_list[random_number])  # Number will be 1-13. Must -1 to get to 0-12.
        user_list.append(pykemon)
    new_list = copy.deepcopy(user_list)
    return new_list


# Gets a list of pykemon available to the computer
def computer_pykemon(pykemon_list):
    computer_list = []
    index = len(pykemon_list) - 1
    while len(computer_list) < 3:
        random_number = random.randint(0, index)
        pykemon = copy.copy(pykemon_list[random_number]) # Number will be 1-13. Must -1 to get to 0-12.
        computer_list.append(pykemon)
    new_list = copy.deepcopy(computer_list)
    return new_list

# Class creating the Pykemon and giving it the ability to attack.
class Pykemon(object):
    """Creates a Pykemon when given the correct information"""

    def __init__(self, name: str, hp: int, av: int, dmgtype: str, weakness: str):
        self.name = name
        self.hp = int(hp)
        self.av = int(av)
        self.dmgtype = dmgtype
        self.weakness = weakness

    def __str__(self):
        return self.name

    def attack(self, target):
        if target.weakness == self.dmgtype:
            print("{} attacks {} for {} points of damage.".format(self.name, target.name, self.av * 2))
            target.hp -= self.av * 2

        else:
            print("{} attacks {} for {} points of damage.".format(self.name, target.name, self.av))
            target.hp -= self.av

# Sends the information to the Pykemon Class
def pykemon_grabber(pykemon_list):
    return Pykemon(pykemon_list[0], pykemon_list[1], pykemon_list[2], pykemon_list[3], pykemon_list[4])

# Main battle
def battle(userpykemon, computerpykemon, user_list, computer_list, userchoice, computerchoice):
# Calculates who gets to go first.
    choice = random.randint(1, 2)
    if choice == 1:
        first = userpykemon
    else:
        first = computerpykemon

    if first == userpykemon:
        while userpykemon.hp > 0 and computerpykemon.hp > 0:
            userpykemon.attack(computerpykemon)
            print("(ai)", computerpykemon.name, " has ", computerpykemon.hp, " remaining.")
            if computerpykemon.hp > 0:
                computerpykemon.attack(userpykemon)
                print("(player)", userpykemon.name, " has ", userpykemon.hp, " remaining.")
    elif first == computerpykemon:
        while computerpykemon.hp > 0 and userpykemon.hp > 0:
            computerpykemon.attack(userpykemon)
            print("(player)", userpykemon.name, " has ", userpykemon.hp, " remaining.")
            if userpykemon.hp > 0:
                userpykemon.attack(computerpykemon)
                print("(ai)", computerpykemon.name, " has ", computerpykemon.hp, " remaining.")

# Returns the newly updated lists, with health values modified, and "fainted" pykemon removed.
    if userpykemon.hp > 0:
        user_list[userchoice - 1][1] = userpykemon.hp
        computer_list.remove(computer_list[computerchoice - 1])
        return "USER", user_list, computer_list

    if computerpykemon.hp > 0:
        computer_list[computerchoice - 1][1] = computerpykemon.hp
        user_list.remove(user_list[userchoice - 1])
        return "COMPUTER", user_list, computer_list

# Gives the user the option to pick, while displaying health.
def user_choice(userpykemon):
    if len(userpykemon) == 1:
        print("")
        print("")
        print("You only have one available Pykemon.")
        print("")
        print("")
        return 1
    while True:
        try:
            count = 1
            print("Please pick from the following Pykemon.")
            for pykemon_choices in userpykemon:
                print(count, "-", pykemon_choices[0], "[",pykemon_choices[1],"hp ]")
                count += 1
            choice = int(input("==>"))
            if len(userpykemon) >= choice > 0:
                print("")
                print("")
                return choice
        except: Exception
        print("You must pick a valid number.")


# MAIN
def main():
    file = open("pykemonindex.csv")
    csv_info = csv_reader(file)
    file.close()
    user_list = user_pykemon(csv_info)
    computer_list = computer_pykemon(csv_info)


    while len(user_list) > 0 and len(computer_list) > 0:

        userchoice = user_choice(user_list)
        userpykemon = pykemon_grabber(user_list[userchoice - 1])

        computerchoice = int(random.randint(0, len(computer_list) - 1))
        computerpykemon = pykemon_grabber(computer_list[computerchoice - 1])

        winner, user_list, computer_list = battle(userpykemon, computerpykemon, user_list, computer_list, userchoice,
                                                  computerchoice)

        if winner == "USER":

            print("")
            print("You won that round!")
            print("")
        elif winner == "COMPUTER":
            print("")
            print("You lost that round! You have", len(user_list), " remaining Pykemon.")
            print("")

    if len(user_list) > 0:
        print("Congrats on winning!")
        print("")
    elif len(user_list) <= 0:
        print("Better luck next time!")
        print("")


run = play_again()
while run == True:
    main()
    run = play_again()
# File: DoctorDork.py
# Author: Slow
# Date: 2022-06-19

import os
import sys
import time
import random
import string
import pipx
import pipx.colors as colors
import webbrowser
import win32gui
import win32con
hwnd = win32gui.GetForegroundWindow()
win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)



# Colours
W = "\033[0m"  # white = "\033[0m"
R = "\033[31m" # Red = "\033[31m"
G = "\033[32m" # Green = "\033[32m"
O = "\033[33m" # Orange = "\033[33m"
B = "\033[34m" # Blue = "\033[34m"
Y = "\033[40m" # Yellow = "\033[40m"

    


def logo():
    print(G + '''
                                                    ####################################################
                                                    #                                                  #
                                                    #     Welcome to the Doctor contact dork tool      #
                                                    #                                                  #
                                                    #       Because looking for a Doctor sucks!        #
                                                    #                                                  #
                                                    # This will take you to most website contact forms #
                                                    #                                                  #
                                                    ####################################################
''')
    print(W)

logo()

def print_slow(str):
    for letter in str:
        sys.stdout.write(letter)
        sys.stdout.flush()
        time.sleep(0.1)


print_slow("Another Slow Production. ")
print()
print()

#Sleep timer
time.sleep(4)
#Clear screen
os.system('cls')

# Print word in Blue ascii terminal font.
print(B + '''
                  _____             _                _____                     _       __  __           _        ______                
                 |  __ \           | |              / ____|                   | |     |  \/  |         | |      |  ____|               
                 | |  | | ___   ___| |_ ___  _ __  | (___   ___  __ _ _ __ ___| |__   | \  / | __ _  __| | ___  | |__   __ _ ___ _   _ 
                 | |  | |/ _ \ / __| __/ _ \| '__|  \___ \ / _ \/ _` | '__/ __| '_ \  | |\/| |/ _` |/ _` |/ _ \ |  __| / _` / __| | | |
                 | |__| | (_) | (__| || (_) | |     ____) |  __/ (_| | | | (__| | | | | |  | | (_| | (_| |  __/ | |___| (_| \__ \ |_| |
                 |_____/ \___/ \___|\__\___/|_|    |_____/ \___|\__,_|_|  \___|_| |_| |_|  |_|\__,_|\__,_|\___| |______\__,_|___/\__, |
                                                                                                                                  __/ |
                                                                                                                                 |___/ 
''')

# Create a menu in yellow Ascii.
print("\033[1;33;40m")

city = input("What city are you looking for? ")
state = input("What state are you looking for? ")
practice = input("What type of doctor are you looking for? ")

# supress error str = input("group:"doctor") | group:"physician" | inurl:"contact" | inurl:"contact-us" + "city" + "state" + "practice"") #This is the dork.
# "group:lawyer | group:attorney | inurl:contact | inurl:contact-us + input(city) + input(state) + input(practice)"

ask = input("Would you like to open the dork in your browser? ")


def open_chrome():
    pass


if ask == "yes":
    open_chrome()
    webbrowser.open(
        f"https://www.google.com/search?q=group:doctor | group:physician | inurl:contact | inurl:contact-us + {city}+{state}+{practice}")
    print("Opening Google...")
    if ask == "no":
        print("Closing Google...")
        time.sleep(1)

# doctor + group:physician + inurl:contact + inurl:contact-us + input(city) + input(state) + input(practice)')

# Imports
import tkinter as tk
from tkinter import font
from tkinter.constants import INSERT
import requests
import time
from threading import *
import math
import keyboard

# Variables
window = tk.Tk()

randQuote = requests.get('https://api.quotable.io/random')
newQuote = randQuote.json()
wordsInQuote = newQuote["length"]

globalTime = 0
gameEnd = 0

playerInputVar = tk.StringVar()

transparent = "#00FFFFFF"

userInputText = ""

# Main window params
window.title("Type Racer")



# Functions
class Timer(Thread):
    def run(self):
        timed = 0
        for i in range(1000):
            global globalTime
            global gameEnd
            if gameEnd == 1:
                canvas.delete("timeUsed")
                return
            else:
                timed += 1
                # print(timed)
                time.sleep(1)
                canvas.delete("timeUsed")
                globalTime = timed
                canvas.create_text(375, 75, text=globalTime, font=("Poppins", 12), tags="timeUsed")
            
def close():
    global gameEnd
    gameEnd = 1
    window.destroy()
    exit()

class KeyChecker(Thread):
    def run(self):
        num = 0
        global globalTime
        global gameEnd
        for z in range(1000):
            tempUserInput = playerInputVar.get()
            quote = newQuote["content"]
            num += 1
            if keyboard.read_key() == "enter":
                if tempUserInput == quote:
                    canvas.delete("quote")
                    canvas.delete("timeUsed")
                    canvas.delete("inputBox")
                    calculate(globalTime, newQuote["length"])
                    gameEnd = 1
                else:
                    canvas.delete("quote")
                    canvas.delete("timeUsed")
                    canvas.delete("inputBox")
                    canvas.create_text(375, 225, text="You are wrong, lmao. Restart, peasant.")
                    gameEnd = 1
                return

class Game(Thread):
    def run(self):
        startButton.pack_forget()
        playerInput = tk.Entry(window, textvariable=playerInputVar)
        canvas.create_text(375, 125, text=str(newQuote["content"]), font=("Poppins", 12), width=600, tags="quote")
        canvas.create_window(375, 225, window=playerInput, width=500, tags="inputBox")
        canvas.pack()
        # print("Your quote is: " + "\n" + newQuote["content"])

        # userInput = input("")

        # if(userInput == newQuote["content"]):
        #     global gameEnd
        #     gameEnd = 1
        #     calculate(globalTime, newQuote["length"])
        # else:
        #     print("You did it wrong, lmao. Restart the program, peasant.")

def calculate(userTime, quoteLength):
    timeInMinutes = userTime / 60

    cpm = quoteLength / timeInMinutes
    wpm = cpm / 5
    wpm = math.ceil(wpm)

    canvas.create_text(375, 125, text="Your result is " + str(wpm) + " WPM", font=("Poppins", 12))

    # print("Your WPM result is: " + str(math.ceil(wpm)))

def startGame():
    game = Game()
    timer = Timer()
    keyCheck = KeyChecker()

    game.start()
    timer.start()
    keyCheck.start()

def test():
    print("1")

# Widgets
canvas = tk.Canvas(window, width=750, height=450)
startButton = tk.Button(window, text="Start", command=startGame)





# Packings
startButton.pack()


# Mainloop
window.protocol("WM_DELETE_WINDOW", close)
window.mainloop()
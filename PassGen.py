"""
v2.1
A program for generating a password based on a number of randomly
selected words from the wordlist here
https://www.ef.edu/english-resources/english-vocabulary/top-3000-words/
Based on the concept provided by xkcd here https://xkcd.com/936/
Author: Me
Date: 3Dec2019
"""

import random, time, sys, os, math
from tkinter import *
from tkinter import messagebox

#For use with pyinstaller
#Requires sys and os Libraries
def resource_path(relative_path):
# Get absolute path to resource, works for dev and for PyInstaller
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

words = [line.rstrip('\n') for line in open(resource_path("wordlist"))]

#grabs a word from wordlist randomly
def getwords(seed):
    random.seed(time.time()*seed)
    b = random.randint(1,len(words))
    return words[b]

#gets number of words to use, then passes that to password generator
def setNum():
    c = lenout.get()
    outputPassword(c)

#calculates entropy based on total entries in wordlist, then find time to crack based on guesstime (guesses per day)
def calcTime():
    guesstime = 2**55
    length = 0
    
    try: length = int(lenout.get()) + int(xtralen.get())
    except ValueError: length = int(lenout.get())
    
    pool  = 171000
    if (checknum.get() == 1): pool += 10
    if (checkpunc.get() == 1): pool += 6
    if (checkcaps.get() == 1): pool += len(words)
    
    entropy = math.log2(pool**length)
    timetocrack = math.floor(((2**entropy)/guesstime))
    
    if(timetocrack > 365):
        timetocrack /= 365
        output =  str(math.floor(timetocrack)) + " years"
    else: output = str(timetocrack) + " days"
        
    if(entropy <= 28 ): strength = "VERY WEAK"
    elif (entropy > 28 and entropy <= 35): strength = "WEAK"
    elif (entropy > 35 and entropy <= 59): strength = "FAIR"
    elif (entropy > 59 and entropy <= 127): strength = "STRONG"
    else: strength = "RIDICULOUS"
    
    return "entropy is ~" + str(math.floor(entropy)) + " bits\n Password strength is " + strength + "\nTime to crack @ 2^55 guesses/day:\n" + output

#generates passphrase using desired number of words
def outputPassword(c):
    passes = ""
    try:
        for x in range(int(c)):
            passes = passes + " " + getwords((x+1)*42)   #modifies seed each itineration, otherwise it would always pick the same word
            wordsout.set(passes)
    except ValueError: wordsout.set("enter an integer for word count")
#    messagebox.showinfo("", "hi there")
    
    challenge.set(str(len(words)) + " words in list\n" + calcTime())
    
#writes password to file, then clears output
def boom():
    output = wordsout.get()
    with open("output.txt", "w") as f:
        f.write("xkcd Password Generator:\n"+output)
    wordsout.set("xkcd Password Generator")

main = Tk()
main.title("xkcd Password Generator")
main.geometry('300x300')
buttsize = 40

wordsout = StringVar()
lenout = StringVar()
challenge = StringVar()
checknum = IntVar()
checkpunc = IntVar()
checkcaps = IntVar()
xtralen = StringVar()
butts = Frame(main).pack(side=TOP, fill=X)
wordsout.set("xkcd Password Generator")

wordso = Label(butts, textvariable = wordsout, width = buttsize, bg = "black", fg = "white").pack()
lenit = Entry(butts, width = buttsize, textvariable = lenout).pack()
lenout.set("Enter number of words to use")
makeit = Button(butts, width = buttsize, text = "Generate Password", command = lambda: setNum()).pack()
boomit = Button(butts, width = buttsize, text = "BOoOM", command = lambda: boom()).pack()
things = Label(butts, text = "\/ Additonal arguements \/", width = buttsize, bg = "black", fg = "white").pack()
C1 = Checkbutton(butts, text = "Numbers?", variable = checknum, offvalue = 0, onvalue = 1).pack()
C2 = Checkbutton(butts, text = "Punctuation?", variable = checkpunc).pack()
C3 = Checkbutton(butts, text = "Caps?", variable = checkcaps).pack()
xlength = Entry(butts, width = buttsize, textvariable = xtralen).pack()
xtralen.set("Enter # of extra character you plan on using")
chalout = Label(butts, textvariable = challenge, width = buttsize, bg = "black", fg = "white").pack()
challenge.set("approximate time to crack based on bits of entropy")

main.mainloop()

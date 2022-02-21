# Go to root/test of PyNXBot
import signal
import sys
import json
sys.path.append('../')

from rng import XORSHIFT
from nxbot import BDSPBot

config = json.load(open("../config.json"))
b = BDSPBot(config["IP"])

def signal_handler(signal, advances): #CTRL+C handler
    print("Stop request")
    b.close()

signal.signal(signal.SIGINT, signal_handler)

r = XORSHIFT(b.getSeed())
seed = r.state()
advances = 0
print("Initial Seed")
print(f"S[0]: {seed[0]:08X}\tS[1]: {seed[1]:08X}\nS[2]: {seed[2]:08X}\tS[3]: {seed[3]:08X}")
print()
print(f"Advances: {advances}\n\n")

targetAdvances = []
botFlag = input("Press A at a specific advance? (y/n) ")
if botFlag == "y" or botFlag == "Y":
    botFlag = True
    userAdvances = input("Input the target advances separated by a space: ")
    targetAdvances = [int(i) for i in userAdvances.split(' ') if i.isdigit()]
else:
    botFlag = False
print("\n")

# Variables for conversation timeline
conversationStarted = False
remainder = divmod(targetAdvances[0], 41)[1]
startConversation = [remainder] # I noticed during testing that all targets were off by 1 advance, this constant corrects that

# Identify when to begin the conversation
for conversationTarget in startConversation:
    if conversationTarget + 41 < targetAdvances[0] - 500:
        startConversation.append(conversationTarget + 41)

# Variable to handle progression of conversation
conversationProgressed = False

# Dexscrolling Variables
dexOpened = False
dexScrolled = False
trainercardOpened = False
scrolls = 0

while True:
    currSeed = b.getSeed()

    while r.state() != currSeed:
        r.next()
        advances += 1

        if r.state() == currSeed:
            print("Current Seed")
            print(f"S[0]: {currSeed[0]:08X}\tS[1]: {currSeed[1]:08X}\nS[2]: {currSeed[2]:08X}\tS[3]: {currSeed[3]:08X}")
            print()
            print(f"Advances: {advances}\n\n")

            if not dexOpened and botFlag and not conversationStarted and advances > 60 and advances <= targetAdvances[0] - 2300:
                print(f"Opening pokedex to advance...\n\n")
                b.click("X")
                b.pause(0.9)
                b.click("A")
                b.pause(1.2)
                b.click("R")
                b.pause(1.5)
                dexOpened = True

            if dexOpened and botFlag and not conversationStarted and advances > 60 and advances <= targetAdvances[0] - 2300:
                print(f"Pokedex scrolled {scrolls} times\n\n")
                scrolls += 1
                b.click("DRIGHT")
                b.pause(0.2)

            if dexOpened and botFlag and not conversationStarted and advances > 60 and advances >= targetAdvances[0] - 2300:
                print(f"Closing pokedex...\n\n")
                b.click("B")
                b.pause(0.9)
                b.click("B")
                b.pause(0.9)
                dexOpened = False
                dexScrolled = True

            if botFlag and dexScrolled and not conversationStarted:
                for conversationTarget in startConversation:
                    if advances < conversationTarget:
                        break
                    if advances == conversationTarget and advances > 30:
                        b.click("A")
                        print(f"Conversation started on advance {conversationTarget}\n\nConversation started on advance {conversationTarget}\n\nConversation started on advance {conversationTarget}\n\nConversation started on advance {conversationTarget}\n\nConversation started on advance {conversationTarget}\n\nConversation started on advance {conversationTarget}\n\n")
                        conversationStarted = True
                    if advances > conversationTarget:
                        startConversation.remove(conversationTarget)

            if dexScrolled and conversationStarted and not conversationProgressed:
                b.pause(1.45)
                b.click("A")
                b.pause(1.45)
                b.click("A")
                b.pause(1.45)
                b.click("A")
                conversationProgressed = True

            if botFlag and dexScrolled and conversationStarted and conversationProgressed:
                for currentTarget in targetAdvances:
                    if advances < currentTarget:
                        break
                    if advances == currentTarget:
                        for i in range(5):
                            b.click("A")
                            b.pause(0.2)
                        print(f"We hit {currentTarget}!\n\n")
                        b.close()
                    if advances > currentTarget:
                        targetAdvances.remove(currentTarget)

            if len(targetAdvances) == 0:
                print("Missed all potential targets, ending...")
                b.close()

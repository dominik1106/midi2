import logging
# import sys
# import time
import rtmidi
from rtmidi.midiutil import open_midiinput
import midi2

NOTES_FILENAME = "notes.txt"

notesWanted = []

#Get target notes from default.txt
try:
    with open(NOTES_FILENAME) as f:
        notesWanted = [int(x.strip()) for x in f]
except FileNotFoundError:
    print("File not found, defaulting to C4 major scale")
    notesWanted = [60, 62, 64, 65, 67, 69, 71]

def result():
    print("UNLOCKED")

midi2.midiCallback(result, notesWanted, printInput=False)
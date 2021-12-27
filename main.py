import logging
import sys
import time
import rtmidi
from rtmidi.midiutil import open_midiinput

NOTES_FILENAME = "notes.txt"


def midi2String(midinumber):
    keys = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
    pianoNumber = midinumber - 20 #0 is now the lowest Key on a 88 Keyboard
    pianoAdjusted = pianoNumber + 8 #B0 is now 12, as if the first scale would extend down to C0
    scaleNumber = pianoAdjusted // 12 #This returns the scale
    posInScale = pianoAdjusted % 12 #Position in current scale (from 0 to 11), so C is always 0, B is 11
    currentKey = keys[posInScale] + str(scaleNumber)
    return currentKey


#Configure Logger
log = logging.getLogger('main')
logging.basicConfig(level=logging.DEBUG)


notesWanted = []
notesPlayed = []

#Get target notes from default.txt
try:
    with open(NOTES_FILENAME) as f:
        notesWanted = [int(x.strip()) for x in f]
except FileNotFoundError:
    print("File not found, defaulting to C4 major scale")
    notesWanted = [60, 62, 64, 65, 67, 69, 71]


#If port was given as cmd argument
port = sys.argv[1] if len(sys.argv) > 1 else None

#If before no port was given, it will give a list of devices and ask the user to specify one
try:
    midiin, port_name = open_midiinput(port)
except (EOFError, KeyboardInterrupt):
    sys.exit()
except rtmidi._rtmidi.NoDevicesError:
    print("No device connected!")
    sys.exit()

print("Entering main loop. Press Control-C to exit")
try:
    timer = time.time()
    while True:
        msg = midiin.get_message()

        if msg:
            message, deltatime = msg
            timer += deltatime
            #print("[%s] @%0.6f %r" % (port_name, timer, message))
            if(message[0] == 144):
                notesPlayed.append(message[1])
                if(len(notesPlayed) > len(notesWanted)):
                    notesPlayed.pop(0)
                
                print(midi2String(message[1]))
                if(notesPlayed == notesWanted):
                    print("UNLOCKING!")
                    notesPlayed == []

        time.sleep(0.01)
except KeyboardInterrupt:
    print('')
finally:
    print("Exiting")
    midiin.close_port()
    del midiin
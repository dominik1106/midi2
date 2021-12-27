import logging
import sys
import time
import rtmidi
from rtmidi.midiutil import open_midiinput


def midi2String(midinumber):
    keys = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
    pianoNumber = midinumber - 20 #0 is now the lowest Key on a 88 Keyboard
    pianoAdjusted = pianoNumber + 8 #B0 is now 12, as if the first scale would extend down to C0
    scaleNumber = pianoAdjusted // 12 #This returns the scale
    posInScale = pianoAdjusted % 12 #Position in current scale (from 0 to 11), so C is always 0, B is 11
    currentKey = keys[posInScale] + str(scaleNumber)
    return currentKey


#If port was given as cmd argument
port = sys.argv[1] if len(sys.argv) > 1 else None

#If before no port was given, it will give a list of devices and ask the user to specify one


def midiCallback(callback, notesWanted, port = None, printInput = True):
    notesPlayed = []

    if(notesWanted == None or len(notesWanted) <= 0):
        return

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

                    if printInput:
                        print(midi2String(message[1]))

                    if(notesPlayed == notesWanted):
                        callback()
                        notesPlayed == []

            time.sleep(0.01)
    except KeyboardInterrupt:
        print('')
    finally:
        print("Exiting")
        midiin.close_port()
        del midiin

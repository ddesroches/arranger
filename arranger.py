#!/usr/bin/env python
# encoding: utf=8
"""
arranger.py

Given an audio file provide the means to audition each section and rearrange
the track by sections including deletes and repeats.

By Dave and Nick, 2013.

Example operation:

"Track includes sections 1..12."
> p 4 6 9
(play sections 4 6 9)

> a 2 2 5 3 4 6 7 8 9 8 8 2 12
(arrange sections; rearranged track plays)

> s output_filename
(new mp3 saved to output_filename)

"""

import subprocess
import soundcloud

from engine import Engine

usage = """
Usage: 
    python arranger.py [input_filename]

Example:
    python arranger.py songoftheyear.mp3
"""

"""class TestEngine():
    def play(self, arg):
        print "playing sections %s..."%arg
        
    def arrange(self, arg):
        print "arranging track by %s..."%arg
        
    def save(self, arg):
        print "saving track %s..."%arg
        
    def kill(self):
        print "You have stopped the playback"
        
        """

def main(input_filename):
    engine = Engine(input_filename)
    sections = engine.get_sections()
    print("Track includes sections 1..%d" % len(sections))
        
    client = soundcloud.Client(access_token = "1-58137-40361369-f78a9445cc6c563")
    
    while True:
        cmd = raw_input("> ")
        if len(cmd) == 0:
            continue

        if cmd[0].lower() == "p":
            engine.play([int(x) - 1 for x in cmd.split()[1:]])
            
        elif cmd[0].lower() == "h":
            print "a [sections] - arrange sections (e.g. a 2 2 4 5 10) "
            print "p [sections] - play sections (e.g. p 4 5 6) or current arrangement"
            print "k - kill current playback"
            print "s filename - save current arrangement (option to upload to SoundCloud)"
            print "h - help"
            print "q - quit"
            
        elif cmd[0].lower() == "k":
            engine.kill()
            
        elif cmd[0].lower() == "a":
            engine.arrange([int(x) - 1 for x in cmd.split()[1:]])
            
        elif cmd[0].lower() == "q":
            break
            
        elif cmd[0].lower() == "s":
            name = cmd[2:]
            engine.save(name)
                        
            print"Upload track to SoundCloud? (y/n)"
            yesNo = raw_input("> ")
            if yesNo.lower().startswith("y"):
                print "Name your sound:"
                title = raw_input("> ")
                track = client.post('/tracks', track = {'title': title, 'asset_data': open(name, 'rb')})
                print "Your new song is now posted at %s" % track.permalink_url                
            else:
                return

if __name__ == '__main__':
    import sys
    try:
        input_filename = sys.argv[1]
    except:
        print usage
        sys.exit(-1)
    main(input_filename)

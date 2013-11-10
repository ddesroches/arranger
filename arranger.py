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
import time
import webbrowser

import soundcloud

from engine import Engine

USAGE = """
Usage: 
    python arranger.py input_filename
"""

HELP = """  a <sections> - arrange sections (e.g. a 2 2 4 5 10)
  p [<sections>] - play sections (e.g. p 4 5 6) or current arrangement
  k - kill current playback
  s <filename> - save current arrangement (option to upload to SoundCloud)
  h - help
  q - quit"""

def main(input_filename=None):
    if input_filename:
        engine = Engine(input_filename)
        sections = engine.get_sections()
        print("track includes sections 1..%d" % len(sections))
    else:
        engine = None

    client = soundcloud.Client(access_token = "1-58194-65838022-e30bc60d1afac57")
    
    while True:
        cmd = raw_input("arranger > ")
        if len(cmd) == 0:
            continue

        if cmd[0].lower() == "p":
            if engine:
                engine.play([int(x) - 1 for x in cmd.split()[1:]])
            else:
                print "load a track with 'l <filename>'"
            
        elif cmd[0].lower() == "a":
            if engine:
                engine.arrange([int(x) - 1 for x in cmd.split()[1:]])
            else:
                print "load a track with 'l <filename>'"
            
        elif cmd[0].lower() == "s":
            if engine:
                name = cmd[2:]
                if len(name) < 1:
                    print "empty name"
                    continue

                engine.save(name)
                if not '.' in name:
                    name = name + '.mp3'

                yesNo = raw_input("Upload track to SoundCloud? (y/n) > ")
                if yesNo.lower().startswith("y"):
                    title = raw_input("Name your sound > ")
                    track = client.post('/tracks', track = {'title': title, 'asset_data': open(name, 'rb')})
                    genre = raw_input("What genre is your sound? > ")
                    tags = raw_input("Add tags. > ").split(",")
                    if track.state == "finished":
                        webbrowser.open(track.permalink_url)
                        
                    else:
                        time.sleep(1)
                        
                    id_string = "/tracks/%s"%str(track.id)
                    track = client.get(id_string)
                    client.put(track.uri, track={'genre': genre, "tag_list" : tags)
                    })
                else:
                    continue
            else:
                print "load a track with 'l <filename>'"

        elif cmd[0].lower() == "l":
            if engine:
                engine.kill()
            new_filename = cmd[1:].strip()
            engine = Engine(new_filename)
            print("track includes sections 1..%d" % len(engine.get_sections()))

        elif cmd[0].lower() == "h":
            print HELP
            
        elif cmd[0].lower() == "k":
            if engine:
                engine.kill()

        elif cmd[0].lower() == "q":
            if engine:
                engine.kill()
            break

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()

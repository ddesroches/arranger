import os
import operator
import cherrypy

from engine import Engine

HEAD = """
<doctype html>
<html>
<title>The Lone Arranger</title>
<head>
<h1>The Lone Arranger</h1>
<script>
function file_chosen()
{
    document.getElementById("filename").click();
}
</script>
</head>
<body>
BODY_HERE
</body>
<footer>
<h5>by David & Nick DesRoches for <a href="http://boston.musichackday.org/2013">Music Hack Day Boston 2013</a></h5>
<a href = "http://the.echonest.com"><p><img src="/images/echo_nest_logo.gif" alt="Powered by The Echo Nest"></p></a>
</footer>
</html>
"""

class Arranger(object):
    def __init__(self):
        self.input_filename = None
        self.section_list = None
        self.engine = None
        self.sections = None  # current list of audio sections for display

    def index(self):
        return HEAD.replace("BODY_HERE", open("body.html").read())
    index.exposed = True

    def play(self):
        engine.play(self.section_list)
    play.exposed = True
    
    def arrange(self, section_list):
        engine = Engine(document.getElementById("filename").name)
        #engine.arrange(section_list)
        #self.sections = engine.get_sections()
        self.sections = [(0.0, 8.1030800000000003)
            (8.1030800000000003, 17.119399999999999)
            (25.222480000000001, 10.52399)
            (35.746470000000002, 16.750139999999998)
            (52.496609999999997, 11.51864)
            (64.015249999999995, 18.80688)
            (82.822119999999998, 12.914199999999999)
            (95.736320000000006, 18.047529999999998)
            (113.78385, 35.805979999999998)
            (149.58983000000001, 15.222060000000001)
            (164.81189000000001, 21.20607)]

        # 'sections' is a list of dicts like [{'start': <time>, 'duration': <time>}, etc...]
        body = self._make_arrangement_table(self.sections)
        return HEAD.replace("BODY_HERE", body)
    arrange.exposed = True

    def save(self, title, tags):
        tmpfile = '_tmpfile.mp3'
        if engine:
            engine.save(tmpfile)
            # Upload tmpfile to SoundCloud with title, tags.
        
        return HEAD.replace("BODY_HERE", body)
    save.exposed = True

    def _make_arrangement_table(self, sections):
        # Start the table
        table = '<table border="1"><tr width=1000>'
        totalDuration = sum([s[1] for s in sections])
        for s in sections:
            table += '<td bgcolor=red width=%d' % 1000.0 / (s[0] / totalDuration) + '</td>'
            #table += '<td><iframe src="https://embed.spotify.com/?uri=spotify:track:%s" frameborder="0" width="400" height="80" allowtransparency="true"></iframe></td>' % t["foreign_id"]

        table += '</tr>'
        return table

if __name__ == "__main__":
    cherrypy.server.socket_host = "127.0.0.1"
    cherrypy.server.socket_port = 8080
    config = {
              "/static":
                {"tools.staticdir.on": True,
                 "tools.staticdir.dir": os.getcwd(),
                },
              "/images":
                {"tools.staticdir.on": True,
                 "tools.staticdir.dir": os.getcwd()
                }
             }

    cherrypy.tree.mount(Arranger(), "/", config=config)
    cherrypy.engine.start()
    cherrypy.engine.block()

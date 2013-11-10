import subprocess

from echonest.remix import audio

class Engine(object):
    def __init__(self, filename):
        self.filename = filename
        self.audiofile = audio.LocalAudioFile(filename, verbose=False)
        self.sections = self.audiofile.analysis.sections
        self.arrangement = None
        self.collect = None
        # Current arrangement is whole track in order.
        self.arrange(range(0, len(self.sections)))
        self.play_process = None
        self.arrangement_changed = True

    def _write_output_file(self, section_list, output_file):
        if section_list:
            collect = audio.AudioQuantumList()
            for s in section_list:
                collect.append(self.sections[s])
        else:
            collect = self.collect

        out = audio.getpieces(self.audiofile, collect)
        out.encode(output_file)

    def get_sections(self):
        return self.sections

    def play(self, section_list=None):
        if self.play_process:
            self.kill()

        tmpfile = '_tmpfile_.mp3'
        if section_list or self.arrangement_changed:
            print "building new arrangement..."
            self._write_output_file(section_list, tmpfile)
            self.arrangement_changed = False

        self.play_process = subprocess.Popen("mpg123 -q " + tmpfile, shell=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)

    def arrange(self, section_list):
        '''section_list - a list of section indices to play in order'''
        self.arrangement = section_list
        self.collect = audio.AudioQuantumList()
        for s in self.arrangement:
            self.collect.append(self.sections[s])
        self.arrangement_changed = True
            
    def save(self, output_filename):
        '''save the current arrangement to the given filenmame.'''
        self._write_output_file(None, output_filename)

    def kill(self):
        '''kill the current playback operation'''
        if self.play_process:
            self.play_process.kill()
            self.play_process = None

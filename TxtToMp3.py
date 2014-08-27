import sys
import wave
import struct 
import random
import math
from itertools import *

# morse code letters and number is dict
morse = {'a' : ".-", 'b' : "-...",
'c' : "-.-. ", 'd' : "-.. ",
'e' : ". ", 'f' : "..-. ",
'g' : "--. ", 'h' : ".... ",
'i' : ".. ", 'j' : ".--- ",
'k' : "-.- ", 'l' : ".-.. ",
'm' : "-- ", 'n' : "-. ",
'o' : "--- ", 'p' : ".--. ",
'q' : "--.- ", 'r' : ".-. ",
's' : "... ", 't' : "- ",
'u' : "..- ", 'v' : "...- ",
'w' : ".-- ",  'x' : "-..- ",
'y' : "-.-- ", 'z' : "--.. ",
'0' : "----- ", '1' : ".---- ",
'2' : "..--- ", '3' : "...-- ",
'4' : "....- ", '5' : "..... ",
'6' : "-.... ", '7' : "--... ",
'8' : "---.. ", '9' : "----. ",
' ' : "/ " }

# given lower case text return morse code string, with space = / and a space between each morse letter
def text_to_morse(text):
    output = ""
    for c in text:
        output += morse[c];
    return output

# return an packed list of shorts, that makes up a wave for the dash    
def create__wave(frequency, seconds):
    framerate = 44100
    amplitude = 0.5
    period = int(framerate / frequency)
   
    # create a generator sine_wave that returns the values of the sinewave
    lookup_table = [float(amplitude) * math.sin(2.0*math.pi*float(frequency)*(float(i%period)/float(framerate))) for i in xrange(period)]
    sine_wave = (lookup_table[i%period] for i in count(0))
    # upscale the amplitude and create a packed list of values
    values = []
    max_amplitude = 5000
    for i in range((int) (44100 * seconds)):
        val =(sine_wave.next() * max_amplitude )
        values.append(struct.pack('h',val))
    return values

def compute_samples(channels, nsamples=None):
    return islice(izip(*(imap(sum, izip(*channel)) for channel in channels)), nsamples)

def create_audio_file(morse_code):

    wave_file = wave.open("myfile.wav",'wb')
    wave_file.setparams((2,2,44100, 0,'NONE', 'not compressed'))
    
    values = []

    # define the dot and dash wave, to speed up the program
    dot_wave = create__wave(1000,0.5) 
    dash_wave = create__wave(500,1)
    empty = [struct.pack('h',0) for i in range(44100)]

    for c in morse_code:
        if c == '.':
            values += dot_wave
            values += empty
            
        if c == '-':
            values += dash_wave
            values += empty


    value_str = ''.join(values)
    wave_file.writeframes(value_str)

    wave_file.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit()
    input_string = sys.argv[1]
    print input_string
    input_string.lower()    
    create_audio_file( text_to_morse(input_string))

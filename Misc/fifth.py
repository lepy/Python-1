# https://stackoverflow.com/questions/8299303/generating-sine-wave-sound-in-python?rq=1
# https://en.wikipedia.org/wiki/Symphony_No._5_(Beethoven)

import pyaudio
import numpy as np
from time import sleep


# range [0.0, 1.0]
VOLUME = 1.0

# sampling rate, Hz, must be integer
SAMPLING_RATE = 44100

# in seconds, may be float
SHORT_DURATION = 0.3   
LONG_DURATION = 4.0

# sine frequency, Hz, may be float
G_FREQUENCY = 391.995        
E_FREQUENCY = 329.628
F_FREQUENCY = 342.228
D_FREQUENCY = 293.665

PI = np.pi

def short_pause():
    sleep(0.2)
    
def long_pause():
    sleep(0.7)

# generate samples. 
# Note conversion to float32 array
def samples(rate, duration, frequency):
    
    sample = (np.sin(
        2 * PI * np.arange(rate * duration)
        * frequency / rate)).astype(np.float32)
    
    return sample


p = pyaudio.PyAudio()

# for paFloat32 sample values 
# must be in range [-1.0, 1.0]
stream = p.open(
    format=pyaudio.paFloat32, channels=1,
    rate=SAMPLING_RATE, output=True)

g_short = samples(
    SAMPLING_RATE, SHORT_DURATION, G_FREQUENCY)
    
e_long = samples(
    SAMPLING_RATE, LONG_DURATION, E_FREQUENCY)
    
f_short = samples(
    SAMPLING_RATE, SHORT_DURATION, F_FREQUENCY)
    
d_long = samples(
    SAMPLING_RATE, LONG_DURATION, D_FREQUENCY)

# play

# three short Gs
for _ in range (3): 
    stream.write(VOLUME * g_short)
    short_pause()

# one long E    
stream.write(VOLUME * e_long)
long_pause()

# three short Fs
for _ in range (3): 
    stream.write(VOLUME * f_short)
    short_pause()

# one long D
stream.write(VOLUME * d_long)

stream.stop_stream()
stream.close()
p.terminate()


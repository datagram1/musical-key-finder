#!/usr/local/bin/python3.9

import sys
import json
import scipy.stats
import librosa
from keyfinder import *

file = sys.argv[1]
#print(file)
y, sr = librosa.load(file, sr=None)
onset_env = librosa.onset.onset_strength(y=y, sr=sr)
#simple static tempo
tempo = librosa.beat.tempo(onset_envelope=onset_env, sr=sr)

#detect the key
y_harmonic, y_percussive = librosa.effects.hpss(y)
key = Tonal_Fragment(y_harmonic, sr)

#static tempo, uniform dist
prior = scipy.stats.uniform(30, 300)  # uniform over 30-300 BPM
utempo = librosa.beat.tempo(onset_envelope=onset_env, sr=sr, prior=prior)

#build the output object
output = dict()
output['freqs'] = key.keyfreqs
for x in output['freqs'].keys():
	output['freqs'][x] = str(output['freqs'][x])
output['key'] = key.key
if key.altkey is not None:
	output['altkey'] = key.altkey
output['bpm'] = str(tempo[0].round(0).astype(int))
output['bpmu'] = str(utempo[0].round(0).astype(int))
output['bpm_float'] = str(tempo[0])
output['bpmu_float'] = str(utempo[0])
#print(output)
print(json.dumps(output))

#!/usr/bin/env python

#print "*** FM PIANO VERSION WITH NOTE CACHING ***"

"""
##########################################################################
#                       * * *  PySynth  * * *
#       A very basic audio synthesizer in Python (www.python.org)
#
#          Martin C. Doege, 2012-11-29 (mdoege@compuserve.com)
##########################################################################
# Based on a program by Tyler Eaves (tyler at tylereaves.com) found at
#   http://mail.python.org/pipermail/python-list/2000-August/041308.html
##########################################################################
# 'song' is a Python list (or tuple) in which the song is defined,
#   the format is [['note', value]]
# Notes are 'a' through 'g' of course,
# optionally with '#' or 'b' appended for sharps or flats.
# Finally the octave number (defaults to octave 4 if not given).
# An asterisk at the end makes the note a little louder (useful for the beat).
# 'r' is a rest.
# Note value is a number:
# 1=Whole Note; 2=Half Note; 4=Quarter Note, etc.
# Dotted notes can be written in two ways:
# 1.33 = -2 = dotted half
# 2.66 = -4 = dotted quarter
# 5.33 = -8 = dotted eighth
"""

import wave, struct
import numpy as np
from random import random, randint
from math import sin, cos, pi, log, exp
from mixfiles import mix_files
from demosongs import *
from mkfreq import getfreq
from pydub import AudioSegment

pitchhz, keynum = getfreq()

A = ["a", "c#", "e", "e"]
B = ["a", "c#", "e", "e"]
C = ["a", "c#", "e", "e"]
D = ["d", "f#", "a", "e"]
E = ["e", "g#", "b", "e"]
F = ["f", "a", "c", "e"]
G = ["g", "b", "d", "e"]
As = ["db", "f", "ab", "e"]
Bs = ["db", "f", "ab", "e"]
Cs = ["db", "f", "ab", "e"]
Ds = ["db", "f", "ab", "e"]
Es = ["db", "f", "ab", "e"]
Fs = ["db", "f", "ab", "e"]
Gs = ["db", "f", "ab", "e"]
Ab = ["db", "f", "ab", "e"]
Cb = ["db", "f", "ab", "e"]
Bb = ["db", "f", "ab", "e"]
Db = ["db", "f", "ab", "e"]
Eb = ["db", "f", "ab", "e"]
Fb = ["db", "f", "ab", "e"]
Gb = ["db", "f", "ab", "e"]
Am = ["db", "f", "ab", "e"]
Bm = ["db", "f", "ab", "e"]
Cm = ["db", "f", "ab", "e"]
Dm = ["db", "f", "ab", "e"]
Em = ["db", "f", "ab", "e"]
Fm = ["db", "f", "ab", "e"]
Gm = ["db", "f", "ab", "e"]
Ad = ["db", "f", "ab", "e"]
Bd = ["db", "f", "ab", "e"]
Cd = ["db", "f", "ab", "e"]
Dd = ["db", "f", "ab", "e"]
Ed = ["db", "f", "ab", "e"]
Fd = ["db", "f", "ab", "e"]
Gd = ["db", "f", "ab", "e"]
Abm = ["db", "f", "ab", "e"]
Bbm = ["db", "f", "ab", "e"]
Cbm = ["db", "f", "ab", "e"]
Dbm = ["db", "f", "ab", "e"]
Ebm = ["db", "f", "ab", "e"]
Fbm = ["db", "f", "ab", "e"]
Gbm = ["db", "f", "ab", "e"]
Asm = ["db", "f", "ab", "e"]
Bsm = ["db", "f", "ab", "e"]
Csm = ["db", "f", "ab", "e"]
Dsm = ["db", "f", "ab", "e"]
Esm = ["db", "f", "ab", "e"]
Fsm = ["db", "f", "ab", "e"]
Gsm = ["db", "f", "ab", "e"]
Abd = ["db", "f", "ab", "e"]
Bbd = ["db", "f", "ab", "e"]
Cbd = ["db", "f", "ab", "e"]
Dbd = ["db", "f", "ab", "e"]
Ebd = ["db", "f", "ab", "e"]
Fbd = ["db", "f", "ab", "e"]
Gbd = ["db", "f", "ab", "e"]
Asd = ["db", "f", "ab", "e"]
Bsd = ["db", "f", "ab", "e"]
Csd = ["db", "f", "ab", "e"]
Dsd = ["db", "f", "ab", "e"]
Esd = ["db", "f", "ab", "e"]
Fsd = ["db", "f", "ab", "e"]
Gsd = ["db", "f", "ab", "e"]


# Bd = ["b", "d", "f", "r"]
# Fsd = ["fs", "a", "c", "r"]
# Csd = ["cs", "eb", "gb", "r"]
# Gsd = ["gs", "b", "d", "r"]
# Dsd = ["ds", "fs", "a", "r"]
# Asd = ["as", "db", "e", "r"]
# Esd = ["f", "as", "b", "r"]
# Cd = ["c", "eb", "gb", "r"]
# Ad = ["a", "c", "eb", "r"]
# Dd = ["d", "f", "ab", "r"]
# Gd = ["g", "bb", "ab", "r"]
# Fd = ["f", "ab", "b", "r"]
# Bbd = ["bb", "db", "e", "r"]
#
# A = ["a", "c#", "e", "gs"]
# B = ["b", "ds", "fs", "as"]
# C = ["c", "e", "g", "ds"]
# D = ["d", "fs", "a", "cs"]
# E = ["e", "gs", "b", "ds"]
# F = ["f", "a", "c", "e"]
# G = ["g", "b", "d", "fs"]
# Cs = ["cs", "f", "gs", "c"]
# Ds = ["ds", "g", "as", "d"]
# ## Es = F
# Fs = ["fs", "as", "cs", "f"]
# Gs = ["gs", "c", "ds", "g"]
# As = ["as", "d", "f", "a"]
# ## Bs = C
# Cb = B
# Db = ["db", "f", "ab", "c"]
# Eb = ["eb", "g", "as", "d"]
# ##Fb = E
# Gb = ["gb", "as", "db", "f"]
# Ab = ["ab", "c", "eb", "g"]
# Bb = ["as", "d", "f", "a"]
#
# Am = ["a", "c", "e", "g"]
# Bm = ["b", "d", "fs", "a"]
# Cm = ["c", "eb", "g", "d"]
# Dm = ["d", "f", "a", "c"]
# Em = ["e", "g", "b", "d"]
# Fm = ["f", "ab", "c", "eb"]
# Gm = ["g", "bb", "d", "f"]
# Csm = ["cs", "e", "gs", "b"]
# Dsm = ["ds", "gb", "as", "db"]
# ## Es = F
# Fsm = ["fs", "a", "cs", "e"]
# Gsm = ["gs", "cb", "ds", "gb"]
# Asm = ["as", "db", "f", "ab"]
# ## Bs = C
# ## Cb = B
# Dbm = ["db", "e", "ab", "b"]
# Ebm = ["eb", "gb", "as", "db"]
# Fb = E
# Gbm = ["gb", "a", "db", "e"]
# Abm = ["ab", "b", "eb", "gb"]
# Bbm = ["as", "db", "f", "ab"]

chord_progression = {
"I":
[C, G, D, A, E, B, Fs, F, Bb, Eb, Ab, Db, Gb, Cb],
"II":
[Dm, Am, Em, Bm, Fsm, Csm, Gsm, Gm, Cm, Fm, Bbm, Ebm, Abm, Dbm],
"III":
[Em, Bm, Fsm, Csm, Gsm, Dsm, Asm, Am, Dm, Gm, Cm, Fm, Bbm, Ebm],
"IV":
[F, C, G, D, A, E, B, Bb, Eb, Ab, Db, Gb, Cb, Fb],
"V":
[G, D, A, E, B, Fs, Cs, C, F, Bb, Eb, Ab, Db, Gb],
"VI":
[Am, Em, Bm, Fsm, Csm, Dsm, Dm, Gm, Cm, Fm, Bbm, Ebm, Abm],
"VII":
[Bd, Fsd, Csd, Gsd, Dsd, Asd, Esd, Cd, Ad, Dd, Gd, Cd, Fd, Bbd]
}

# Harmonic intensities (dB) for selected piano keys,
Gsd = ["db", "f", "ab", "e"]
# measured with output from a Yamaha P-85
harmo = (
  (1, -15.8, -3., -15.3, -22.8, -40.7),
  (16, -15.8, -3., -15.3, -22.8, -40.7),
  (28, -5.7, -4.4, -17.7, -16., -38.7),
  (40, -6.8, -17.2, -22.4, -16.8, -75.6),
  (52, -8.4, -19.7, -23.5, -21.6, -76.8),
  (64, -9.3, -20.8, -37.2, -36.3, -76.4),
  (76, -18., -64.5, -74.4, -77.3, -80.8),
  (88, -24.8, -53.8, -77.2, -80.8, -90.),
)

def linint(arr, x):
	"Interpolate an (X, Y) array linearly."
	for v in arr:
		if v[0] == x: return v[1]
	xvals = [v[0] for v in arr]
	ux = max(xvals)
	lx = min(xvals)
	try: assert lx <= x <= ux
	except:
		#print lx, x, ux
		raise
	for v in arr:
		if v[0] > x and v[0] - x <= ux - x:
			ux = v[0]
			uy = v[1]
		if v[0] < x and x - v[0] >= lx - x:
			lx = v[0]
			ly = v[1]
	#print lx, ly, ux, uy
	return (float(x) - lx) / (ux - lx) * (uy - ly) + ly

harmtab = np.zeros((88, 20))

for h in range(1, len(harmo[0])):
	dat = []
	for n in range(len(harmo)):
		dat.append((float(harmo[n][0]), harmo[n][h]))
	for h2 in range(88):
		harmtab[h2,h] = linint(dat, h2+1)

#print harmtab[keynum['c4'],:]
for h2 in range(88):
	for n in range(20):
		ref = harmtab[h2,1]
		harmtab[h2,n] = 10.**((harmtab[h2,n] - ref)/20.)
#print harmtab[keynum['c4'],:]

##########################################################################
#### Main program starts below
##########################################################################
# Some parameters:

# Beats (quarters) per minute
# e.g. bpm = 95

# Octave shift (neg. integer -> lower; pos. integer -> higher)
# e.g. transpose = 0

# Playing style (e.g., 0.8 = very legato and e.g., 0.3 = very staccato)
# e.g. leg_stac = 0.6

# Volume boost for asterisk notes (1. = no boost)
# e.g. boost = 1.2

# Output file name
#fn = 'pysynth_output.wav'

# Other parameters:

# Influences the decay of harmonics over frequency. Lowering the
# value eliminates even more harmonics at high frequencies.
# Suggested range: between 3. and 5., depending on the frequency response
#  of speakers/headphones used
harm_max = 5.
##########################################################################

# def musicStyle(style_music):
#     styleMusic = {"Rock":{tempo:120, notelength: 4}, "Early Rock":{tempo:120, notelength: 4}, "Classical":{tempo:90, notelength: 2}}


def wavListCreator(input_list, output_files):
    wav_lists = [[] for _ in range(0,4)]
    randomOctave = randint(1,5)
    noteBeat = 1

    for eachinput in input_list: #parse through every roman numeral
        #randomChord = randint(0,13)
        randomChord = 0
        ourChord = chord_progression[eachinput][randomChord] # assign a random chord variable (i.e. chord A)

        for x, list in enumerate(wav_lists):
            list.append([ourChord[x]+str(randomOctave), noteBeat])

    print (wav_lists)

    for num in range(0,4):
        make_wav(wav_lists[num], fn = output_files[num])


def make_wav(song,bpm=120,transpose=0,leg_stac=.9,boost=1.1,repeat=0,fn="out.wav", silent=False):
	data = []
	note_cache = {}
	cache_this = {}

	f=wave.open(fn,'w')

	f.setnchannels(1)
	f.setsampwidth(2)
	f.setframerate(44100)
	f.setcomptype('NONE','Not Compressed')

	bpmfac = 120./bpm

	def length(l):
	    return 88200./l*bpmfac

	def waves2(hz,l):
	    a=44100./hz
	    b=float(l)/44100.*hz
	    return [a,round(b)]

	att_len = 3000
	att_bass = np.zeros(att_len)
	att_treb = np.zeros(att_len)
	for n in range(att_len):
		att_treb[n] = linint(((0,0.), (100, .2), (300, .7), (400, .6), (600, .25), (800, .9), (1000, 1.25), (2000,1.15), (3000, 1.)), n)
		att_bass[n] = linint(((0,0.), (100, .1), (300, .2), (400, .15), (600, .1), (800, .9), (1000, 1.25), (2000,1.15), (3000, 1.)), n)
	decay = np.zeros(1000)
	for n in range(900):
		decay[n] = exp(linint(( (0,log(3)), (3,log(5)), (5, log(1.)), (6, log(.8)), (9,log(.1)) ), n/100.))

	def zz(a):
		for q in range(len(a)):
			if a[q] < 0: a[q] = 0

	def render2(a, b, vol, pos, knum, note):
		l=waves2(a, b)
		q=int(l[0]*l[1])
		lf = log(a)
		snd_len = max(int(3.1*q), 44100)

		raw_note = 12*44100
		if note not in list(note_cache.keys()):
			x2 = np.arange(raw_note)
			sina = 2. * pi * x2 / float(l[0])
			sina14 = 14. * 2. * pi * x2 / float(l[0])
			amp1 = 1. - (x2/snd_len)
			amp2 = 1. - (4*x2/snd_len)
			amp_3to6 = 1. - (.25*x2/snd_len)
			zz(amp1)
			zz(amp2)
			zz(amp_3to6)
			new = (
				amp1 * np.sin(sina+.58*amp2*np.sin(sina14))
	            	  + amp_3to6 * np.sin(sina+.89*amp_3to6*np.sin(sina))
	           	   + amp_3to6 * np.sin(sina+.79*amp_3to6*np.sin(sina))
		   	   )
			new *= np.exp(-x2/decay[int(lf*100)]/44100.)
			if cache_this[note] > 1:
				note_cache[note] = new.copy()
		else:
			new = note_cache[note].copy()
		dec_ind = int(leg_stac*q)
		new[dec_ind:] *= np.exp(-np.arange(raw_note-dec_ind)/3000.)
		if snd_len > raw_note:
			print("Warning, note too long:", snd_len, raw_note)
			snd_len = raw_note
		data[pos:pos+snd_len] += ( new[:snd_len] * vol  )

	ex_pos = 0.
	t_len = 0
	for y, x in song:
		if x < 0:
			t_len+=length(-2.*x/3.)
		else:
			t_len+=length(x)
		if y[-1] == '*':
			y = y[:-1]
		if not y[-1].isdigit():
			y += '4'
		cache_this[y] = cache_this.get(y, 0) + 1
	#print "Note frequencies in song:", cache_this
	data = np.zeros(int((repeat+1)*t_len + 441000))
	#print len(data)/44100., "s allocated"

	for rp in range(repeat+1):
		for nn, x in enumerate(song):
			if not nn % 4 and silent == False:
				print("[%u/%u]\t" % (nn+1,len(song)))
			if x[0]!='r':
				if x[0][-1] == '*':
					vol = boost
					note = x[0][:-1]
				else:
					vol = 1.
					note = x[0]
				if not note[-1].isdigit():
					note += '4'		# default to fourth octave
				a=pitchhz[note]
				kn = keynum[note]
				a = a * 2**transpose
				if x[1] < 0:
					b=length(-2.*x[1]/3.)
				else:
					b=length(x[1])

				render2(a, b, vol, int(ex_pos), kn, note)
				ex_pos = ex_pos + b

			if x[0]=='r':
				b=length(x[1])
				ex_pos = ex_pos + b

	##########################################################################
	# Write to output file (in WAV format)
	##########################################################################
	if silent == False:
		print("Writing to file", fn)

	data = data / (data.max() * 2.)
	out_len = int(2. * 44100. + ex_pos+.5)
	data2 = np.zeros(out_len, np.short)
	data2[:] = 32000. * data[:out_len]
	f.writeframes(data2.tostring())
	f.close()
	print()

def mergeWavFiles(fileList, final_song):
    sound1 = AudioSegment.from_wav(fileList[0])
    sound2 = AudioSegment.from_wav(fileList[1])
    sound3 = AudioSegment.from_wav(fileList[2])
    sound4 = AudioSegment.from_wav(fileList[3])

    combined_sounds = sound1 + sound2 + sound3 + sound4
    combined_sounds.export(final_song, format="wav")
    print ("SUCCESS COMBINING!")

##########################################################################
# Synthesize demo songs
##########################################################################

if __name__ == '__main__':
    print("*** TEST VERSION ***")

    input_list = ["I", "IV", "II"]
    output_files = ["CS1.wav", "CS2.wav", "CS3.wav", "CS4.wav"]
    final_song = "FINAL_SONG.wav"

    wavListCreator(input_list, output_files)

    mergeWavFiles(output_files, final_song)

import numpy as np
import os
import sys
import random
script_dir = os.path.dirname( __file__ )
pygmu_dir = os.path.join( script_dir, '..', 'pygmu' )
sys.path.append( pygmu_dir )
import pygmu as pg
import utils as ut

words = pg.WavReaderPE("samples/Tamper_TVFrame4.wav")
orig_beat = pg.WavReaderPE("samples/BigBeat120bpm10.wav")
orig_bpm = 120 * 48000 / 44100   # higher srate
orig_duration = 176865

bpm = 100
beat_dur = int(orig_duration*orig_bpm/bpm)
beat = pg.TimewarpPE(orig_beat, pg.IdentityPE().gain(bpm/orig_bpm)).loop(beat_dur).crop(pg.Extent(0))

q_note = words.frame_rate() * 60.0 / bpm

#   and the typical mediterranian diet.   so increase your intake of olive oil,   fresh vegetables
# ^         ^       ^             ^     ^      ^           ^         ^          ^       ^  

def beat_to_frame(b):
	return int(b * q_note)

def snip(pe, s, e):
	return pe.crop(pg.Extent(int(s), int(e))).time_shift(int(-s))

and_the = snip(words, 0, 25208)
typical = snip(words, 25208, 55196)
mediterranean = snip(words, 56934, 95615)
diet = snip(words, 95615, 121257)
so_in = snip(words, 128211, 153853)
crease_your = snip(words, 153961, 176344)
intake_of = snip(words, 176670, 206441)
olive_oil = snip(words, 206767, 244361)
fresh = snip(words, 244361, 258051)
vegetables = snip(words, 258051, 294450)

snips = [typical, mediterranean, diet, crease_your, intake_of, olive_oil, fresh, vegetables]

def choose_snip():
	return random.choice(snips)


def tuned_snip(snip, beat, pitch, q):
	f0 = ut.pitch_to_freq(pitch)
	if q > 0:
		pe = pg.BQ2LowPassPE(snip, f0, q)
	else:
		pe = snip
	return pe.time_shift(int(beat * q_note))

mix = pg.MixPE(
	beat.time_shift(beat_to_frame(4)).gain(0.2).crop(pg.Extent(0, int(32 * q_note))),
	tuned_snip(typical, 0, 65, 256),
	tuned_snip(typical, 1, 65, 256),
	tuned_snip(typical, 2, 65, 256),
	tuned_snip(typical, 3, 65, 256),

	tuned_snip(typical, 4, 65, 256),
	tuned_snip(typical, 5, 65, 256),
	tuned_snip(typical, 6, 65, 256),
	tuned_snip(typical, 7, 65, 256),

	tuned_snip(typical, 8, 65, 256),
	tuned_snip(typical, 9, 72, 256),
	tuned_snip(typical, 10, 68, 256),
	tuned_snip(typical, 11, 65, 256),

	tuned_snip(typical, 12, 64, 256),
	tuned_snip(fresh, 13, 65, 256),
	tuned_snip(fresh, 13.5, 67, 256),
	tuned_snip(mediterranean, 14, 68, 256),
	tuned_snip(diet, 15.25, 70, 64),
	tuned_snip(diet, 15.5, 68, 64),
	tuned_snip(diet, 15.75, 67, 64),

	tuned_snip(typical, 16, 65, 128),
	tuned_snip(typical, 17, 65, 64),
	tuned_snip(typical, 18, 65, 32),
	tuned_snip(typical, 19, 65, 16),

	tuned_snip(typical, 20, 65, 16),
	tuned_snip(typical, 21, 65, 16),
	tuned_snip(typical, 22, 65, 16),
	tuned_snip(typical, 23, 65, 16),

	tuned_snip(typical, 24, 65, 16),
	tuned_snip(typical, 25, 72, 16),
	tuned_snip(typical, 26, 68, 16),
	tuned_snip(typical, 27, 65, 16),

	tuned_snip(typical, 28, 64, 16),
	tuned_snip(fresh, 29, 65, 16),
	tuned_snip(fresh, 29.5, 67, 16),
	tuned_snip(mediterranean, 30, 68, 16),
	tuned_snip(diet, 31.25, 70, 2),
	tuned_snip(diet, 31.5, 68, 2),
	tuned_snip(diet, 31.75, 67, 2),

	tuned_snip(olive_oil, 32.0, 60, 256)
	)

# Biquad2PE runs fast enough to render in real time...
pg.Transport(mix).play()

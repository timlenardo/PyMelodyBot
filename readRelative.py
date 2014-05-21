#!/usr/bin python

from music21 import *
from pymarkovchain import MarkovChain
from random import randrange
import copy
import os
import inspect
mc = MarkovChain("./markov")

db = ''
assoc = {}

path = 'MidiMelodies'

#for s in files:
for filename in os.listdir(path):
  s = converter.parse(path + '/' + filename)
  #s = converter.parse(s)i
  part = s.parts[0]
  first = 1
  # Keep track of the first note in the melody for relative tracking
  first_note = note.Note()
  first_ps = 0

  for cur_note in part.notes:
    name = cur_note.fullName
    # If the current note is a chord, get instead the root of the chord
    if "Chord" in name:
      n = note.Note(cur_note.pitches[0])
      n.duration = cur_note.duration
      #print n
      #print cur_note
      cur_note = n

    to_add = ""
    # Set the first note
    if first == 1:
      first_note = cur_note
      first_ps= cur_note.ps
      dur = cur_note.duration.fullName
      assoc[dur] = cur_note.duration
      to_add = "0!@#" + dur
      first = 0
    else:
       # Need to somehow set the relative value
       cur_ps = cur_note.ps
       dur = cur_note.duration.fullName
       assoc[dur] = cur_note.duration
       next_val = cur_ps - first_ps
       to_add = str(next_val) + "!@#" + dur
    db = db + (' ' + to_add);
  db = db + ('\n');

mc.generateDatabase(db, '\n')
sen = mc.generateString()
s1 = stream.Stream()

sen = sen.split(' ')
# print sen
for word in sen:
  val_dur = word.split('!@#')
  val = val_dur[0]
  dur = val_dur[1]
  base = 65
  cur_val = base + float(val)
  cur_dur = assoc[dur]
  p = pitch.Pitch('C')
  p.ps = cur_val
  n = note.Note(p)
  n.duration = cur_dur
  s1.append(n)
  '''try:
    note = assoc[word]
    note_add = copy.deepcopy(note)
    word = word.replace('#', ' ')
    s1.append(note_add)
  except:
    pass'''

index = randrange(1000)
name = 'GeneratedMidi/generated_MIDI' + str(index) + '.mid'
print index

mf = midi.translate.streamToMidiFile(s1)

print len(mf.tracks)
print len(mf.tracks[0].events)
mf.open(name, 'wb')
mf.write()
mf.close()

#s1.write('midi', name)

#for p in s.parts:
#  print str(p)'''



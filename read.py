#!/usr/bin python

from music21 import *
from pymarkovchain import MarkovChain
from random import randrange
import copy
import os
import inspect
mc = MarkovChain("./markov")

files = ['/Users/telenardo/Downloads/midi0.mid','/Users/telenardo/Downloads/midi1.mid','/Users/telenardo/Downloads/midi2.mid','/Users/telenardo/Downloads/midi3.mid','/Users/telenardo/Downloads/midi4.mid']
db = ''
assoc = {}

path = 'MidiMelodies'

#for s in files:

for filename in os.listdir(path):
  s = converter.parse(path + '/' + filename)
  part = s.parts[0]

  for cur_note in part.notes:

    name = cur_note.fullName
    '''if "Chord" in name:
      n = note.Note(cur_note.pitches[0])
      n.duration = cur_note.duration
      print cur_note
      print n
      cur_note = n
      name = n.fullName'''
    name = name.replace(' ','#')
    assoc[name] = cur_note
    db = db + (' ' + name);
  db = db + ('\n');

mc.generateDatabase(db, '\n')
sen = mc.generateString()
s1 = stream.Stream()


keepGoing = 1
sen = ""

while keepGoing == 1:
  mc.generateDatabase(db, '\n')
  sen = mc.generateString()
  sen = sen.split(' ')
  length = 0.0
  counter = 0
  for word in sen:
    counter = counter + 1
    val_dur = word.split('!@#')
    dur = val_dur[1]
    cur_dur = assoc[dur]
    length += cur_dur.quarterLength
  if length == 4.0 and counter > 10:
    keepGoing = 0


s1 = stream.Stream()

# print sen
for word in sen:
  print "Word" + word
  val_dur = word.split('!@#')
  val = val_dur[0]
  dur = val_dur[1]
  # Start all melodies on C4
  base = 65
  # For rests
  if val == "REST":
    cur_dur = assoc[dur]
    n = note.Rest()
    n.duration = cur_dur
    s1.append(n)
  else:
    val = val.strip()
    print val
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
name = '/Users/telenardo/Downloads/generated_MIDI' + str(index) + '.mid'
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





'''sen = sen.split(' ')
for word in sen:
  try:
    note = assoc[word]
    note_add = copy.deepcopy(note)
    word = word.replace('#', ' ')
    s1.append(note_add)
  except:
    pass

index = randrange(1000)
name = '/Users/telenardo/Downloads/generated_MIDI' + str(index) + '.mid'
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



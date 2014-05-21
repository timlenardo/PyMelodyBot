#!/usr/bin python

from music21 import *
from pymarkovchain import MarkovChain
from random import randrange
import copy
import os
import inspect
mc = MarkovChain("./markov")

files = ['/Users/telenardo/Downloads/midi0.mid']#,'/Users/telenardo/Downloads/midi1.mid','/Users/telenardo/Downloads/midi2.mid','/Users/telenardo/Downloads/midi3.mid','/Users/telenardo/Downloads/midi4.mid']
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
  last_add = ""

  for cur_note in part.notesAndRests:
    name = cur_note.fullName
    # If the current note is a chord, get instead the root of the chord
    if "Chord" in name:
      n = note.Note(cur_note.pitches[0])
      n.duration = cur_note.duration
      #print n
      #print cur_note
      cur_note = n

    # Read and store the duration
    dur = cur_note.duration.fullName
    dur = dur.replace(' ', '@')
    assoc[dur] = cur_note.duration
    add = 1

    to_add = ""
    if cur_note.isRest:
      to_add = "REST"
    else:
      # Set the first note
      if first == 1:
        first_note = cur_note
        first_ps= cur_note.ps
        to_add = "0.0"
        first = 0
      else:
        # Need to somehow set the relative value
        cur_ps = cur_note.ps
        next_val = cur_ps - first_ps
        # Limit the size of jumps?
        #if next_val < 12.0 and next_val > -12.0:
        to_add = str(next_val)
        #else:
        #  add = 0

    #if add == 1:
    # Add the duration
    to_add = to_add + "!@#" + dur
    db = db + (' ' + to_add);

    # KEEP TRACK OF CURRENT AND LAST NOTE
    # EXEMPTING THE FIRST NOTE OF EACH
    if last_add != "":
      db = db + "|||||" + last_add
    last_add = to_add

  db = db + ('\n');

keepGoing = 1
sen = ""

# Impose restrictions on the number of notes in the melody
# For example... 4 Beats, at least 10 notes...
while keepGoing == 1:
  mc.generateDatabase(db, '\n')
  sen = mc.generateString()
  sen = sen.split(' ')
  length = 0.0
  counter = 0
  for word in sen:
    # If double, take the latter half
    if "|||||" in word:
      word = word.split('|||||')[1]
    # Up the counter
    counter = counter + 1
    val_dur = word.split('!@#')
    dur = val_dur[1]
    cur_dur = assoc[dur]
    length += cur_dur.quarterLength
  # STOP THE LOOP WHEN CONDITIONS ARE MET!
  if length == 1.0 and counter > 3:
    keepGoing = 0

# Create the stream to return
s1 = stream.Stream()

# Print out the melody to file!
for word in sen:
  # Again, if Double take the latter half of the string
  if "|||||" in word:
    word = word.split('|||||')[1]
  print word
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
    val = ''.join(val.split())
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



import os
from mido import MidiFile, MidiTrack, Message
import random

import geneticalgorithm as ga


def generate_random(snote=50, mlength=12, numofmidi=10, pitchrnd=False, timernd=False):
    
	notes = range(snote, snote+mlength)
	times = range(50,300)
	time = 100 

	noterange = range(mlength)

	# pitch range for random pitch value ;
	pitches = range(-8192,8191)
    
	# Create music folder if it does not exist
	if not os.path.exists('music'):
		os.makedirs('music')

	for j in range(numofmidi):
    
		mid = MidiFile(type=0) # type0 can have only one track
    
		track = MidiTrack() # note list (kind of)

		mid.tracks.append(track)
    
		# the note which the pitch will change for
		pitchnote = random.choice(noterange)
    
		for i in noterange:

			note = random.choice(notes)
			pitch = random.choice(pitches)
            
			if timernd:
				time = random.choice(times)
        
			if pitchrnd:
				# Change the pitch for only one note
				if i == pitchnote: # Change the pitch on third note
					track.append(Message('pitchwheel', pitch=pitch))
				if i == (pitchnote +1): # Change the pitch back to default
					track.append(Message('pitchwheel'))
        
			track.append(Message('note_on', channel=0, note=note, time=time))
			track.append(Message('note_off', channel=0, note=note, time=time))
        

			mid.save('music/random' + str(j) + '.mid')



def apply_mutation(mutantnotelist, midino, snote=50):

	mid = MidiFile(type=0) # type0 can have only one track
    
	track = MidiTrack() # note list (kind of)

	mid.tracks.append(track)
    
	time = 100
    
	# Create mutant music folder if it does not exist
	if not os.path.exists('mutantmusic'):
		os.makedirs('mutantmusic')
    
	# add the octaves back
	mutantnotelist2 = [x+snote for x in mutantnotelist]
	
	for note in mutantnotelist2:
        
		#print(note)
        
		track.append(Message('note_on', channel=0, note=int(note), time=time))
		track.append(Message('note_off', channel=0, note=int(note), time=time))
        
        
	mid.save('mutantmusic/random' + str(midino) + '.mid')



def read_midi(filename, snote=50):
    
	mid = MidiFile(filename)
    
	noteonlist = []
	for i, track in enumerate(mid.tracks):
		#print('Track {}: {}'.format(i, track.name))
		for message in track:
			#print(message)
			if message.type == 'note_on':
				noteonlist.append(message.note)
    
	# normalize the note integers for mutation by reducing octaves
	notelist = [x-snote for x in noteonlist]
    
	return notelist



if __name__ == "__main__":

	mlength = 12
	snote = 50 # starting note
	numofmidi = 10 # number of midi files

	pitchrnd = False # do not include pitch variations for now
	timernd = False # do not include time variations for now

	generate_random(snote, mlength, numofmidi, pitchrnd, timernd)

	for j in range(numofmidi):
    
		midiname = 'music/random' + str(j) + '.mid'
    
		notelist = read_midi(midiname, snote)
    
		mutantnotelist = ga.mutate(notelist, mlength)
    
		apply_mutation(mutantnotelist, j, snote)

	print('Midi files are created. Please check the "music" and “mutantmusic” folder')

# -*- coding: utf-8 -*-
"""
Based on code from Jordy Thielen
Loads the data from the music21 corpus, and applies a music model to it to extract the distribution.
"""

import sys
import music21
import musicmodel

class Generator:

    # model: 'flat', 'firstOrder'
    # corpus: allFolk', 'folk', 'essenFolk', 'bach'
    def __init__(self, modelType, corpus):
        self.corpus = corpus
        self.modelType = modelType

    def setScores(self):
        paths = 'empty'
        if self.corpus  == 'allFolk':
            paths = music21.corpus.getComposer('miscFolk')
            paths.extend(music21.corpus.getComposer('essenFolksong'))
        elif self.corpus == 'folk':
            paths = music21.corpus.getComposer('miscFolk')
        elif self.corpus == 'essenFolk':
            paths = music21.corpus.getComposer('essenFolksong')
        elif self.corpus == 'bach':
            paths = music21.corpus.getComposer('bach')
        else:
            print("Unkown corpus selected.")
            sys.exit(-1)
        scores = []
        for path in paths:
            print('Parsing; ', path)
            try:
                scores.append(music21.corpus.parse(path))
            except:
                print('Error when parsing the path; ', path)
        self.scores = scores

    def setNotes(self):
        self.setScores()
        notes = []
        for s in range(len(self.scores)):
            score = self.scores[s]
            scoreNotes = score.flat.notes
            print("Transposing ", len(scoreNotes), " notes for score; ", (s+1), "/", len(self.scores))
            for n in range(len(scoreNotes)):
                # transpose
                note = scoreNotes[n]
                note.transpose(-1*note.getContextByClass('KeySignature').pitchAndMode[0].pitchClass)
                notes.append(note) 
        self.notes = notes

    
    def generateDistribution(self):
        self.setNotes()
        model = musicmodel.Model(self.modelType, self.notes)
        return model.getDistribution()



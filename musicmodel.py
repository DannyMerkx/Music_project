# -*- coding: utf-8 -*-
"""
Based on code from Jordy Thielen
Creates the specified distribution (modelType) based on the given data.
"""

import music21
import sys
import numpy
import matplotlib.pyplot as plt

class Model:
    
    maxRange = 12
    
    def __init__(self, modelType, data):
        self.type = modelType
        self.data = [x for x in data if isinstance(x, music21.note.Note)]       
        if self.type == 'flat':
            self.distribution = self.createFlatDistribution()
        elif self.type == 'firstOrder':
            self.distribution = self.createFirstOrderDistribution()
        elif self.type == 'secondOrder':
            self.distribution= self.createSecondOrderDistribution()
        else:
            print('Unknown model type selected.')
            sys.exit(-2)
        self.plotDistribution()

    def getDistribution(self):
        return self.distribution

    def createFlatDistribution(self):
        distribution = [[1.0/12 for i in range(self.maxRange)] for j in range(self.maxRange)]
        print(distribution)
        return distribution
        
    def createFirstOrderDistribution(self):
        countDict = self.countNotes()
        totals = self.sumColumns(countDict)
        distribution = [[0.0 for i in range(self.maxRange)] for j in range(self.maxRange)]
        for x in range(0,self.maxRange):
            for y in range(0,self.maxRange):
                if not(totals[x] == 0):
                    distribution[x][y] = countDict[(x,y)] / totals[x]           
        return distribution
        
    def createSecondOrderDistribution(self):
        countDict = self.countNotesTriples()
        totals = self.sumColumnsTriples(countDict)
        distribution = [[0.0 for i in range(self.maxRange)] for j in range(self.maxRange*self.maxRange)]
        count=0
        for x in range(0,self.maxRange):
            for y in range(0,self.maxRange):
                for z in range (0,self.maxRange):
                    if not(totals[count] == 0):
                        distribution[count][z] = countDict[(x,y,z)] / totals[count]    
                count=count+1
        return distribution     
        
    def sumColumns(self, countDict):
        totals = [0.0 for i in range(self.maxRange)]
        for x in range(0,self.maxRange):
            for y in range(0,self.maxRange):
                totals[x] = countDict[(x,y)] + totals[x] 
        return totals
    
    def sumColumnsTriples(self, countDict):
        totals = [0.0 for i in range(self.maxRange*self.maxRange)]
        count=0
        for x in range(0,self.maxRange):
            for y in range(0,self.maxRange):
                for z in range(0,self.maxRange):
                    totals[count] = countDict[(x,y,z)] + totals[count]
                count=count+1
        return totals
                
    def countNotes(self):
        countDict = dict([((x, y), 0) for x in range(self.maxRange) for y in range(self.maxRange)])
        start = 0
        while not(isinstance(self.data[start], music21.note.Note)):
            start = start + 1
        firstNote = self.data[start].pitch.pitchClass
        for n in range(start, len(self.data)):
            if isinstance(self.data[n], music21.note.Note):
                secondNote = self.data[n].pitch.pitchClass
                countDict[(firstNote, secondNote)] = countDict[(firstNote, secondNote)] + 1
                firstNote = self.data[n].pitch.pitchClass 
        return countDict
    
    def countNotesTriples(self):
        countDictTriples = dict([((x, y, z), 0) for x in range(self.maxRange) for y in range(self.maxRange) for z in range(self.maxRange)])
        start = 0
        while not(isinstance(self.data[start], music21.note.Note)):
            start = start + 1        
        for n in range(start, len(self.data)-2):
            if isinstance(self.data[n], music21.note.Note) and isinstance(self.data[n+1], music21.note.Note) and isinstance(self.data[n+2], music21.note.Note):                                
                firstNote = self.data[n].pitch.pitchClass                
                secondNote = self.data[n+1].pitch.pitchClass
                thirdNote = self.data[n+2].pitch.pitchClass
                countDictTriples[(firstNote, secondNote, thirdNote)] = countDictTriples[(firstNote, secondNote, thirdNote)] + 1
        return countDictTriples
        
    def plotDistribution(self):
        plt.figure()
        plt.title(self.type)
        plt.imshow(self.distribution)
        plt.xticks(numpy.arange(0,12), ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'])
        plt.yticks(numpy.arange(0,12), ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'])
        plt.show()
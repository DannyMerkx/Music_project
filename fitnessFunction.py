'''


'''

from scipy import spatial
import numpy as np

###########################################################################
#           PITCH TRANSITION PROBABILITIES
###########################################################################

# Huron, page 70, only based on 7 figures
probPitchTable = [[0, 0.056, 0, 0, 0, 0.056, 0.056, 0, 0, 0, 0],
                  [0, 0, 0.056, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0.011, 0, 0.022, 0.011, 0, 0.078, 0, 0.022, 0, 0.022, 0.056],
                  [0, 0, 0, 0, 0.056, 0, 0, 0, 0, 0, 0],
                  [0.011, 0, 0.011, 0.011, 0, 0.011, 0, 0.011, 0, 0.011, 0],
                  [0.056, 0, 0, 0, 0.056, 0, 0, 0, 0, 0, 0],
                  [0.011, 0, 0.011, 0.011, 0, 0, 0, 0.011, 0, 0.011, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0.056, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0.056, 0],
                  [0.011, 0, 0.067, 0.011, 0, 0.011, 0, 0, 0, 0.011, 0],
                  [0.011, 0, 0.011, 0.011, 0, 0.011, 0, 0.011, 0, 0, 0]]

# convert probTable to table with fitness values
fitPitchTable = probPitchTable
for i in range(11):
    for j in range(11):
        if fitPitchTable[i][j]==0:
            fitPitchTable[i][j]=1
        if fitPitchTable[i][j]==0.011:
            fitPitchTable[i][j]=1.2
        if fitPitchTable[i][j]==0.022:
            fitPitchTable[i][j]=1.4
        if fitPitchTable[i][j]==0.056:
            fitPitchTable[i][j]=1.6
        if fitPitchTable[i][j]==0.067:
            fitPitchTable[i][j]=1.8
        if fitPitchTable[i][j]==0.078:
            fitPitchTable[i][j]=2

###########################################################################
#           SCALE TRANSITION PROBABILITIES
###########################################################################

# Huron, page 158 --> scale degrees (I do not fully understand them)
# TODO
# probScaleTable = []
# fitScaleTable = probScaleTable

###########################################################################
#           AVERAGE PITCH HEIGHT
###########################################################################

# Huron, page 87 --> average pitch height for melodies of 12 tones.
averagePitchHeight = [6.7, 7.9, 8.4, 8.5, 8.5, 8.3, 8.5, 8.6, 8.3, 8.0, 7.6, 6.4]

###########################################################################
#           OTHER IDEAS
###########################################################################

# Take into account an a priori probability of that tone at that position in time?
# Huron, page 148-149 --> frequency of tones, both for minor and major scale
# Huron, page 74 --> small tone intervals

###########################################################################
#           FITNESS FUNCTIONS
###########################################################################

def computeFitnessPitchTransitions(melody):
    fitness = 1.0
    for x in range (1,len(melody)-1):
        fitness= fitness * fitPitchTable[melody[x - 1]][melody[x]]
    return fitness

def computeFitnessPitchTransitions2(melody):
    fitness = 0
    for x in range (1,len(melody)-1):
        fitness= fitness + fitPitchTable[melody[x - 1]][melody[x]]
    return fitness

###########################################################################

# TODO
#def computeFitnessScaleTransitions(melody):
#    return fitness

###########################################################################

def computeFitnessPitchHeight(melody):
    corrMatrix = np.corrcoef(melody, averagePitchHeight)
    return corrMatrix[0,1]

def computeFitnessCombination(melody, ratio=0.05):
    fitness1 = computeFitnessPitchTransitions2(melody)
    fitness2 = 17*computeFitnessPitchHeight(melody)
    return ratio*fitness2 + (1-ratio)*fitness1

###########################################################################

def testDistanceMeasures():
    v1 = [1,2,3,4]
    v2 = [8,7,6,5]
    sim1 = 1 - spatial.distance.cosine(v1,v2)
    sim2 = spatial.distance.correlation(v1,v2)
    sim3 = spatial.distance.euclidean(v1,v2)
    sim4 = spatial.distance.hamming(v1,v2)
    sim5 = np.corrcoef(v1,v2)

    print(['cosine: ',sim1])
    print(['corr: ',sim2])
    print(['euclidean: ',sim3])
    print(['hamming: ',sim4])
    print(['npcorr: ',sim5])
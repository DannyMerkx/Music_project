import geneticalgorithm as ga
import matplotlib.pyplot as plt

results = []

for i in range(10):
    results.append(ga.mutateRandom())
    print(results[i]['bestmelody'])

# red dashes, blue squares and green triangles
plt.plot(range(0,5000), results[0]['progress'], 'r', range(0,5000), results[1]['progress'], 'b', range(0,5000), results[2]['progress'], 'g')
plt.show()

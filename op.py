#Complexity-entropy plane for logistic map and Gaussian noise.

import numpy as np
import ordpy
from matplotlib import pylab as plt

def logistic(a=4, n=100000, x0=0.4):
    x = np.zeros(n)
    x[0] = x0
    for i in range(n-1):
        x[i+1] = a*x[i]*(1-x[i])
    return(x)

time_series = [logistic(a) for a in [3.05, 3.55, 4]]
time_series += [np.random.normal(size=100000)]


PE = ordpy.permutation_entropy(time_series, dx=4, taux=10)

print (PE)

exit(0);

HC = [ordpy.complexity_entropy(series, dx=4) for series in time_series]


print(HC);

f, ax = plt.subplots(figsize=(8.19, 6.3))

for HC_, label_ in zip(HC, ['Period-2 (a=3.05)',
                            'Period-8 (a=3.55)',
                            'Chaotic (a=4)',
                            'Gaussian noise']):
    ax.scatter(*HC_, label=label_, s=100)

ax.set_xlabel('Permutation entropy, $H$')
ax.set_ylabel('Statistical complexity, $C$')

ax.legend()

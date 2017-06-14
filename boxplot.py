import matplotlib
from matplotlib import pyplot

data = [0,-2.84,-1.74,-3.15,0,0,0,0,-0.99,-0.98]
data.sort()

fig = pyplot.figure()
ax = fig.add_subplot(111)

ax.set_ylabel('Topic Log Odds', fontsize =20)
ax.set_ylim(bottom=-5,top=0)
ax.yaxis.grid()

bp = ax.boxplot(data, patch_artist=True)

for median in bp['medians']:
    median.set(color='#000000')

for box in bp['boxes']:
    box.set(facecolor = '#b2ccf7')
ax.set_xticklabels([''])
fig.savefig('boxplot.png')
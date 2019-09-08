# Some windroses
 
# IEM example: https://github.com/akrherz/iem/blob/e9cd3d7adf671a399fdeca94d0a2d96c533ffea7/htdocs/plotting/auto/scripts/p16.py

from pandas import *
import csv
import numpy
import numpy.ma as ma
from windrose import WindroseAxes
from matplotlib import pyplot
import matplotlib.cm as cm
import pylab
from matplotlib.patches import Rectangle

spfl = 'WindSp.csv'
f = open(spfl)
csv_f = csv.reader(f)
ctr = 0
for rw in csv_f:
    if ctr == 0:
        stns = rw
        nstns = len(rw)
        dtlst = [None] * len(stns)
        for j in range(nstns):
            dtlst[j] = []
    else:
        for j in range(nstns):
            if rw[j] == 'M':
                dtlst[j].append(None)
            elif rw[j] != '':
                dtlst[j].append(float(rw[j]))
    ctr = ctr + 1
f.close()

print(stns)
for j in range(nstns):
    print(len(dtlst[j]))


spfl = 'WindDir.csv'
f = open(spfl)
csv_f = csv.reader(f)
ctr = 0
for rw in csv_f:
    if ctr == 0:
        stns = rw
        nstns = len(rw)
        dtlst2 = [None] * len(stns)
        for j in range(nstns):
            dtlst2[j] = []
    else:
        for j in range(nstns):
            if rw[j] == 'M':
                dtlst2[j].append(None)
            elif rw[j] != '':
                dtlst2[j].append(float(rw[j]))
    ctr = ctr + 1
f.close()

print(stns)
for j in range(nstns):
    print(len(dtlst2[j]))

# Try some data arrays
for j in range(nstns):
    if (len(dtlst[j]) != len(dtlst2[j])):
        str1 = '%s does not have matching sizes for speed (%d) and direction (%d)' % (stns[j],len(dtlst[j]),len(dtlst2[j]))
        print(str1)
    else:
        spdarr = numpy.asarray(dtlst[j])
        dirarr = numpy.asarray(dtlst2[j])

        # Data Frame
        wndfrm = pandas.DataFrame({'WindDir':dirarr, 'WindSpeed':spdarr})
        wndsb = wndfrm[ (wndfrm['WindDir'].notnull()) & (wndfrm['WindSpeed'].notnull())]
        print(numpy.amax(wndsb['WindSpeed']))

        # Speed Histogram
        bnsq = numpy.arange(0.0,54.0,3.0)
        fig = pyplot.figure(figsize=(7.5,6), facecolor='w', edgecolor='w')
        p1 = pyplot.subplot(1,1,1)
        n, bins, patches = pylab.hist(wndsb['WindSpeed'], bnsq, density=False, histtype='bar', \
                                      rwidth=1.0,color='#3333CC')
        p1.xaxis.grid(color='#777777',linestyle='dotted')
        p1.yaxis.grid(color='#777777',linestyle='dotted')
        p1.set_xlabel('Wind Speed',size=12)
        p1.set_ylabel('Count',size=12)
        for lb in p1.xaxis.get_ticklabels():
            lb.set_fontsize(11)
        for lb in p1.yaxis.get_ticklabels():
            lb.set_fontsize(11)
        tstr = '%s Wind Speed' % (stns[j])
        pyplot.title(tstr,size=14)
        pngnm = '%s_WindSpeedHist.png' % (stns[j])
        fig.savefig(pngnm,bbox_inches=0)
        pyplot.close()

        wndsb = wndsb[(wndsb['WindSpeed'] > 0)]
        # A Rose?
        fig = pyplot.figure(figsize=(7.5,6), facecolor='w', edgecolor='w')
        rect = [0.08, 0.1, 0.8, 0.8]
        ax = WindroseAxes(fig, rect, facecolor='w')
        fig.add_axes(ax)
        #ax.bar(wndsb['WindDir'],wndsb['WindSpeed'],normed=True,opening=0.8,edgecolor='white')
        #ax.set_legend()

        ax.bar(wndsb['WindDir'], wndsb['WindSpeed'],
               normed=True, bins=[0, 2, 5, 7, 10, 15, 20], opening=0.8,
               edgecolor='white', nsector=36)
        handles = []
        pctr = 0
        for p in ax.patches_list:
            color = p.get_facecolor()
            # Skip the first bin
            if pctr > 0:
                handles.append(Rectangle((0, 0), 0.1, 0.3,
                                         facecolor=color, edgecolor='black'))
            pctr = pctr + 1
        legend = fig.legend(handles,
                            ('2-5', '5-7', '7-10', '10-15', '15-20', '20+'),
                            loc=(0.75, 0.03), ncol=2,
                            title='Wind Speed',
                            mode=None, columnspacing=0.9, handletextpad=0.45)
        pyplot.setp(legend.get_texts(), fontsize=10)
        pyplot.gcf().text(0.5, 0.99, stns[j],
                       fontsize=14, ha='center', va='top')

        pngnm = '%s_WindRose.png' % (stns[j])
        fig.savefig(pngnm,bbox_inches=0)
        pyplot.close()


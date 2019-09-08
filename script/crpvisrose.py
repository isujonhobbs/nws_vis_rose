# Some visibility roses 
 
# IEM example: https://github.com/akrherz/iem/blob/e9cd3d7adf671a399fdeca94d0a2d96c533ffea7/htdocs/plotting/auto/scripts/p16.py

from pandas import *
import csv
import numpy
import numpy.ma as ma
from windrose import WindroseAxes
from matplotlib import pyplot
import matplotlib.cm as cm
import pylab
from matplotlib import colors
from matplotlib.patches import Rectangle

spfl = 'VisWindDir.csv'
f = open(spfl)
csv_f = csv.reader(f)
ctr = 0
for rw in csv_f:
    if ctr == 0:
        stns = []
        stnidx = []
        for k in range(len(rw)):
            if (rw[k] != ''):
                stns.append(rw[k])
                stnidx.append(k)
        nstns = len(stns)
        dtlst = [None] * len(stns)
        dtlst2 = [None] * len(stns)
        for j in range(nstns):
            dtlst[j] = []
            dtlst2[j] = []
    else:
        for j in range(nstns):
            if rw[stnidx[j]] == 'M':
                dtlst[j].append(None)
            elif rw[stnidx[j]] != '':
                dtlst[j].append(float(rw[stnidx[j]]))
            if rw[stnidx[j]+1] == 'M':
                dtlst2[j].append(None)
            elif rw[stnidx[j]+1] != '':
                dtlst2[j].append(float(rw[stnidx[j]+1]))
    ctr = ctr + 1
f.close()

print(stns)
for j in range(nstns):
    print(len(dtlst[j]))

print(stns)
for j in range(nstns):
    print(len(dtlst2[j]))

# Colormap
rdlst = ["#872010","#8F3027","#963F38","#9D4C47","#A35A56","#A96764","#AE7572", \
        "#B48280","#B8908E","#BC9D9C","#C0ABAA","#C4B8B8","#C6C6C6"]
rdmp = colors.LinearSegmentedColormap.from_list("RedGray",rdlst)

# Try some data arrays
for j in range(nstns):
    if (len(dtlst[j]) != len(dtlst2[j])):
        str1 = '%s does not have matching sizes for speed (%d) and direction (%d)' % (stns[j],len(dtlst[j]),len(dtlst2[j]))
        print(str1)
    else:
        dirarr = numpy.asarray(dtlst[j])
        visarr = numpy.asarray(dtlst2[j])

        # Data Frame
        wndfrm = pandas.DataFrame({'WindDir':dirarr, 'Visibility':visarr})
        wndsb = wndfrm[ (wndfrm['WindDir'].notnull()) & (wndfrm['Visibility'].notnull())]

        vistbl = wndsb['Visibility'].value_counts()
        vistbl = pandas.DataFrame(vistbl)
        print(vistbl.columns)
        #vistbl = vistbl.sort_values(by='index',ascending=True)
        # Reorder by vis
        #print(vistbl)
        #print(vistbl.index.values)
        visfrm = pandas.DataFrame({'Visibility':vistbl.index.values, 'Count':vistbl['Visibility']})
        print(visfrm.columns)
        print(visfrm.dtypes)
        visfrm = visfrm.sort_values(by='Visibility',ascending=True)
        print(visfrm)

        bsq = numpy.arange(visfrm.shape[0])
        bspt = numpy.arange(0,visfrm.shape[0],2)
        vscts = numpy.array(visfrm['Visibility'])
        # Bar Chart of Visibility
        #bnsq = numpy.arange(0.0,54.0,3.0)
        fig = pyplot.figure(figsize=(7.5,6), facecolor='w', edgecolor='w')
        p1 = pyplot.subplot(1,1,1)
        rct1 = p1.bar(bsq,visfrm['Count'],0.5,color='#3333CC')
        #p1.xaxis.grid(color='#777777',linestyle='dotted')
        p1.yaxis.grid(color='#777777',linestyle='dotted')
        p1.set_xlabel('Visibility',size=12)
        p1.set_ylabel('Count',size=12)
        p1.set_xticks(bspt)
        p1.set_xticklabels(vscts[bspt])
        for lb in p1.xaxis.get_ticklabels():
            lb.set_fontsize(11)
        for lb in p1.yaxis.get_ticklabels():
            lb.set_fontsize(11)
        tstr = '%s Visibility' % (stns[j])
        pyplot.title(tstr,size=14)
        pngnm = '%s_VisHist.png' % (stns[j])
        fig.savefig(pngnm,bbox_inches=0)
        pyplot.close()


        # A Rose?
        fig = pyplot.figure(figsize=(7.5,6), facecolor='w', edgecolor='w')
        rect = [0.08, 0.1, 0.8, 0.8]
        ax = WindroseAxes(fig, rect, facecolor='w')
        fig.add_axes(ax)

        ax.bar(wndsb['WindDir'], wndsb['Visibility'],
               normed=True, bins=[0, 0.3, 1.1, 2.1, 3.1, 4.1, 5.1], opening=0.8,
               edgecolor='white', nsector=18, cmap=rdmp)
#        ax.set_legend()
        handles = []
        for p in ax.patches_list:
            color = p.get_facecolor()
            handles.append(Rectangle((0, 0), 0.1, 0.3,
                           facecolor=color, edgecolor='black'))
        legend = fig.legend(handles,
                            ('< 0.5', '0.5-1.0', '1.0-2.0', '2.0-3.0', '3.0-4.0', '4.0-5.0', '> 5.0'),
                            loc=(0.75, 0.03), ncol=2,
                            title='Visibility',
                            mode=None, columnspacing=0.9, handletextpad=0.45)
        pyplot.setp(legend.get_texts(), fontsize=10)
        pyplot.gcf().text(0.5, 0.99, stns[j],
                       fontsize=14, ha='center', va='top')

        pngnm = '%s_VisRose.png' % (stns[j])
        fig.savefig(pngnm,bbox_inches=0)
        pyplot.close()


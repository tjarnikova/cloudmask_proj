from __future__ import division
import argparse
import h5py
import glob
from matplotlib import pyplot as plt
import site
site.addsitedir('../utilities')
from TJ_reproject import reproj_L1B
import planck
reload(planck)
from planck import planckInvert
from mpl_toolkits.basemap import Basemap
from matplotlib.colors import Normalize
from matplotlib import cm
import numpy as np
import textwrap


mask_name='MYD35_L2.A2015032.1320.006.2015033170551.h5'

with h5py.File(mask_name) as mask_name:
	maskVals=mask_name.select('Cloud_Mask')
maskVals=maskVals.get()
maskVals=maskVals[0,...] #get the first byte
maskout,landout=bitmap.getmask_zero(maskVals)
oceanvals=(landout==0)
cloudvals=np.logical_and(maskout==0,oceanvals)
cloudfrac=np.sum(cloudvals)/oceanvals.size
oceanfrac=np.sum(oceanvals)/landout.size

options={'fignum':1}
corner_plot=simplots(option_dict=options)
theMap=corner_plot.make_lambert()
x,y=theMap(theMeta['cornerlons'],theMeta['cornerlats'])
theMap.plot(x,y)
theFig=theMap.ax.figure
theFig.canvas.draw()
theTitle=theMap.ax.set_title('cloud frac: %5.3f, oceanfrac: %5.3f' % (cloudfrac,oceanfrac))
x,y=theTitle.get_position()
theSize=theTitle.get_fontsize()
y=y*1.12
theMatch=re.compile('^MYD35_L2.(.*).005.*')
topTitle=theMatch.match(theMeta['filename']).group(1)
topText=theMap.ax.text(x,y,'%s' % topTitle,transform=theMap.ax.transAxes,ha='center',fontsize=theSize)
title='map.png'
figname='%s/%s.png' % (plot_dir,title)
theFig.canvas.print_figure(figname,dpi=150)
process.command("firefox %s" % figname)


#plt.show()
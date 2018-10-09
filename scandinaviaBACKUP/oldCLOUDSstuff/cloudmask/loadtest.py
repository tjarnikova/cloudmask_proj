import h5py
import glob
import matplotlib.pyplot as plt
# from matplotlib import pyplot as plt
import site
site.addsitedir('../../src')
from TJ_reproject import reproj_L1B
from matplotlib.colors import Normalize
from matplotlib import cm
import numpy as np
from mpl_toolkits.basemap import Basemap

l1b_file,=glob.glob('MYD021KM.A2015033.2215.006.2015034173643.h5')
l1b_file=h5py.File(l1b_file)
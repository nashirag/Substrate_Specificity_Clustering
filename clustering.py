## HIERARCHICAL CLUSTERING OF SUBSTRATE ARRAY DATA ##
# @date_created: Thursday, October 14th, 2021
# @author: nashira grigg

# IMPORT NECESSARY PACKAGES
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from scipy.cluster.hierarchy import dendrogram, linkage, set_link_color_palette
import matplotlib.pyplot as plt
import glob
import random

# READ IN MATRICES
#Retrieve all files from file list
all_files = glob.glob("./matrices/*.csv")
alldata = []

#Reformat data into one dataframe for hierarchy analysis
for filename in all_files:
    df = pd.read_csv(filename, index_col='Seq')
    name = []
    data = []
    columns = list(df)
    rows = list(df.index)
    c = 0
    r = 0
    for i in rows: 
        for j in columns:
            name.append(i + '-' + j)
            data.append(df.iloc[r][c])
            c += 1
        c = 0
        r += 1
    alldata.append(data)

#Insert all data into one dataframe
finalData = pd.DataFrame(alldata, columns = name, index = [s.strip('/Round 10.csv') for s in all_files])

#Generate random data for comparison
ncol = len(finalData.columns)
allrands = []
n = 0

while n < 1:
    rands = []
    i = 0
    while i < ncol:
        rands.append(random.uniform(min(finalData.min()), max(finalData.max())))
        i += 1
    allrands.append(rands)
    n += 1

ar = pd.DataFrame(allrands, columns=finalData.columns)
ar.index = ['Random']

finalData = finalData.append(ar)

all_features = finalData


# RUN WARD LINKAGE ON DATA
Z = linkage(all_features, 'ward')

# SET UP GRAPH FUNCTION OF DENDROGRAM FOR OUR LINKAGE
def fancy_dendrogram(*args, **kwargs):
    max_d = kwargs.pop('max_d', None)
    annotate_above = kwargs.pop('annotate_above', 0)

    ddata = dendrogram(*args, **kwargs)
    set_link_color_palette(None)
    
    if not kwargs.get('no_plot', False):
        plt.xlabel('Squared Euclidean Distance')
        for i, d, c in zip(ddata['icoord'], ddata['dcoord'], ddata['color_list']):
            x = 0.5 * sum(i[1:3])
            y = d[1]
            if y > annotate_above:
                plt.plot(y, x, 'o', c=c)
                (print(c))
                plt.annotate("%.3g" % y, (y, x), xytext=(-14, 13),
                             textcoords='offset points',
                             va='top', ha='center')
        if max_d:
            plt.axhline(y=max_d, c='k')
        
        plt.xlim([190, 0])
        plt.savefig("./matrices/substrate_hclust_ward.pdf", bbox_inches='tight', pad_inches=0.5)
    return ddata
    
    
# GRAPH OUR RESULTS
fancy_dendrogram(Z, truncate_mode='lastp', p=12, leaf_rotation=0., leaf_font_size=12., show_contracted=True, annotate_above=0, labels=all_features.index, orientation="left", color_threshold = 11)

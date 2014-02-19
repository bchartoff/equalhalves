import csv
from mpl_toolkits.basemap import Basemap, shiftgrid, cm
import numpy as np
import matplotlib.pyplot as plt

# create the figure and axes instances.
fig = plt.figure()
ax = fig.add_axes([0.1,0.1,0.8,0.8])
#setup base map
m = Basemap(llcrnrlon=-123.4,llcrnrlat=21.77,urcrnrlon=-54.55,urcrnrlat=48.79,\
            rsphere=(6378137.00,6356752.3142),\
            resolution='l',area_thresh=1000.,projection='lcc',\
            lat_1=50.,lon_0=-107.,ax=ax)
# transform to nx x ny regularly spaced 5km native projection grid
nx = int((m.xmax-m.xmin)/5000.)+1; ny = int((m.ymax-m.ymin)/5000.)+1
# draw coastlines and political boundaries.
m.drawcoastlines()
m.drawcountries()
m.drawstates()

#plot lines dividing country in 1/2
data = csv.reader(open("output.csv","rU"))
head = data.next()
for row in data:
	x, y = m([float(row[1]),float(row[3])],[float(row[0]),float(row[2])])
	m.plot(x, y, 'D-', markersize=1, linewidth=.5, color='r', markerfacecolor='b')

#set title and save graph
ax.set_title('Lines Dividing USA population in half')
plt.savefig('output.png',dpi=75)
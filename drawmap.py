import csv
from greatcircles import *
from mpl_toolkits.basemap import Basemap, shiftgrid, cm
import numpy as np
import matplotlib.pyplot as plt



def drawmap(m,outfile,title):
	# create the figure and axes instances.
	fig = plt.figure()
	ax = fig.add_axes([0.1,0.1,0.8,0.8])
	#setup base map, mercator projection (lat/long lines are straight)
	# transform to nx x ny regularly spaced 5km native projection grid
	nx = int((m.xmax-m.xmin)/5000.)+1; ny = int((m.ymax-m.ymin)/5000.)+1

	# draw coastlines and political boundaries.
	m.drawcoastlines()
	m.drawcountries()
	m.drawstates()

	# plot lines dividing country in 1/2
	data = csv.reader(open("output.csv","rU"))
	head = data.next()

	for row in data:
		try:
			lon1 = float(row[1])
			lon2 = float(row[3])
			lat1 = float(row[0])
			lat2 = float(row[2])
		except:
			pass
		#get great circle from calculated endpoints in output
		inCircle = Greatcircle(lat2,lon2,lat1,lon1)

		#extend great cirlce to the right and left by calculating it's intersection with 2
		#other great circles, at fixed longitudes (vertical lines on mercator projection)
		rightCircle = Greatcircle(0.,-60,10.,-60.)
		leftCircle = Greatcircle(0.,-130.,10.,-130.)

		right_coords = intersection(inCircle,rightCircle)
		left_coords = intersection(inCircle,leftCircle)

		try:
			if lon1<lon2:
				#m.drawgreatcircle(lon2,lat2,-60.,right_coords[0], linewidth=.5, color='b', alpha = 1)
				m.drawgreatcircle(-130.,left_coords[0],lon2,lat2, linewidth=.5, color='b', alpha = 1)

			else:
				#m.drawgreatcircle(lon1,lat1,-60.,right_coords[0], linewidth=.5, color='b', alpha = 1)
				m.drawgreatcircle(-130.,left_coords[0],lon1,lat1, linewidth=.5, color='b', alpha = 1)
			m.drawgreatcircle(lon1,lat1,lon2,lat2,linewidth=.5, color='r')
		except:
			pass

	#set title and save graph
	ax.set_title(title)
	plt.savefig(outfile,dpi=75)

#lambert conformal conical map is most familiar N American projection, great circles are curves
lcc = Basemap(llcrnrlon=-124.5,llcrnrlat=20.,urcrnrlon=-54.566,urcrnrlat=48.352,\
            rsphere=(6378137.00,6356752.3142),\
            resolution='l',area_thresh=1000.,projection='lcc',\
            lat_1=50.,lon_0=-107.)

#gnomic projection appears skewed, but great circles are drawn as straight lines
gnom = Basemap(llcrnrlon=-110.4,llcrnrlat=24.2,urcrnrlon=-54.55,urcrnrlat=48.79,\
           	projection='gnom',\
            lat_0=90.,lon_0=-90.)

#draw both maps and save to png
drawmap(lcc,"lcc.png","Great Circles Evenly Dividing US Population\nLambert Conformal Conical Projection")
drawmap(gnom,"gnom.png","Great Circles Evenly Dividing US Population\nGnomic Projection")
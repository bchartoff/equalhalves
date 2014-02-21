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

		for lon in [[-130,-101,'b'],[-101,-93,'b'],[-93,-87,'b'],[-87,-80,'b'],[-80,-60,'b']]:
			#draw great circles arcs staggered like so. Drawing a single arc between the l/r endpoints
			#encounters problems w/ basemap, which will not draw great circles which circle the globe and
			#return -- to be fixed w/ a more elegant solution (in the intersection function?)
			rightCircle = Greatcircle(0.,lon[0],10.,lon[0])
			leftCircle = Greatcircle(0.,lon[1],10.,lon[1])
			right_coords = intersection(inCircle,rightCircle)
			left_coords = intersection(inCircle,leftCircle)
			m.drawgreatcircle(left_coords[1],left_coords[0],right_coords[1],right_coords[0],linewidth=.2, color=lon[2])
		#draw median center of population, found here
		# https://www.census.gov/newsroom/releases/archives/facts_for_features_special_editions/cb11ff10.html
		m.plot(-87.410365,38.472967, latlon=True,marker='o',color='r')


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
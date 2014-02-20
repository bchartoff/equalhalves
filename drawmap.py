import csv
import math
from mpl_toolkits.basemap import Basemap, shiftgrid, cm
import numpy as np
import matplotlib.pyplot as plt


class Greatcircle:
	def __init__(self,lat1,lon1,lat2,lon2):
		dlat = math.radians(lat2-lat1)
		dlon = math.radians(lon2-lon1)
		self.lat1 = math.radians(lat1)
		self.lat2 = math.radians(lat2)
		self.lon1 = math.radians(lon1)
		self.lon2 = math.radians(lon2)

		y = math.sin(dlon)*math.cos(self.lat2)
		x = (math.cos(self.lat1)*math.sin(self.lat2))-(math.sin(self.lat1)*math.cos(self.lat2)*math.cos(dlon))
		self.bearing = (math.degrees(math.atan2(y,x))+360)%360


# test = Greatcircle(-12,-15,2,12)

# print "lat1 " +str(math.degrees(test.lat1))
# print "bearing " +str(test.bearing)

def intersection(circle1, circle2):
	lat1 = circle1.lat1
	lat2 = circle2.lat1
	lon1 = circle1.lon1
	lon2 = circle2.lon2
	b13 =  math.radians(circle1.bearing)
	b23 =  math.radians(circle2.bearing)

	dlat = lat2-lat1
	dlon = lon2-lon1

  	dist12 = 2*math.asin(math.sqrt(math.sin(dlat/2)*math.sin(dlat/2) + \
    math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)*math.sin(dlon/2)))

	bA = math.acos( ( math.sin(lat2) - math.sin(lat1)*math.cos(dist12) ) /\
	( math.sin(dist12)*math.cos(lat1) ) )
	
	bB = math.acos( ( math.sin(lat1) - math.sin(lat2)*math.cos(dist12) ) /\
	( math.sin(dist12)*math.cos(lat2) ) );

	if math.sin(lon2-lon1) > 0:
		b12 = bA
		b21 = 2*math.pi - bB
	else:
		b12 = 2*math.pi - bA;
		b21 = bB

	alpha1 = (b13 - b12 + math.pi) % (2*math.pi) - math.pi  # angle 2-1-3
	alpha2 = (b21 - b23 + math.pi) % (2*math.pi) - math.pi  # angle 1-2-3

	alpha3 = math.acos(-1*math.cos(alpha1)*math.cos(alpha2) + \
	math.sin(alpha1)*math.sin(alpha2)*math.cos(dist12) )

	dist13 = math.atan2( math.sin(dist12)*math.sin(alpha1)*math.sin(alpha2), \
	math.cos(alpha2)+math.cos(alpha1)*math.cos(alpha3) )

	lat3 = math.asin( math.sin(lat1)*math.cos(dist13) + \
	math.cos(lat1)*math.sin(dist13)*math.cos(b13) )

	dLon13 = math.atan2( math.sin(b13)*math.sin(dist13)*math.cos(lat1), \
	math.cos(dist13)-math.sin(lat1)*math.sin(lat3) )

	lon3 = lon1+dLon13

	lon3 = (lon3+3*math.pi) % (2*math.pi) - math.pi # normalise to -180..+180

	return [math.degrees(lat3),math.degrees(lon3)]



  


  

 # def fromvec(x,y,z,radius):
 #        float lat = (float)Math.Acos(position.Y / sphereRadius); //theta
 #        float lon = (float)Math.Atan(position.X / position.Z); //phi
 #        return new LatLon(lat, lon);


# create the figure and axes instances.
fig = plt.figure()
ax = fig.add_axes([0.1,0.1,0.8,0.8])
#setup base map
m = Basemap(llcrnrlon=-130.4,llcrnrlat=21.77,urcrnrlon=-54.55,urcrnrlat=48.79,\
           	projection='merc',\
            lat_0=90.,lon_0=-90.)
# transform to nx x ny regularly spaced 5km native projection grid
nx = int((m.xmax-m.xmin)/5000.)+1; ny = int((m.ymax-m.ymin)/5000.)+1
# draw coastlines and political boundaries.
m.drawcoastlines()
m.drawcountries()
m.drawstates()

#plot lines dividing country in 1/2
data = csv.reader(open("output.csv","rU"))
head = data.next()

edges,junk = m([-80.,-170.],[0,0])
for row in data:
	lon1 = float(row[1])
	lon2 = float(row[3])
	lat1 = float(row[0])
	lat2 = float(row[2])

	inCircle = Greatcircle(lat2,lon2,lat1,lon1)
	rightCircle = Greatcircle(0.,-70,10.,-70.)
	rightCircle2 = Greatcircle(0.,-80,10.,-80.)

	leftCircle = Greatcircle(0.,-130.,10.,-130.)

	right_coords2 = intersection(inCircle,rightCircle2)
	right_coords = intersection(inCircle,rightCircle)
	left_coords = intersection(leftCircle,inCircle)


	try:
		if lon1>lon2:
			m.drawgreatcircle(-70.,right_coords[0],lon2,lat2, linewidth=4, color='b', alpha = .05,markerfacecolor='b')
			#m.drawgreatcircle(-80.,right_coords2[0],lon2,lat2, linewidth=.25, color='b', markerfacecolor='b')
		else:
			m.drawgreatcircle(-70.,right_coords[0],lon1,lat1, linewidth=4, color='b', alpha = .05,markerfacecolor='b')

		if lon1<lon2:
			m.drawgreatcircle(-130.,left_coords[0],lon2,lat2, linewidth=4, color='b', alpha = .05,markerfacecolor='b')
			#m.drawgreatcircle(-80.,right_coords2[0],lon2,lat2, linewidth=.25, color='b', markerfacecolor='b')
		else:
			m.drawgreatcircle(-130.,left_coords[0],lon1,lat1, linewidth=4, color='b', alpha = .05,markerfacecolor='b')
			#m.drawgreatcircle(-80.,right_coords2[0],lon1,lat1, linewidth=.25, color='b', markerfacecolor='b')
		#m.drawgreatcircle(-120,left_coords[0],lon1,lat1, linewidth=.5, color='r', markerfacecolor='b')
		#m.drawgreatcircle(lon2,lat2,lon1,lat1,linewidth=.25, color='r', markerfacecolor='b')
	except:
		pass
	#calculate intersections w/ bounding box, to extend lines to edge of map
	# y1 = ((y2-y1)/(x2-x1))*21.77-x1+y1
	# x1 = 21.77
	# y2 = ((y2-y1)/(x2-x1))*48.79-x1+y1
	# x2 = 48.79
	# x1 = x[0]-100000
	# print x1
	# x2 = x[1]+100000
	# y1 = y[0]-100000
	# y2 = y[1]+100000
	# # ytemp = (((y2-y1)/(x2-x1))*(edges[0]-y1))+y1
	# # y2 = (((y2-y1)/(x2-x1))*(edges[1]-y1))+y1
	# # y1 = ytemp
	# # x1 = edges[0]

	# # x2 = edges[1]


	# x, y = [x1,x2],[y1,y2]
	# m.plot(x, y, 'D-', markersize=1, linewidth=.5, color='r', markerfacecolor='b')

#set title and save graph
ax.set_title('Lines Dividing USA population in half')
plt.savefig('output.png',dpi=75)
import math

#################
# great cirlce calculation functions from http://www.movable-type.co.uk/scripts/latlong.html
##################

#radius of Earth in km
R = 6371

class Greatcircle:
	def __init__(self,lat1,lon1,lat2,lon2):
		#create a great circle which runs through 2 points w/ known lat/lon
		dlat = math.radians(lat2-lat1)
		dlon = math.radians(lon2-lon1)
		self.lat1 = math.radians(lat1)
		self.lat2 = math.radians(lat2)
		self.lon1 = math.radians(lon1)
		self.lon2 = math.radians(lon2)

		#calculate initial bearing from pt1 to pt2 (in degrees) along great circle
		y = math.sin(dlon)*math.cos(self.lat2)
		x = (math.cos(self.lat1)*math.sin(self.lat2))-(math.sin(self.lat1)*math.cos(self.lat2)*math.cos(dlon))
		self.bearing = (math.degrees(math.atan2(y,x))+360)%360

		#calculate length of great circle between pt1 and pt2
		a = math.sin(dlat/2)*math.sin(dlat/2)+\
		math.sin(dlon/2)*math.sin(dlon/2)*math.cos(self.lat1)*math.cos(self.lat2)
		c = 2*math.atan2(math.sqrt(a),math.sqrt(1-a))
		self.length = R*c


def crosstrack(circle,lat3,lon3):
	#calc distance from third point to a given great circle
	#sign of distance used to determine which side of circle points lie on in calculation.py
	circle13 = Greatcircle(math.degrees(circle.lat1),math.degrees(circle.lon1),lat3,lon3)
	d13 = circle13.length
	b13 = math.radians(circle13.bearing)
	b12 = math.radians(circle.bearing)

	return math.asin(math.sin(d13/R)*math.sin(b13-b12)) * R


def intersection(circle1, circle2):
	#calc intersection point of two great circles
	#used in drawmap.py to extend circles to fixed longitudes
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


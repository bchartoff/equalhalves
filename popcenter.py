import csv
from greatcircles import *

data = csv.reader(open("data.csv","rU"))
head = data.next()

out.writerow(["Lat1","Long1","Lat2","Long2","Pop_left","Pop_right","Percent_left","Percent_right"])


lats = []
longs = []
pops = []

for row in data:
	#from census data, find coords and populations of census block centers of population
	lats.append(float(row[5]))
	longs.append(float(row[6]))
	pops.append(float(row[4]))

def mediancenter:
	for i in range(0,len(lats)):
		

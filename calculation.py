import csv
from random import randint
from greatcircles import *

data = csv.reader(open("data.csv","rU"))
out = csv.writer(open("output.csv","wb"))

head = data.next()
out.writerow(["Lat1","Long1","Lat2","Long2","Pop_left","Pop_right","Percent_left","Percent_right"])


lats = []
longs = []
pops = []
lats_round = []
longs_round = []

for row in data:
	#from census data, find coords and populations of census block centers of population
	lats.append(float(row[5]))
	longs.append(float(row[6]))
	pops.append(float(row[4]))

	#populate list of points to draw great circles through. Round to nearest .1 so that pop centers don't fall exactly on lines
	lats_round.append(round(float(row[5]),1))
	longs_round.append(round(float(row[6]),1))

for loopcount in range(0,10000):
	print loopcount
	left_total = 0.
	right_total = 0.

	#pick two random points w/in the US to draw a great circle through
	n1 = 0
	n2 = 0
	while True:
		n1 = randint(0,len(lats)-1)
		n2 = randint(0,len(lats)-1)
		#ensure uniqueness of points
		if n1 == n2:
			continue
		else:
			break

	#create a circle to test
	testCircle = Greatcircle(lats_round[n1],longs_round[n1],lats_round[n2],longs_round[n2])

	for i in range(0,len(lats)):	
		#for each center of population, determine if it lies to the left or right of the circle,
		#and increment the appropriate population total
		if crosstrack(testCircle,lats[i],longs[i]) < 0:
			right_total += pops[i]
		else:
			left_total += pops[i]
	#write to file lines for which division is close to 50/50
	total_pop = left_total+right_total
	percent_left = left_total/total_pop
	percent_right = right_total/total_pop

	if abs(percent_right - percent_left) <= .01:
		out.writerow([lats_round[n1],longs_round[n1],lats_round[n2],longs_round[n2],left_total,right_total,percent_left,percent_right])
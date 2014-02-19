import csv
from random import randint

data = csv.reader(open("data.csv","rU"))
out = csv.writer(open("output.csv","wb"))

head = data.next()
out.writerow(["Lat1","Long1","Lat2","Long2","Pop_left","Pop_right","Percent_left","Percent_right"])

class Line:
	x1 = 0
	y1 = 0
	x2 = 0
	y2 = 0
	m = 0
	#Find slope of line based on two points
	def __init__(self,x1,y1,x2,y2):
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2
		self.m = (y1-y2)/(x1-x2)
	def xint(self,y):
		#eqn of line: y-y1 = m(x-x1), rearrange to solve for x w/ given y
		return (y-self.y1+self.m*self.x1)/self.m


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

	#populate list of points to draw lines through. Round to nearest .1 so that pop centers don't fall exactly on lines
	lats_round.append(round(float(row[5]),1))
	longs_round.append(round(float(row[6]),1))

for loopcount in range(0,10000):
	left_total = 0.
	right_total = 0.

	#pick two random points w/in the US to draw a line through
	n1 = 0
	n2 = 0
	while True:
		n1 = randint(0,len(lats)-1)
		n2 = randint(0,len(lats)-1)
		#prevent division by 0 errors for slope calcs
		if lats_round[n1] == lats_round[n2]:
			continue
		else:
			break

	
	line = Line(lats_round[n1],longs_round[n1],lats_round[n2],longs_round[n2])


	for i in range(0,len(lats)):
		#handle horizontal lines
		if line.m == 0:
			if lats[i] > line.y1:
				right_total += pops[i]
			else:
				left_total += pops[i]
		else:
			#for each center of population, determine if it lies to the left or right of the line, and increment the appropriate population total
			if line.xint(longs[i]) - lats[i] < 0:
				right_total += pops[i]
			else:
				left_total += pops[i]
	#write to file lines for which division is close to 50/50
	total_pop = left_total+right_total
	percent_left = left_total/total_pop
	percent_right = right_total/total_pop

	if abs(percent_right - percent_left) <= .01:
		out.writerow([lats_round[n1],longs_round[n1],lats_round[n2],longs_round[n2],left_total,right_total,percent_left,percent_right])



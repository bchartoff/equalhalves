Equalhalves
==========

Calculate great circles which split US population into equal halves and map them.

Data source is US Census 2010 centers of population by block group

https://www.census.gov/geo/reference/centersofpop.html

152 great circles calculated from 10,000 randomly chosen arcs (with anchor points near centers of population)

The red dot represents the 2010 median center of population, which is the point of intersection of 2 perpendicular lines (N-S and E-W) which divide the population in half.

https://www.census.gov/newsroom/releases/archives/facts_for_features_special_editions/cb11ff10.html

Map drawn w/ Python's basemap package

lcc.png shows one of the most familiar N. American projection, the lambert conformal conical projection.

gnom.png shows the gnomic projection, on which great circles are represented as straight lines.
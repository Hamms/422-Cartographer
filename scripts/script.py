import sys, math
from xml.dom.minidom import parse, parseString

class TrackSimplifier:
	
	# This is the maximum change in angle before we start a new path
	# We may want to consider an method which considers a history of the change in angle...
	threshold = 45.0

	def __init__(self):
		self.path = Path()
		self.paths = [self.path]
		self.prevPoint = False
		self.prevDir = False
	
	def insertPoint(self, point):
		cur = GPXPoint(point)
		print cur.time

		# Initialize newPath for proper scoping
		newPath = False

		# If we have a previous point, calculate a direction
		if self.prevPoint:
			direction = calculateDirection(cur, self.prevPoint)
			# If we have a previous direction, check against our threshold
			if self.prevDir:
				diff = math.fabs(direction - self.prevDir)

				# Hack! - this will ignore backwards directions within the threshold.  We should find a better way to solve this.
				# Todo: Fix this hack
				if diff > self.threshold and diff < (360 - self.threshold):
					print "!",
					newPath = True
				print diff

			self.prevDir = direction
		
		if newPath: 
			# Start a new path, store the old one
			self.path = Path()
			self.paths.append(self.path)

		# Add this point to our path
		self.path.addPoint(cur)
		self.prevPoint = cur

	def info(self):
		print "paths:",len(self.paths)


# A GPXPoint is a latitude/longitude object
class GPXPoint:
	def __init__(self, point):
		lat = point.getAttribute("lat")
		lon = point.getAttribute("lon")
		
		children = point.childNodes
		time = 0

		for child in children:
			if child.nodeName == "time":
				time = child.childNodes[0].nodeValue
				break;
				
		self.lat = lat
		self.lon = lon
		self.time = time
		self.XMLNode = point

	def __str__(self):
		return "lat: " + self.lat + ", lon: " + self.lon
	
	# Return a pair of points converted into floating point numbers
	def getPos(self):
		return (float(self.lon), float(self.lat))


# A path is a group of points which do not include any change in direction
class Path:
	def __init__(self):
		# Todo: Keys are not implemented yet - they are intended to be notable points which we can draw our simplified path with
		self.keys = []
		self.points = []
	
	def finishPath():
		# todo: something here
		return
	
	def addPoint(self, point):
		# Add a new point.
		self.points.append(point)

		# Todo: Determine if this point should be a new key
		if len(self.keys) == 0:
			self.keys.append(point)


# Calculate the direction defined by two points, travelling from p1 to p2
# returns an angle from -180 to 180 degrees, where 0 is north, 90 is east, 180 is south, and -90 is west
def calculateDirection(p1, p2):
	(x1, y1), (x2, y2) = p1.getPos(), p2.getPos()
	# calculate in radians, then translate to degrees
	radians = math.atan2(y2-y1, x2-x1)
	degrees = math.degrees(radians)
	return degrees


def processFile(filename):
	print "Processing file", filename, "\n"
	dom = parse(filename)
	segments = dom.getElementsByTagName("trkseg")
	print len(segments), "segments to process"

	for seg in segments:
		points = seg.childNodes
		simplifier = TrackSimplifier()

		print "\n", "Processing new segment"
		print len(points), "points in this segment"
		for point in points:
			if point.nodeName == "trkpt":

				simplifier.insertPoint(point)
		print "There were", len(simplifier.paths), "paths in this segment"


usage = """FILENAME"""

def main(args):
	if len(args) < 2:
		sys.stderr.write("USAGE: Python " + args[0] + " " + usage)
		sys.exit(1)

	inputFile = args[1]
	processFile(inputFile)

if __name__ == "__main__":
	main(sys.argv)

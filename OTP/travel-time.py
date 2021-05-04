#!/usr/bin/jython

from org.opentripplanner.scripting.api import * 
otp = OtpsEntryPoint.fromArgs([ "--graphs", "/Users/bahman/Dropbox (Sydney Uni)/Bahman/3 way estimating OD/Calculation/OTP/graphs", "--router", "current"])


# Start timing the code
import time
start_time = time.time()

# Get the default router
router = otp.getRouter() 					#The default router. If there is one router, this will be the default.

# Create a default request for a given time
req = otp.createRequest()					# a new plan request that can be used to plan route / shortest path tree on a router.
req.setDateTime(2019, 7, 22, 8, 00, 00)		# set arrival/departure time
# req.setArriveBy(False)					# whether the trip should depart at dateTime (false, the default), or arrive at dateTime.
req.setMaxTimeSec(18000) 					# set a limit to maximum travel time (seconds)
req.setModes('WALK,TRANSIT')				# define transport mode: WALK,BUS,RAIL
req.clampInitialWait = 600 					# maximum wait time in seconds the user is willing to delay trip start
#req.maxWalkDistance = 1000            		# set the maximum distance (in meters) the user is willing to walk.Defaults to unlimited.
# req.walkSpeed = walkSpeed                 # set average walking speed ( meters/sec)
# req.setMaxTransfers(3)					# set maximum transfer in one journey
# ?ERROR req.setSearchRadiusM(500)          # set max snapping distance to connect trip origin to street network
 
# for more routing options, check: http://dev.opentripplanner.org/javadoc/0.19.0/org/opentripplanner/scripting/api/OtpsRoutingRequest.html



# Read Coordinates of Origins & Destinations - The file points.csv contains the columns stop_name, stop_lat and stop_lon.

origins = otp.loadCSVPopulation('points.csv', 'stop_lat', 'stop_lon')
destinations = otp.loadCSVPopulation('points.csv', 'stop_lat', 'stop_lon')

# Create a CSV output
matrixCsv = otp.createCSVOutput()
matrixCsv.setHeader([ 'origin', 'destination', 'walk_distance', 'travel_time', 'boarding','individual' ])


# Start Loop
for origin in origins:
			req.setOrigin(origin)				# set origin for for evaluating the SPT at a given point.
			spt = router.plan(req)				# A shortest-path-tree, the result of a plan request on a router.
			if spt is None: continue
			# Evaluate the SPT for all points
  			result = spt.eval(destinations)		#The evualuated value, or NULL if no evaluation can be done (out of range, non snappable).
			# Add a new row of result in the CSV output
			for r in result:
   				matrixCsv.addRow([ origin.getStringData('stop_name'), r.getIndividual().getStringData('stop_name'), r.getWalkDistance() , r.getTime(),  r.getBoardings(), r.getIndividual() ])

# Notice:
# getTime returns the time, in seconds, for this evualuated individual. Return null/None if no time is available (position not snapped or out of time range)
# getBoardings returns the number of boardings to get to this point (this is the number of transfers +1). Return 0 for walk only path. Return null/None if no information is available at this point (position not snapped or out of evaluated time range).
# getWalkDistance returns The distance in meters walked to get to this point. Return null/None if no information is available at this point.
# getIndividual: The individual evaluated (the same individual from the evuluated population).

# Save the result
matrixCsv.save('traveltime_matrix.csv')

# Stop timing the code
print("Elapsed time was %g seconds" % (time.time() - start_time))

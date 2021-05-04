import googlemaps #visit for more info		 https://github.com/googlemaps/google-maps-services-python/blob/master/googlemaps/distance_matrix.py
from datetime import datetime
import pandas as pd
from itertools import tee
import json


#Read CSV file into data frame named 'df'
#change seperator (sep e.g. ',') type if necessary
df = pd.read_csv('points.csv')

#Perform request to use the Google Maps API web service
API_key = 'AIza.....'		#enter Google Maps API key
gmaps = googlemaps.Client(key=API_key)

#specify the departure time
d_t = datetime(2019,7,22,8,00,00,00)
# Creating an empty Dataframe with column names only
travel_time = pd.DataFrame(columns=['From', 'To', 'Distance', 'Time'])


for index_i, row_i in df.iterrows():
	LatOrigin = row_i['stop_lat']
	LongOrigin = row_i['stop_lon']
	origin = (LatOrigin,LongOrigin)
	for index_j, row_j in df.iterrows():
		LatDestination = row_j['stop_lat']
		LongDestination = row_j['stop_lon']
		destination = (LatDestination,LongDestination)
		#pass origin and destination variables to distance_matrix function# output in meters
		#mode=None, language=None, avoid=None, units=None, departure_time=None, arrival_time=None, transit_mode=None, transit_routing_preference=None, traffic_model=None, region=None
		#duration is expressed in seconds, and distance is in meters
		result = gmaps.distance_matrix(origin, destination,region = 'au',departure_time= d_t, mode='transit',transit_mode='rail',units = 'metric')
		distance = result["rows"][0]["elements"][0]["distance"]["value"]
		duration = result["rows"][0]["elements"][0]["duration"]["value"]
		# Append rows in Empty Dataframe by adding dictionaries
		tt = pd.Series([row_i['stop_name'],row_j['stop_name'],distance,duration],index=['From', 'To', 'Distance', 'Time'])
		travel_time = travel_time.append(tt,ignore_index=True)

travel_time.to_csv('calculated_TT.csv', index=None, header= ['From', 'To', 'Distance', 'Time'])


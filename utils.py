import pandas as pd 
import requests
import numpy as np
import math
def get_osrm_distance(from_location:str, to_location:str, lat_lon_file:str, via_location:str=None):
    '''
        Function to calculate the osrm from one destination to another.
        Via is optional.
        The lat_lon_file should contain the latitudes and longitudes of the all locations.
    '''
    # Read the file with the latitudes and longitudes
    lat_lon = pd.read_csv(lat_lon_file)
    # Get the latitudes and longitudes of the from and to locations (and via if it exists)
    from_lat_lon = lat_lon[lat_lon['Destination'] == from_location]
    to_lat_lon = lat_lon[lat_lon['Destination'] == to_location]
    if via_location is not None:
        via_lat_lon = lat_lon[lat_lon['Destination'] == via_location]

    # Check if the locations exist
    if from_lat_lon.empty or to_lat_lon.empty:
        print('From or to location not found - update the lat_lon_file and try again')
        return 0
    
    # Get the latitudes and longitudes
    from_lat = from_lat_lon['Latitude'].values[0]
    from_lon = from_lat_lon['Longitude'].values[0]
    to_lat = to_lat_lon['Latitude'].values[0]
    to_lon = to_lat_lon['Longitude'].values[0]
    if via_location is not None:
        via_lat = via_lat_lon['Latitude'].values[0]
        via_lon = via_lat_lon['Longitude'].values[0]
    
    if via_location is not None:
        url = f"http://localhost:5000/route/v1/driving/{from_lon},{from_lat};{via_lon},{via_lat};{to_lon},{to_lat}?overview=false"
    else:
        url = f"http://localhost:5000/route/v1/driving/{from_lon},{from_lat};{to_lon},{to_lat}?overview=false"

    response = requests.get(url)

    data = response.json()

    if data['code'] == 'Ok':
        distance = data['routes'][0]['distance'] / 1000  # Convert meters to kilometers
        return distance
    else:
        print(f"Error fetching distance: {data['code']}")
        return 0


# # Test the function
# from_location = 'Aabybro'
# to_location = 'Esbjerg'
# via_location = 'Aalborg'
# lat_lon_file = 'national_destinations.csv'

# distance = get_osrm_distance(from_location, to_location, lat_lon_file, via_location)



def get_haversine_distance(from_location, to_location, lat_lon_file):
    '''
        Function to calculate the haversine distance between two locations
    '''
    lat_lon_file = pd.read_csv(lat_lon_file)
    
    lat1 = lat_lon_file[lat_lon_file['Destination'] == from_location]['Latitude'].values[0]
    lon1 = lat_lon_file[lat_lon_file['Destination'] == from_location]['Longitude'].values[0]

    lat2 = lat_lon_file[lat_lon_file['Destination'] == to_location]['Latitude'].values[0]
    lon2 = lat_lon_file[lat_lon_file['Destination'] == to_location]['Longitude'].values[0]
    
    R = 6371  # Radius of the Earth in kilometers
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = math.sin(d_lat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(d_lon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance


# Test the function
from_location = 'Aabybro'
to_location = 'Esbjerg'
via_location = 'Aalborg'
lat_lon_file = 'national_destinations.csv'

distance = get_haversine_distance(from_location, to_location, lat_lon_file)

print(f'Haversine distance: {distance:.2f} km')
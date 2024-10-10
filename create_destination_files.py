'''
                This script reads a .xlsx file with business travel data and extracts all unique destinations.
'''

import requests
import pandas as pd

# Load .xlsx file
FILE_PATH = 'csv/cleaned_BusinessTravels.xlsx'

national_travel = pd.read_excel(FILE_PATH, sheet_name='DK_BusinessTravels_clean')
international_travel = pd.read_excel(FILE_PATH, sheet_name='Abroad_BusinessTravels_clean')

# Go through all columns with 'from', 'to' or 'via' in the header
# and append all unique values to a list. Only from row 4 and down.
# 

# National travel
national_from_to_via_car = []
national_from_to_via_bus = []
national_from_to_via_train = []

for column in national_travel.columns:
    if 'from' in column.lower() or 'to' in column.lower() or 'via' in column.lower():
        if 'car' in column.lower():
            national_from_to_via_car.extend(national_travel[column].iloc[3:].unique())
        elif 'bus' in column.lower():
            national_from_to_via_bus.extend(national_travel[column].iloc[3:].unique())
        elif 'train' in column.lower():
            national_from_to_via_train.extend(national_travel[column].iloc[3:].unique())


# International travel
international_from_to_via_car = []
international_from_to_via_bus = []
international_from_to_via_train = []
international_from_to_via_plane = []

for column in international_travel.columns:
    if '_from' in column.lower() or '_to' in column.lower() or '_via' in column.lower():
        if 'car' in column.lower():
            international_from_to_via_car.extend(international_travel[column].iloc[3:].unique())
        elif 'bus' in column.lower():
            international_from_to_via_bus.extend(international_travel[column].iloc[3:].unique())
        elif 'train' in column.lower():
            international_from_to_via_train.extend(international_travel[column].iloc[3:].unique())
        elif 'plane' in column.lower():
            international_from_to_via_plane.extend(international_travel[column].iloc[3:].unique())

# Remove NaN values
national_from_to_via_car = [value for value in national_from_to_via_car if not pd.isnull(value)]
national_from_to_via_bus = [value for value in national_from_to_via_bus if not pd.isnull(value)]
national_from_to_via_train = [value for value in national_from_to_via_train if not pd.isnull(value)]

international_from_to_via_car = [value for value in international_from_to_via_car if not pd.isnull(value)]
international_from_to_via_bus = [value for value in international_from_to_via_bus if not pd.isnull(value)]
international_from_to_via_train = [value for value in international_from_to_via_train if not pd.isnull(value)]
international_from_to_via_plane = [value for value in international_from_to_via_plane if not pd.isnull(value)]

# Order all the strings alphabetically and remove duplicates
national_from_to_via_car = sorted(list(set(national_from_to_via_car)))
national_from_to_via_bus = sorted(list(set(national_from_to_via_bus)))
national_from_to_via_train = sorted(list(set(national_from_to_via_train)))

international_from_to_via_car = sorted(list(set(international_from_to_via_car)))
international_from_to_via_bus = sorted(list(set(international_from_to_via_bus)))
international_from_to_via_train = sorted(list(set(international_from_to_via_train)))
international_from_to_via_plane = sorted(list(set(international_from_to_via_plane)))

# print('#### NATIONAL TRAVEL ####')
# print('Car travel:')
# # Print car travel destinations, one per line
# for destination in national_from_to_via_car:
#     print('\t' + destination)
# print('\nBus travel:')
# for destination in national_from_to_via_bus:
#     print('\t' + destination)
# print('\nTrain travel:')
# for destination in national_from_to_via_train:
#     print('\t' + destination)

# print('\n\n#### INTERNATIONAL TRAVEL ####')
# print('Car travel:')
# # Print car travel destinations, one per line
# for destination in international_from_to_via_car:
#     print('\t' + destination)
# print('\nBus travel:')
# for destination in international_from_to_via_bus:
#     print('\t' + destination)
# print('\nTrain travel:')
# for destination in international_from_to_via_train:
#     print('\t' + destination)
# print('\nPlane travel:')
# for destination in international_from_to_via_plane:
#     print('\t' + destination)



# Make a list with all unique destinations and sort them alphabetically
international_all = sorted(list(set(international_from_to_via_car + international_from_to_via_bus + international_from_to_via_train + international_from_to_via_plane)))
national_all = sorted(list(set(national_from_to_via_car + national_from_to_via_bus + national_from_to_via_train)))

# print('\n\n#### ALL DESTINATIONS ####')
# print('National travel:')
# for destination in national_all:
#     print('\t' + destination)
# print('\nInternational travel:')
# for destination in international_all:
#     print('\t' + destination)



# Function to get coordinates for a location
def get_coordinates(location):
    url = f'https://nominatim.openstreetmap.org/search?q={location}&format=json'
    response = requests.get(url)
    data = response.json()
    if len(data) > 0:
        return data[0]['lat'], data[0]['lon']
    else:
        return None, None
    
# Get coordinates for all destinations
national_coordinates = {}
for destination in national_all:
    #print(f'Getting coordinates for {destination}')
    lat, lon = get_coordinates(destination)
    national_coordinates[destination] = (lat, lon)

international_coordinates = {}
for destination in international_all:
    #print(f'Getting coordinates for {destination}')
    lat, lon = get_coordinates(destination)
    international_coordinates[destination] = (lat, lon)

# # Print coordinates
# print('\n\n#### NATIONAL COORDINATES ####')
# for destination, coordinates in national_coordinates.items():
#     print(f'{destination}: {coordinates}')

# print('\n\n#### INTERNATIONAL COORDINATES ####')
# for destination, coordinates in international_coordinates.items():
#     print(f'{destination}: {coordinates}')

# Create a dataframe with all destinations and coordinates: Destination, Latitude, Longitude
national_destinations = pd.DataFrame(national_coordinates).T.reset_index()
national_destinations.columns = ['Destination', 'Latitude', 'Longitude']

international_destinations = pd.DataFrame(international_coordinates).T.reset_index()
international_destinations.columns = ['Destination', 'Latitude', 'Longitude']

# Print the dataframes
print(national_destinations)
print(international_destinations)


# Save the dataframes to .csv files
national_destinations.to_csv('national_destinations.csv', index=False)
international_destinations.to_csv('international_destinations.csv', index=False)

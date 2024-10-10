'''
    This script is used to calculate the emissions from international business travels.

    ToDo list:
        - Specify different emissions for different flight lengths
            - What should the cutoff be?
        - Incorporate emissions from stopovers 
            - Calculate flight distance. 
                - If distance > r_Europe, then stopover assumed to be in Frankfurt/Gatwick/??
                  Then one emission factor for the From-->Frankfurt and one factor for Frankfurt-->Destination + add on bc. of take-off/landing twice
                - If distance < r_Europe, stopover assumed to be halfway to destination and emission add on bc. of take-off/landing twice
                  
        - Check up on emission factors for different modes of transport
            - Electric car
            - Petrol
            - Train in DK
            - Train in Europe
            - Ferry (per km)
            - Flight in DK (per km)
            - Flight internationally (dependent on distance)
'''
import requests
import subprocess
import os
import time


import pandas as pd
from utils import get_haversine_distance, get_osrm_distance


# #####################
# #                   #   
# # SETUP OSRM SERVER #
# #                   #   
# #####################

# # Path to the OSRM server
# osm_data_folder = os.path.join(os.path.dirname(__file__), 'osm_denmark')

# # Function to check if OSRM server is running
# def is_osrm_running():
#     try:
#         response = requests.get("http://localhost:5000/health")
#         return response.status_code == 200
#     except requests.ConnectionError:
#         return False

# # Function to start the OSRM server 
# def start_osrm_server():
#     # Ensure the OSRM data folder exists
#     if not os.path.exists(osm_data_folder):
#         print(f"OSRM data folder not found: '{osm_data_folder}'")
#         return

#     # Command to start OSRM server using Docker
#     command = [
#         "docker", "run", "-t", "-i", "-p", "5000:5000",
#         "-v", f"{osm_data_folder}:/data", # Mount the data folder to /data in the container
#         "osrm/osrm-backend",
#         "osrm-routed", "/data/denmark-latest.osrm" # Update the path to match the new folder structure
#         ]

#     # Start the OSRM server in the background
#     try:
#         print("Starting OSRM server...")
#         subprocess.Popen(command) # Starts the server as a background process
#         print("OSRM server started successfully.")
#     except Exception as e:
#         print(f"Error starting OSRM server: {e}")



# # Use this function to alert if OSRM is not running
# if not is_osrm_running():
#     print("OSRM server is not running. Starting the server...")
#     start_osrm_server()
#     # Add a delay to allow the server to start
#     time.sleep(10)
# else:
#     # Proceed with your distance calculations
#     print("OSRM server is running. Ready to calculate distances.")

# The lat_lon_file should contain the latitudes and longitudes of the all locations.
lat_lon_file = 'csv/international_destinations.csv'






###################################
#                                 #
# SETUP EMISSION FACTORS AND DATA # 
#                                 #
###################################

# !! BASED ON COWI (https://www.dsb.dk/globalassets/om-dsb/baeredygtighed/miljo/sammenligning-af-emmisionsfaktorer_cowi-rapport-til-dsb_okt-2023.pdf)
# !! Need to verify the emission factors (talk with local AU ENVS Emission group)

# Fly - International + RFI (person.km) Scope 3. kg CO2e per person km
emission_factor_plane_per_km = 0.197423783892617
# Car - International + RFI (person.km) Scope 3. kg CO2e per person km
emission_factor_car_per_km = 0.243
# Train - International + RFI (person.km) Scope 3. kg CO2e per person km
emission_factor_train_per_km = 0.041
# Bus - International + RFI (person.km) Scope 3. kg CO2e per person km
emission_factor_bus_per_km = 0.027

# # Ferry (Odden<-->Ebeltoft), ~70 km (one way), 0.915 kg CO2e per person km (with car)
# emission_factor_ferry_one_way = 0.915 * 68.524
# # Plane (per passenger per one-way trip), average of Kbh<->Aalborg and Kbh<->Aarhus
# emission_factor_plane_one_way = (39.3 + 28.5) / 2



train_el_eu_part = 0.55 # 45% of the rail network is electrified in EU
train_diesel_eu_part = 0.45 # 55% of the rail network is diesel in EU

train_el_emission_factor = 0.041 # kg CO2e per km
train_diesel_emission_factor = 0.09 # kg CO2e per km

train_eu_average = train_el_emission_factor * train_el_eu_part + train_diesel_emission_factor * train_diesel_eu_part

petrol_car_emission_factor = 0.1779 # kg CO2e per km
electric_car_emission_factor = 0.0188 # kg CO2e per km

bus_long_distance_dk_emission_factor = 0.020 # kg CO2e per km
bus_long_distance_eu_emission_factor = 0.031 # kg CO2e per km

ferry_emission_factor = 0.915 # kg CO2e per km

short_haul_flight_emission_factor = 0.151 # kg CO2e per km. <1500 km
medium_haul_flight_emission_factor = 0.1495 # kg CO2e per km. 1500-3000 km
long_haul_flight_emission_factor = 0.148 # kg CO2e per km. >3000 km

# Define short/medium/long haul flight distances
short_haul_distance = 1500
medium_haul_distance = 3000
long_haul_distance = 5000





# Load .xlsx file
FILE_PATH = 'csv/cleaned_BusinessTravels.xlsx'

international_travel = pd.read_excel(FILE_PATH, sheet_name='Abroad_BusinessTravels_clean')






################################
#                              #
# FLIGHT TRAVELS AND EMISSIONS #
#                              #
################################

# Sheet contains Plane, Car driver, Car passenger, Train and Bus
# Plane has 'To' (assuming from Denmark), no. of stopovers and how many times
# Car driver and Car passenger have 'From' 'Via' and 'To' columns
# Train and Bus have 'From' and 'To' columns

# Build dfs for Plane, Car driver, Car passenger, Train and Bus
# Take all columns with 'plane' in the header and create new df
international_plane = international_travel[[column for column in international_travel.columns if 'plane' in column.lower()]]
# Remove the first column which is a question
international_plane = international_plane.iloc[:, 1:]
# Remove all rows with only NaN values and reset the index
international_plane = international_plane.dropna(how='all', axis=0).reset_index(drop=True)
# The rows are basically a repetition of the pattern '', '_from', '_to', '_via', '_times, so each 5th row is the start of a new travel

# Number of planes
num_planes = 6

# Reshape the dataframe
rows = []
for i in range(1, num_planes + 1):
    plane = f'plane_abroad_{i}'
    plane_to = f'{plane}_to'
    plane_stops = f'{plane}_stops'
    plane_times = f'{plane}_times'
    
    temp_df = international_plane[[plane, plane_to, plane_stops, plane_times]].copy()
    temp_df.columns = ['', 'to', 'stops', 'times']
    temp_df = temp_df.dropna(subset=['', 'to'], how='all').reset_index(drop=True)

    # Because 'times' is roundtrip, multiply by 2 to get one-way trip
    temp_df['times'] = pd.to_numeric(temp_df['times'], errors='coerce') * 2
    
    rows.append(temp_df)

# Concatenate all the reshaped dataframes
reshaped_df = pd.concat(rows, ignore_index=True)

# Remove all rows with a '-' sign anywhere in the row
reshaped_df = reshaped_df[~reshaped_df.apply(lambda x: x.str.contains('-').any(), axis=1)].reset_index(drop=True)

# Remove the first column
reshaped_df = reshaped_df.iloc[:, 1:]

# If 'stops' is NaN, set it to 0
reshaped_df['stops'] = reshaped_df['stops'].fillna(0)



# Use the Haversine function to caculate kms travelled by plane.
# Loop through the dataframe, compute the distance between locations,
# and multiply by number of times travelled.

# Add a new column 'Distance' to the dataframe
reshaped_df['distance'] = 0
for index, row in reshaped_df.iterrows():
    distance = get_haversine_distance('Kastrup', row['to'], 'csv/international_destinations.csv')
    reshaped_df.loc[index, 'distance'] = distance * float(row['times']) # Multiply by 2 to get return trip

# Add new columns 'short_haul', 'medium_haul', 'long_haul' to the dataframe
reshaped_df['short_haul'] = reshaped_df['distance'].apply(lambda x: x if x < short_haul_distance else 0)
reshaped_df['medium_haul'] = reshaped_df['distance'].apply(lambda x: x if short_haul_distance <= x < medium_haul_distance else 0)
reshaped_df['long_haul'] = reshaped_df['distance'].apply(lambda x: x if x >= medium_haul_distance else 0)

# For round trips, multiply the distance by 2
reshaped_df['short_haul'] = reshaped_df['short_haul']
reshaped_df['medium_haul'] = reshaped_df['medium_haul']
reshaped_df['long_haul'] = reshaped_df['long_haul']




# Add new columns 'Emissions' to the dataframe
reshaped_df['emissions_short'] = 0
reshaped_df['emissions_medium'] = 0
reshaped_df['emissions_long'] = 0
reshaped_df['emissions_stopovers'] = 0

# Calculate emissions for short, medium and long haul flights and stopovers
reshaped_df['emissions_short'] = reshaped_df['short_haul'] * short_haul_flight_emission_factor
reshaped_df['emissions_medium'] = reshaped_df['medium_haul'] * medium_haul_flight_emission_factor
reshaped_df['emissions_long'] = reshaped_df['long_haul'] * long_haul_flight_emission_factor
# Stopovers adds ~20 % of the emissions from the flight (only if stopover used)
reshaped_df['emissions_stopovers'] = reshaped_df['stops'] * (reshaped_df['emissions_short'] + reshaped_df['emissions_medium'] + reshaped_df['emissions_long']) * 0.2

# Add new column 'Emissions' to the dataframe
reshaped_df['emissions'] = reshaped_df['emissions_short'] + reshaped_df['emissions_medium'] + reshaped_df['emissions_long'] + reshaped_df['emissions_stopovers']

# Show distance and emissions
print('\n\nPlane travels:')
print(reshaped_df)

international_plane_clean = reshaped_df

# Calculate total distance and emissions from plane travels.
total_distance_plane = reshaped_df['distance'].sum()
total_emissions_plane = reshaped_df['emissions'].sum()

print(f'\nTotal distance travelled by plane: {total_distance_plane:.2f} km')
print(f'Total emissions from plane travels: {total_emissions_plane:.2f} kg CO2e\n\n')

# Save dataframe 
international_plane_clean.to_csv('csv/international_plane_travels.csv')






#######################################
#                                     #
# CAR PASSENGER TRAVELS AND EMISSIONS #
#                                     #
#######################################

# Do the same for Car passenger
# Take all columns with 'car' in the header and create new df
international_car = international_travel[[column for column in international_travel.columns if 'carpassenger' in column.lower()]]
# # Remove the first column which is a question
# international_car = international_car.iloc[:, 1:]
# Remove all rows with only NaN values and reset the index
international_car = international_car.dropna(how='all', axis=0).reset_index(drop=True)
# The rows are basically a repetition of the pattern '', '_from', '_to', '_via', '_times, so each 5th row is the start of a new travel
# Number of cars
num_cars = 5


# Reshape the dataframe
rows = []
for i in range(1, num_cars + 1):
    car = f'carPassenger_abroad_{i}'
    car_from = f'{car}_from'
    car_to = f'{car}_to'
    car_via = f'{car}_via'
    car_times = f'{car}_times'
    car_electric = f'Q_carPassenger_electric_abroad'
    car_petrol = f'Q_carPassenger_gas_abroad'
    
    temp_df = international_car[[car, car_from, car_to, car_via, car_times, car_electric, car_petrol]].copy()
    temp_df.columns = ['', 'from', 'to', 'via', 'times', 'electric', 'petrol']
    temp_df = temp_df.dropna(subset=['', 'from', 'to'], how='all').reset_index(drop=True)

    # Because 'times' is roundtrip, multiply by 2 to get one-way trip
    temp_df['times'] = pd.to_numeric(temp_df['times'], errors='coerce') * 2
    
    rows.append(temp_df)

# Concatenate all the reshaped dataframes
reshaped_df = pd.concat(rows, ignore_index=True)

# Remove all rows with a '-' sign anywhere in the row
reshaped_df = reshaped_df[~reshaped_df.apply(lambda x: x.str.contains('-').any(), axis=1)].reset_index(drop=True)

# Remove the first column
reshaped_df = reshaped_df.iloc[:, 1:]


# Use osrm to calculate the distance between the locations
# Loop through the dataframe, compute the distance between locations, and calculate the emissions

# Add a new column 'Distance' to the dataframe

reshaped_df['distance_electric'] = 0
reshaped_df['distance_petrol'] = 0
for index, row in reshaped_df.iterrows():
    distance = get_osrm_distance(row['from'], row['to'], lat_lon_file, row['via'])
    # Get the number of times the trip is made and multiply the distance by that number
    distance = distance * float(row['times'])

    if row['electric'] == 1 and row['petrol'] == 0:
        reshaped_df.loc[index, 'distance_electric'] = distance
    elif row['electric'] == 0 and row['petrol'] == 1:
        reshaped_df.loc[index, 'distance_petrol'] = distance
    elif row['electric'] == 1 and row['petrol'] == 1:
        reshaped_df.loc[index, 'distance_electric'] = distance / 2
        reshaped_df.loc[index, 'distance_petrol'] = distance / 2
    elif row['petrol'] == 0 and row['electric'] == 0:
        # If no answer is given, assume it is a petrol car and set the 'petrol' to 1
        reshaped_df.loc[index, 'distance_petrol'] = distance
        reshaped_df.loc[index, 'petrol'] = 1

reshaped_df['distance'] = reshaped_df['distance_electric'] + reshaped_df['distance_petrol']

# Add new column 'Emissions' to the dataframe. Calculate emissions based on the car type
reshaped_df['emissions_electric'] = reshaped_df['distance_electric'] * electric_car_emission_factor / 2 # Divide by 2 since we assume two people in car
reshaped_df['emissions_petrol'] = reshaped_df['distance_petrol'] * petrol_car_emission_factor / 2 # Divide by 2 since we assume two people in car
reshaped_df['emissions'] = reshaped_df['emissions_electric'] + reshaped_df['emissions_petrol']

# reshaped_df['emissions'] = reshaped_df['distance'] * emission_factor_car_per_km

international_carPassenger_clean = reshaped_df

# Display the reshaped dataframe
print('\n\nCar passenger travels:')
print(international_carPassenger_clean)
print(f'\nTotal emissions from petrol car passenger travels: {international_carPassenger_clean["emissions"].sum():.2f} kg CO2e')
print(f'Total emissions from electric car passenger travels: {international_carPassenger_clean["emissions"].sum():.2f} kg CO2e')
print(f'Total emissions from car passenger travels: {international_carPassenger_clean["emissions"].sum():.2f} kg CO2e')
print(f'\nTotal distance travelled by electric car passenger: {international_carPassenger_clean["distance_electric"].sum():.2f} km')
print(f'Total distance travelled by petrol car passenger: {international_carPassenger_clean["distance_petrol"].sum():.2f} km')
print(f'Total distance travelled by car passenger: {international_carPassenger_clean["distance"].sum():.2f} km\n\n')

# Save dataframe 
international_carPassenger_clean.to_csv('csv/international_carPassenger_travels.csv')



####################################
#                                  #
# CAR DRIVER TRAVELS AND EMISSIONS #
#                                  #
####################################

# Do the same for Car driver 
# Take all columns with 'car' in the header and create new df
international_car = international_travel[[column for column in international_travel.columns if 'cardriver' in column.lower()]]
# # Remove the first column which is a question
# international_car = international_car.iloc[:, 1:]
# Remove all rows with only NaN values and reset the index
international_car = international_car.dropna(how='all', axis=0).reset_index(drop=True)
# The rows are basically a repetition of the pattern '', '_from', '_to', '_via', '_times, so each 5th row is the start of a new travel
# Number of cars
num_cars = 5

# Reshape the dataframe
rows = []
for i in range(1, num_cars + 1):
    car = f'carDriver_abroad_{i}'
    car_from = f'{car}_from'
    car_to = f'{car}_to'
    car_via = f'{car}_via'
    car_times = f'{car}_times'
    car_electric = f'Q_carDriver_electric_abroad'
    car_petrol = f'Q_carDriver_gas_abroad'
    
    temp_df = international_car[[car, car_from, car_to, car_via, car_times, car_electric, car_petrol]].copy()
    temp_df.columns = ['', 'from', 'to', 'via', 'times', 'electric', 'petrol']
    temp_df = temp_df.dropna(subset=['', 'from', 'to'], how='all').reset_index(drop=True)

    # Because 'times' is roundtrip, multiply by 2 to get one-way trip
    temp_df['times'] = pd.to_numeric(temp_df['times'], errors='coerce') * 2
    
    rows.append(temp_df)

# Concatenate all the reshaped dataframes
reshaped_df = pd.concat(rows, ignore_index=True)

# Remove all rows with a '-' sign anywhere in the row
reshaped_df = reshaped_df[~reshaped_df.apply(lambda x: x.str.contains('-').any(), axis=1)].reset_index(drop=True)

# Remove the first column
reshaped_df = reshaped_df.iloc[:, 1:]



# Use osrm to calculate the distance between the locations
# Loop through the dataframe, compute the distance between locations, and calculate the emissions

# Add a new column 'Distance' to the dataframe
reshaped_df['distance_electric'] = 0
reshaped_df['distance_petrol'] = 0
for index, row in reshaped_df.iterrows():
    distance = get_osrm_distance(row['from'], row['to'], lat_lon_file, row['via'])
    # Get the number of times the trip is made and multiply the distance by that number
    distance = distance * float(row['times'])

    if row['electric'] == 1 and row['petrol'] == 0:
        reshaped_df.loc[index, 'distance_electric'] = distance
    elif row['electric'] == 0 and row['petrol'] == 1:
        reshaped_df.loc[index, 'distance_petrol'] = distance
    elif row['electric'] == 1 and row['petrol'] == 1:
        reshaped_df.loc[index, 'distance_electric'] = distance / 2
        reshaped_df.loc[index, 'distance_petrol'] = distance / 2
    elif row['petrol'] == 0 and row['electric'] == 0:
        # If no answer is given, assume it is a petrol car and set the 'petrol' to 1
        reshaped_df.loc[index, 'distance_petrol'] = distance
        reshaped_df.loc[index, 'petrol'] = 1

reshaped_df['distance'] = reshaped_df['distance_electric'] + reshaped_df['distance_petrol']

percentage_two_passenger_trips = len(international_carPassenger_clean) / len(reshaped_df)
# Add new column 'Emissions' to the dataframe
reshaped_df['emissions_electric'] = reshaped_df['distance_electric'] * electric_car_emission_factor
reshaped_df['emissions_petrol'] = reshaped_df['distance_petrol'] * petrol_car_emission_factor

# Estimate how large a portion of the trips were with two passengers (based on length of carPassenger and carDriver trips)
percentage_two_passenger_trips = len(international_carPassenger_clean) / len(reshaped_df)
print(f'\n\nPercentage of two passenger trips (International): {percentage_two_passenger_trips:.2f}')
# Adjust the emissions for the car driver trips to account for the two passengers
reshaped_df['emissions_electric'] = reshaped_df['emissions_electric'] * (1 - percentage_two_passenger_trips) + reshaped_df['emissions_electric'] * percentage_two_passenger_trips / 2 # Half of the emissions for the two passenger trips
reshaped_df['emissions_petrol'] = reshaped_df['emissions_petrol'] * (1 - percentage_two_passenger_trips) + reshaped_df['emissions_petrol'] * percentage_two_passenger_trips / 2 # Half of the emissions for the two passenger trips
reshaped_df['emissions'] = reshaped_df['emissions_electric'] + reshaped_df['emissions_petrol']


international_carDriver_clean = reshaped_df

# Display the reshaped dataframe
print('\n\nCar driver travels:')
print(international_carDriver_clean)
print(f'\nTotal emissions from electric car driver travels: {international_carDriver_clean["emissions_electric"].sum():.2f} kg CO2e')
print(f'Total emissions from petrol car driver travels: {international_carDriver_clean["emissions_petrol"].sum():.2f} kg CO2e')
print(f'Total emissions from car driver travels: {international_carDriver_clean["emissions"].sum():.2f} kg CO2e')
print(f'\nTotal distance travelled by electric car driver: {international_carDriver_clean["distance_electric"].sum():.2f} km')
print(f'Total distance travelled by petrol car driver: {international_carDriver_clean["distance_petrol"].sum():.2f} km')
print(f'Total distance travelled by car driver: {international_carDriver_clean["distance"].sum():.2f} km\n\n')

# Save dataframe 
international_carDriver_clean.to_csv('csv/international_carDriver_travels.csv')













###############################
#                             #
# TRAIN TRAVELS AND EMISSIONS #
#                             #
###############################


# Take all columns with 'train' in the header and create new df
international_train = international_travel[[column for column in international_travel.columns if 'train' in column.lower()]]
# Remove the first column which is a question
international_train = international_train.iloc[:, 1:]
# Remove all rows with only NaN values and reset the index
international_train = international_train.dropna(how='all', axis=0).reset_index(drop=True)
# The rows are basically a repetition of the pattern '', '_from', '_to', '_via', '_times, so each 5th row is the start of a new travel
# Number of trains
num_trains = 5

# Reshape the dataframe
rows = []

for i in range(1, num_trains + 1):
    train = f'train_abroad_{i}'
    train_from = f'{train}_from'
    train_to = f'{train}_to'
    train_times = f'{train}_times'
    temp_df = international_train[[train, train_from, train_to, train_times]].copy()
    temp_df.columns = ['', 'from', 'to', 'times']
    temp_df = temp_df.dropna(subset=['', 'from', 'to'], how='all').reset_index(drop=True)

    # Because 'times' is roundtrip, multiply by 2 to get one-way trip
    temp_df['times'] = pd.to_numeric(temp_df['times'], errors='coerce') * 2

    rows.append(temp_df)

# Concatenate all the reshaped dataframes
reshaped_df = pd.concat(rows, ignore_index=True)
# Add a row of None values to the 'via' column
reshaped_df['via'] = None

# Remove all rows with a '-' sign anywhere in the row
reshaped_df = reshaped_df[~reshaped_df.apply(lambda x: x.str.contains('-').any(), axis=1)].reset_index(drop=True)

# Remove the first column
reshaped_df = reshaped_df.iloc[:, 1:]

print('\n\nTrain travels:')
print(reshaped_df)

# Use osrm to calculate the distance between the locations
# Loop through the dataframe, compute the distance between locations, and calculate

# Add a new column 'Distance' to the dataframe
reshaped_df['distance'] = 0
for index, row in reshaped_df.iterrows():
    distance = get_osrm_distance(row['from'], row['to'], lat_lon_file, row['via'])
    # Get the number of times the trip is made and multiply the distance by that number
    distance = distance * float(row['times'])

    reshaped_df.loc[index, 'distance'] = distance

# Add new column 'Emissions' to the dataframe
reshaped_df['emissions'] = reshaped_df['distance'] * train_eu_average # Use the average emission factor for trains in EU (45% electrified, 55% diesel)

international_train_clean = reshaped_df

# Display the reshaped dataframe
print('\n\nTrain travels:')
print(international_train_clean)
print(f'Total emissions from train travels: {international_train_clean["emissions"].sum():.2f} kg CO2e')

# Save dataframe 
international_train_clean.to_csv('csv/international_train_travels.csv')








# Take all columns with 'bus' in the header and create new df
international_bus = international_travel[[column for column in international_travel.columns if 'bus' in column.lower()]]
# Remove the first column which is a question
international_bus = international_bus.iloc[:, 1:]
# Remove all rows with only NaN values and reset the index
international_bus = international_bus.dropna(how='all', axis=0).reset_index(drop=True)
# The rows are basically a repetition of the pattern '', '_from', '_to', '_via', '_times, so each 5th row is the start of a new travel
# Number of buses
num_buses = 5

# Reshape the dataframe
rows = []

for i in range(1, num_buses + 1):
    bus = f'bus_abroad_{i}'
    bus_from = f'{bus}_from'
    bus_to = f'{bus}_to'
    bus_times = f'{bus}_times'
    temp_df = international_bus[[bus, bus_from, bus_to, bus_times]].copy()
    temp_df.columns = ['', 'from', 'to', 'times']
    temp_df = temp_df.dropna(subset=['', 'from', 'to'   ], how='all').reset_index(drop=True)

    # Because 'times' is roundtrip, multiply by 2 to get one-way trip
    temp_df['times'] = pd.to_numeric(temp_df['times'], errors='coerce') * 2

    rows.append(temp_df)

# Concatenate all the reshaped dataframes
reshaped_df = pd.concat(rows, ignore_index=True)

# Remove all rows with a '-' sign anywhere in the row
reshaped_df = reshaped_df[~reshaped_df.apply(lambda x: x.str.contains('-').any(), axis=1)].reset_index(drop=True)

# Remove the first column
reshaped_df = reshaped_df.iloc[:, 1:]

# Display the reshaped dataframe
print('\n\nbus travels:')
print(reshaped_df)


# Use osrm to calculate the distance between the locations
# Loop through the dataframe, compute the distance between locations, and calculate

# Add a new column 'Distance' to the dataframe
reshaped_df['distance'] = 0
for index, row in reshaped_df.iterrows():
    distance = get_osrm_distance(row['from'], row['to'], lat_lon_file, row['via'])
    # Get the number of times the trip is made and multiply the distance by that number
    distance = distance * float(row['times'])

    reshaped_df.loc[index, 'distance'] = distance

# Add new column 'Emissions' to the dataframe
reshaped_df['emissions'] = reshaped_df['distance'] * bus_long_distance_eu_emission_factor

international_bus_clean = reshaped_df

# Display the reshaped dataframe
print('\n\nBus travels:')
print(international_bus_clean)
print(f'Total emissions from bus travels: {international_bus_clean["emissions"].sum():.2f} kg CO2e')

# Save dataframe 
international_bus_clean.to_csv('csv/international_bus_travels.csv')





#################################
#                               #
# TOTAL DISTANCES AND EMISSIONS #
#                               #
#################################


# Make new df with total emissions from all travels (only NOT empty dataframes)
all_dfs = [international_bus_clean, international_carPassenger_clean, international_carDriver_clean, international_train_clean, international_plane_clean]
all_df_strs = ['Bus', 'Car Passenger', 'Car Driver', 'Train', 'Plane']

all_df_strs_notEmpty = []
all_df_notEmpty = []
for i, df in enumerate(all_dfs):
    if df.empty:
        pass
    else:
        all_df_strs_notEmpty.append(all_df_strs[i])
        all_df_notEmpty.append(df)

print(all_df_strs_notEmpty)
for df in all_dfs:
    print(df['distance'].sum())

# Make a new dataframe with total distances and emissions
total_distances = pd.DataFrame({'Travel Type': all_df_strs,
                                'Total Distance (km)': [df['distance'].sum() for df in all_dfs]})


# Add a new column 'Emissions' to the dataframe
total_emissions = pd.DataFrame({'Travel Type': all_df_strs,
                                'Total Emissions (kg CO2e)': [df['emissions'].sum() for df in all_dfs]})

# Merge the two dataframes
total_data = pd.merge(total_distances, total_emissions, on='Travel Type')


print('\n\nTotal distances and emissions from all travels:')
print(total_data)

print('\n\n' + 50*'-')
print(f'Total emissions from all travels: {total_data["Total Emissions (kg CO2e)"].sum():.2f} kg CO2e')
print(50*'-' + '\n\n')


# Make a pie chart of the total emissions
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(6, 6))
plt.pie(total_data['Total Emissions (kg CO2e)'], labels=total_data['Travel Type'], autopct='%1.1f%%', startangle=140)
ax.axis('equal')
ax.set_title(f'Total emissions from all travels, {total_data["Total Emissions (kg CO2e)"].sum():.2f} kg CO2e')
plt.show()

# All transports other than plane are very low emitting
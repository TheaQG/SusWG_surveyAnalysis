'''
    Script to calculate the emissions of business travels in Denmark (not including Greenland and the Faroe Islands)

    !!! Need to check with "https://envs.au.dk/fileadmin/envs/Emission_inventories/Emission_factors/Emf_internet__Ex-GHG-main.htm!"
        for more accurate emission factors !!!


'''
import requests
import subprocess
import os
import time

import pandas as pd
import numpy as np


from utils import get_osrm_distance






#####################
#                   #   
# SETUP OSRM SERVER #
#                   #   
#####################

# Path to the OSRM server
osm_data_folder = os.path.join(os.path.dirname(__file__), 'osm_denmark')

# Function to check if OSRM server is running
def is_osrm_running():
    try:
        response = requests.get("http://localhost:5000/health")
        return response.status_code == 200
    except requests.ConnectionError:
        return False

# Function to start the OSRM server 
def start_osrm_server():
    # Ensure the OSRM data folder exists
    if not os.path.exists(osm_data_folder):
        print(f"OSRM data folder not found: '{osm_data_folder}'")
        return

    # Command to start OSRM server using Docker
    command = [
        "docker", "run", "-t", "-i", "-p", "5000:5000",
        "-v", f"{osm_data_folder}:/data", # Mount the data folder to /data in the container
        "osrm/osrm-backend",
        "osrm-routed", "/data/denmark-latest.osrm" # Update the path to match the new folder structure
        ]

    # Start the OSRM server in the background
    try:
        print("Starting OSRM server...")
        subprocess.Popen(command) # Starts the server as a background process
        print("OSRM server started successfully.")
    except Exception as e:
        print(f"Error starting OSRM server: {e}")



# Use this function to alert if OSRM is not running
if not is_osrm_running():
    print("OSRM server is not running. Starting the server...")
    start_osrm_server()
    # Add a delay to allow the server to start
    time.sleep(10)
else:
    # Proceed with your distance calculations
    print("OSRM server is running. Ready to calculate distances.")






###################################
#                                 #
# SETUP EMISSION FACTORS AND DATA # 
#                                 #
###################################

# !! BASED ON COWI (https://www.dsb.dk/globalassets/om-dsb/baeredygtighed/miljo/sammenligning-af-emmisionsfaktorer_cowi-rapport-til-dsb_okt-2023.pdf)
# !! Need to verify the emission factors (talk with local AU ENVS Emission group)

# Car (average per km of diesel, petrol, hybrid and electric cars)
emission_factor_car_per_km = 0.118
# Train
emission_factor_train_per_km = 0.041
# Bus 
emission_factor_bus_per_km = 0.020

# Average distance between two locations in Denmark (Kbh<->Aalborg and Kbh<->Aarhus)
average_distance_plane = (238 + 156) / 2
# Average distance between two locations in Denmark (Odden<-->Aarhus, Odden<-->Ebeltoft)
average_distance_ferry = (62.3 + 69) / 2

# Ferry (Odden<-->Ebeltoft), ~70 km (one way), 0.915 kg CO2e per person km (with car)
emission_factor_ferry_one_way = 0.915 * average_distance_ferry
# Plane (per passenger per one-way trip), average of Kbh<->Aalborg and Kbh<->Aarhus
emission_factor_plane_one_way = (39.3 + 28.5) / 2






# Load .xlsx file
FILE_PATH = 'csv/cleaned_BusinessTravels.xlsx'

national_travel = pd.read_excel(FILE_PATH, sheet_name='DK_BusinessTravels_clean')







#############################
#                           #
# BUS TRAVELS AND EMISSIONS #
#                           #
#############################

# Take all columns with 'bus' in the header and create new df
national_bus = national_travel[[column for column in national_travel.columns if 'bus' in column.lower()]]
# Remove the first column which is a question
national_bus = national_bus.iloc[:, 1:]
# Remove all rows with only NaN values and reset the index
national_bus = national_bus.dropna(how='all', axis=0).reset_index(drop=True)
# The rows are basically a repetition of the pattern '', '_from', '_to', '_via', '_times, so each 5th row is the start of a new travel

# Number of buses
num_buses = 5

# Reshape the dataframe
rows = []
for i in range(1, num_buses + 1):
    bus = f'bus_dk_{i}'
    bus_from = f'{bus}_from'
    bus_to = f'{bus}_to'
    bus_via = f'{bus}_via'
    bus_times = f'{bus}_times'
    
    temp_df = national_bus[[bus, bus_from, bus_to, bus_via, bus_times]].copy()
    temp_df.columns = ['', 'from', 'to', 'via', 'times']
    temp_df = temp_df.dropna(subset=['', 'from', 'to'], how='all').reset_index(drop=True)
    
    rows.append(temp_df)

# Concatenate all the reshaped dataframes
reshaped_df = pd.concat(rows, ignore_index=True)

# Remove all rows with a '-' sign anywhere in the row
reshaped_df = reshaped_df[~reshaped_df.apply(lambda x: x.str.contains('-').any(), axis=1)].reset_index(drop=True)

# Remove the first column
reshaped_df = reshaped_df.iloc[:, 1:]




# Use osrm to calculate the distance between the locations
# Loop through the dataframe, compute the distance between locations, and calculate the emissions
# The lat_lon_file should contain the latitudes and longitudes of the all locations.
lat_lon_file = 'csv/national_destinations.csv'

# Add a new column 'Distance' to the dataframe
reshaped_df['distance'] = 0
for index, row in reshaped_df.iterrows():
    distance = get_osrm_distance(row['from'], row['to'], lat_lon_file, row['via'])
    reshaped_df.loc[index, 'distance'] = distance

# Add new column 'Emissions' to the dataframe
reshaped_df['emissions'] = reshaped_df['distance'] * emission_factor_bus_per_km

national_bus_clean = reshaped_df

# Display the reshaped dataframe
print('\n\nBus travels:')
print(national_bus_clean)
print(f'Total emissions from bus travels: {national_bus_clean["emissions"].sum():.2f} kg CO2e')

# Save dataframe 
national_bus_clean.to_csv('csv/national_bus_travels.csv')





#######################################
#                                     #
# CAR PASSENGER TRAVELS AND EMISSIONS #
#                                     #
#######################################

# Do the same for Car passenger
# Take all columns with 'car' in the header and create new df
national_car = national_travel[[column for column in national_travel.columns if 'carpassenger' in column.lower()]]
# Remove the first column which is a question
national_car = national_car.iloc[:, 1:]
# Remove all rows with only NaN values and reset the index
national_car = national_car.dropna(how='all', axis=0).reset_index(drop=True)
# The rows are basically a repetition of the pattern '', '_from', '_to', '_via', '_times, so each 5th row is the start of a new travel
# Number of cars
num_cars = 8

# Reshape the dataframe
rows = []
for i in range(1, num_cars + 1):
    car = f'carPassenger_dk_{i}'
    car_from = f'{car}_from'
    car_to = f'{car}_to'
    car_via = f'{car}_via'
    car_times = f'{car}_times'
    
    temp_df = national_car[[car, car_from, car_to, car_via, car_times]].copy()
    temp_df.columns = ['', 'from', 'to', 'via', 'times']
    temp_df = temp_df.dropna(subset=['', 'from', 'to'], how='all').reset_index(drop=True)
    
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
reshaped_df['distance'] = 0
for index, row in reshaped_df.iterrows():
    distance = get_osrm_distance(row['from'], row['to'], lat_lon_file, row['via'])
    reshaped_df.loc[index, 'distance'] = distance

# Add new column 'Emissions' to the dataframe
reshaped_df['emissions'] = reshaped_df['distance'] * emission_factor_car_per_km

national_carPassenger_clean = reshaped_df

# Display the reshaped dataframe
print('\n\nCar passenger travels:')
print(national_carPassenger_clean)
print(f'Total emissions from car passenger travels: {national_carPassenger_clean["emissions"].sum():.2f} kg CO2e')

# Save dataframe 
national_carPassenger_clean.to_csv('csv/national_carPassenger_travels.csv')







####################################
#                                  #
# CAR DRIVER TRAVELS AND EMISSIONS #
#                                  #
####################################


# Do the same for Car driver 
# Take all columns with 'car' in the header and create new df
national_car = national_travel[[column for column in national_travel.columns if 'cardriver' in column.lower()]]
# Remove the first column which is a question
national_car = national_car.iloc[:, 1:]
# Remove all rows with only NaN values and reset the index
national_car = national_car.dropna(how='all', axis=0).reset_index(drop=True)
# The rows are basically a repetition of the pattern '', '_from', '_to', '_via', '_times, so each 5th row is the start of a new travel
# Number of cars
num_cars = 8

# Reshape the dataframe
rows = []
for i in range(1, num_cars + 1):
    car = f'carDriver_dk_{i}'
    car_from = f'{car}_from'
    car_to = f'{car}_to'
    car_via = f'{car}_via'
    car_times = f'{car}_times'
    
    temp_df = national_car[[car, car_from, car_to, car_via, car_times]].copy()
    temp_df.columns = ['', 'from', 'to', 'via', 'times']
    temp_df = temp_df.dropna(subset=['', 'from', 'to'], how='all').reset_index(drop=True)
    
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
reshaped_df['distance'] = 0
for index, row in reshaped_df.iterrows():
    distance = get_osrm_distance(row['from'], row['to'], lat_lon_file, row['via'])
    reshaped_df.loc[index, 'distance'] = distance

# Add new column 'Emissions' to the dataframe
reshaped_df['emissions'] = reshaped_df['distance'] * emission_factor_car_per_km

national_carDriver_clean = reshaped_df

# Display the reshaped dataframe
print('\n\nCar driver travels:')
print(national_carDriver_clean)
print(f'Total emissions from car driver travels: {national_carDriver_clean["emissions"].sum():.2f} kg CO2e')

# Save dataframe 
national_carDriver_clean.to_csv('csv/national_carDriver_travels.csv')





###############################
#                             #
# TRAIN TRAVELS AND EMISSIONS #
#                             #
###############################

# Take all columns with 'train' in the header and create new df
national_train = national_travel[[column for column in national_travel.columns if 'train' in column.lower()]]
# Remove the first column which is a question
national_train = national_train.iloc[:, 1:]
# Remove all rows with only NaN values and reset the index
national_train = national_train.dropna(how='all', axis=0).reset_index(drop=True)
# The rows are basically a repetition of the pattern '', '_from', '_to', '_via', '_times, so each 5th row is the start of a new travel
# Number of trains
num_trains = 5

# Reshape the dataframe
rows = []

for i in range(1, num_trains + 1):
    train = f'train_dk_{i}'
    train_from = f'{train}_from'
    train_to = f'{train}_to'
    train_times = f'{train}_times'
    temp_df = national_train[[train, train_from, train_to, train_times]].copy()
    temp_df.columns = ['', 'from', 'to', 'times']
    temp_df = temp_df.dropna(subset=['', 'from', 'to'], how='all').reset_index(drop=True)
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
reshaped_df['distance'] = 0
for index, row in reshaped_df.iterrows():
    distance = get_osrm_distance(row['from'], row['to'], lat_lon_file)
    reshaped_df.loc[index, 'distance'] = distance

# Add new column 'Emissions' to the dataframe
reshaped_df['emissions'] = reshaped_df['distance'] * emission_factor_train_per_km

national_train_clean = reshaped_df

# Display the reshaped dataframe
print('\n\nTrain travels:')
print(national_train_clean)
print(f'Total emissions from train travels: {national_train_clean["emissions"].sum():.2f} kg CO2e')

# Save dataframe 
national_train_clean.to_csv('csv/national_train_travels.csv')





###############################
#                             #
# FERRY TRAVELS AND EMISSIONS #
#                             #
###############################

# For ferry, only one column with the number of travels
for column in national_travel.columns:
    if 'ferry' in column.lower():
        national_ferry = national_travel[column]
        break

# Remove all rows with only NaN values and reset the index
national_ferry = national_ferry.dropna(how='all', axis=0).reset_index(drop=True)
# Remove all rows with 0 travels
national_ferry = national_ferry[national_ferry != 0].reset_index(drop=True)

# Create new df with national_ferry.values[1:] and 'ferry_travels' as column name
national_ferry = pd.DataFrame(national_ferry.values[1:], columns=['ferry_travels'])

# Add a new column 'Emissions' to the dataframe (round trip, so multiply by 2)
national_ferry['emissions'] = national_ferry['ferry_travels'] * emission_factor_ferry_one_way * 2

# Add a new column 'distance' to the dataframe (average of Kbh<->Aalborg and Kbh<->Aarhus)
national_ferry['distance'] = average_distance_ferry * national_ferry['ferry_travels']

national_ferry_clean = national_ferry

# Display the dataframe
print('\n\nFerry travels:')
print(national_ferry_clean)
print(f'Total emissions from ferry travels: {national_ferry_clean["emissions"].sum():.2f} kg CO2e')

# Save dataframe 
national_ferry_clean.to_csv('csv/national_ferry_travels.csv')







################################
#                              #
# FLIGHT TRAVELS AND EMISSIONS #
#                              #
################################

# For flight, only one column with the number of travels
national_flight = national_travel[[column for column in national_travel.columns if 'flight' in column.lower()]]
national_flight = national_flight[1:]

# Remove all rows with only NaN values and reset the index
national_flight = national_flight.dropna(how='all', axis=0).reset_index(drop=True)

# Remove all rows with 0 travels
national_flight = national_flight[national_flight['flight_dk'] != 0].reset_index(drop=True)


# Add a new column 'Emissions' to the dataframe (round trip, so multiply by 2)
national_flight['emissions'] = national_flight * emission_factor_plane_one_way * 2

# Add a new column 'distance' to the dataframe (average of Kbh<->Aalborg and Kbh<->Aarhus)
national_flight['distance'] = average_distance_plane * national_flight['flight_dk']

national_flight_clean = national_flight

# Display the dataframe
print('\n\nFlight travels:')
print(national_flight_clean)
print(f'Total emissions from national flight travels: {national_flight_clean["emissions"].sum():.2f} kg CO2e')

# Save dataframe 
national_flight_clean.to_csv('csv/national_plane_travels.csv')









#################################
#                               #
# TOTAL DISTANCES AND EMISSIONS #
#                               #
#################################


# Make new df with total emissions from all travels
total_distances = pd.DataFrame({'Travel Type': ['Bus', 'Car Passenger', 'Car Driver', 'Train', 'Ferry', 'Flight'],
                                'Total Distance (km)': [national_bus_clean['distance'].sum(),
                                                        national_carPassenger_clean['distance'].sum(),
                                                        national_carDriver_clean['distance'].sum(),
                                                        national_train_clean['distance'].sum(),
                                                        national_ferry_clean['ferry_travels'].sum() * 2 * 68.524, # We asked for round trip
                                                        national_flight_clean['flight_dk'].sum() * 2 * ((238 + 156)/2)]}) # We asked for round trip



# Add a new column 'Emissions' to the dataframe
total_emissions = pd.DataFrame({'Travel Type': ['Bus', 'Car Passenger', 'Car Driver', 'Train', 'Ferry', 'Flight'],
                                'Total Emissions (kg CO2e)': [national_bus_clean['emissions'].sum(),
                                                        national_carPassenger_clean['emissions'].sum(),
                                                        national_carDriver_clean['emissions'].sum(),
                                                        national_train_clean['emissions'].sum(),
                                                        national_ferry_clean['emissions'].sum(),
                                                        national_flight_clean['emissions'].sum()]})

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

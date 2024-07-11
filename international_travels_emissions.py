'''
This script is used to calculate the emissions from international business travels.
'''

import pandas as pd
from utils import get_haversine_distance

# Load .xlsx file
FILE_PATH = '/Users/au728490/Documents/PhD_AU/Python_Scripts/SusWG_surveyAnalysis/csv/cleaned_BusinessTravels.xlsx'

international_travel = pd.read_excel(FILE_PATH, sheet_name='Abroad_BusinessTravels_clean')

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
    
    rows.append(temp_df)

# Concatenate all the reshaped dataframes
reshaped_df = pd.concat(rows, ignore_index=True)

# Remove all rows with a '-' sign anywhere in the row
reshaped_df = reshaped_df[~reshaped_df.apply(lambda x: x.str.contains('-').any(), axis=1)].reset_index(drop=True)

# Remove the first column
reshaped_df = reshaped_df.iloc[:, 1:]

# If 'stops' is NaN, set it to 0
reshaped_df['stops'] = reshaped_df['stops'].fillna(0)

# Display the reshaped dataframe
print('\n\nPlane travels:')
print(reshaped_df)


# Use the Haversine function to caculate kms travelled by plane.
# Loop through the dataframe, compute the distance between locations,
# and multiply by number of times travelled.

# Add a new column 'Distance' to the dataframe
reshaped_df['distance'] = 0
for index, row in reshaped_df.iterrows():
    distance = get_haversine_distance('Kastrup', row['to'], 'international_destinations.csv')
    reshaped_df.loc[index, 'distance'] = distance * float(row['times'])


# Fly - International + RFI (person.km) Scope 3. kg CO2e per person km
emission_factor_plane_per_km = 0.197423783892617

# Add a new column 'Emissions', which is the distance travelled multiplied with emission factor
reshaped_df['emissions'] = reshaped_df['distance'] * emission_factor_plane_per_km

# Calculate total distance and emissions from plane travels.
total_distance_plane = reshaped_df['distance'].sum()
total_emissions_plane = reshaped_df['emissions'].sum()

print(f'Total distance travelled by plane: {total_distance_plane:.2f} km')
print(f'Total emissions from plane travels: {total_emissions_plane:.2f} kg CO2e')






# Do the same for Car driver 
# Take all columns with 'car' in the header and create new df
international_car = international_travel[[column for column in international_travel.columns if 'cardriver' in column.lower()]]
# Remove the first column which is a question
international_car = international_car.iloc[:, 1:]
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
    
    temp_df = international_car[[car, car_from, car_to, car_via, car_times]].copy()
    temp_df.columns = ['', 'from', 'to', 'via', 'times']
    temp_df = temp_df.dropna(subset=['', 'from', 'to'], how='all').reset_index(drop=True)
    
    rows.append(temp_df)

# Concatenate all the reshaped dataframes
reshaped_df = pd.concat(rows, ignore_index=True)

# Remove all rows with a '-' sign anywhere in the row
reshaped_df = reshaped_df[~reshaped_df.apply(lambda x: x.str.contains('-').any(), axis=1)].reset_index(drop=True)

# Remove the first column
reshaped_df = reshaped_df.iloc[:, 1:]

# Display the reshaped dataframe
print('\n\nCar driver travels:')
print(reshaped_df)



# Do the same for Car passenger
# Take all columns with 'car' in the header and create new df
international_car = international_travel[[column for column in international_travel.columns if 'carpassenger' in column.lower()]]
# Remove the first column which is a question
international_car = international_car.iloc[:, 1:]
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
    
    temp_df = international_car[[car, car_from, car_to, car_via, car_times]].copy()
    temp_df.columns = ['', 'from', 'to', 'via', 'times']
    temp_df = temp_df.dropna(subset=['', 'from', 'to'], how='all').reset_index(drop=True)
    
    rows.append(temp_df)

# Concatenate all the reshaped dataframes
reshaped_df = pd.concat(rows, ignore_index=True)

# Remove all rows with a '-' sign anywhere in the row
reshaped_df = reshaped_df[~reshaped_df.apply(lambda x: x.str.contains('-').any(), axis=1)].reset_index(drop=True)

# Remove the first column
reshaped_df = reshaped_df.iloc[:, 1:]

# Display the reshaped dataframe
print('\n\nCar passenger travels:')
print(reshaped_df)



# Take all columns with 'car' in the header and create new df
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
    rows.append(temp_df)

# Concatenate all the reshaped dataframes
reshaped_df = pd.concat(rows, ignore_index=True)

# Remove all rows with a '-' sign anywhere in the row
reshaped_df = reshaped_df[~reshaped_df.apply(lambda x: x.str.contains('-').any(), axis=1)].reset_index(drop=True)

# Remove the first column
reshaped_df = reshaped_df.iloc[:, 1:]

# Display the reshaped dataframe
print('\n\nTrain travels:')
print(reshaped_df)




# Take all columns with 'car' in the header and create new df
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


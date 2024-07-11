'''
    Script to calculate the emissions of business travels in Denmark (not including Greenland and the Faroe Islands)
'''

import pandas as pd
import numpy as np






# Load .xlsx file
FILE_PATH = '/Users/au728490/Documents/PhD_AU/Python_Scripts/SusWG_surveyAnalysis/csv/cleaned_BusinessTravels.xlsx'

national_travel = pd.read_excel(FILE_PATH, sheet_name='DK_BusinessTravels_clean')

# Car driver, Car passenger, Bus, Train, Flight, Ferry
# Car Driver, Car passenger and Bus have 'From' 'To' and 'Via' columns
# Train has 'From' and 'To' columns
# Ferry has only counts of travels
# Flight has only counts of travels

# Build dfs for Car driver, Car passenger and Bus with 'From' 'To' and 'Via' columns

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


# Display the reshaped dataframe
print('\n\nBus travels:')
print(reshaped_df)






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

# Display the reshaped dataframe
print('\n\nCar passenger travels:')
print(reshaped_df)





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

# Display the reshaped dataframe
print('\n\nCar driver travels:')
print(reshaped_df)




# Take all columns with 'car' in the header and create new df
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

# Display the reshaped dataframe
print('\n\nTrain travels:')
print(reshaped_df)







# For ferry, only one column with the number of travels
for column in national_travel.columns:
    if 'ferry' in column.lower():
        national_ferry = national_travel[column]
        break
# Remove all rows with only NaN values and reset the index (first index is the question, )
national_ferry = national_ferry.dropna(how='all').reset_index(drop=True)

# Remove all rows with 0 travels
national_ferry = national_ferry[national_ferry != 0].reset_index(drop=True)
print('\n\nFerry travels:')
print(national_ferry)



# For flight, only one column with the number of travels
national_flight = national_travel[[column for column in national_travel.columns if 'flight' in column.lower()]]
# Remove all rows with only NaN values and reset the index
national_flight = national_flight.dropna(how='all').reset_index(drop=True)
# Remove all rows with 0 travels
national_flight = national_flight[national_flight != 0].reset_index(drop=True)

print('\n\nFlight travels:')
print(national_flight)

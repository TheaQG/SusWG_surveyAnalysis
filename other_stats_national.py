'''
    ToDo list:
        - Compare with national statistics (what is average/median for all working Danes/world citizens?)

'''

import requests
import subprocess
import os
import time

import pandas as pd
import numpy as np

# Import plot libs
import matplotlib.pyplot as plt
# import seaborn as sns

# Define figure path
PATH_FIGS = 'Figures/National_BusinessTravels/'
if not os.path.exists(PATH_FIGS):
    os.makedirs(PATH_FIGS)


# Set font size for plots
plt.rcParams.update({'font.size': 14})
# Set font size for title
plt.rcParams.update({'axes.titlesize': 16})
# Set font size for labels
plt.rcParams.update({'axes.labelsize': 14})
# Set font size for legend
plt.rcParams.update({'legend.fontsize': 12})


# Load in all national data 

national_bus = pd.read_csv('csv/national_bus_travels.csv')
national_carDriver = pd.read_csv('csv/national_carDriver_travels.csv') 
national_carPassenger = pd.read_csv('csv/national_carPassenger_travels.csv')
national_ferry = pd.read_csv('csv/national_ferry_travels.csv')
national_train = pd.read_csv('csv/national_train_travels.csv')
national_plane = pd.read_csv('csv/national_plane_travels.csv')

# Based on the columns 'electric' and 'petrol', divide into two dfs
national_carDriver_electric = national_carDriver[national_carDriver['electric'] == 1]
national_carDriver_petrol = national_carDriver[national_carDriver['petrol'] == 1]
# # Rename the columns 'distance_eletric' and 'distance_petrol' to 'distance'
# national_carDriver_electric.rename(columns={'distance_electric': 'distance'}, inplace=True)
# national_carDriver_petrol.rename(columns={'distance_petrol': 'distance'}, inplace=True)
# # Rename the columns 'emissions_eletric' and 'emissions_petrol' to 'emissions'
# national_carDriver_electric.rename(columns={'emissions_electric': 'emissions'}, inplace=True)
# national_carDriver_petrol.rename(columns={'emissions_petrol': 'emissions'}, inplace=True)

# Based on the columns 'electric' and 'petrol', divide into two dfs
national_carPassenger_electric = national_carPassenger[national_carPassenger['electric'] == 1]
national_carPassenger_petrol = national_carPassenger[national_carPassenger['petrol'] == 1]
# # Rename the columns 'distance_eletric' and 'distance_petrol' to 'distance'
# national_carPassenger_electric.rename(columns={'distance_electric': 'distance'}, inplace=True)
# national_carPassenger_petrol.rename(columns={'distance_petrol': 'distance'}, inplace=True)
# # Rename the columns 'emissions_eletric' and 'emissions_petrol' to 'emissions'
# national_carPassenger_electric.rename(columns={'emissions_electric': 'emissions'}, inplace=True)
# national_carPassenger_petrol.rename(columns={'emissions_petrol': 'emissions'}, inplace=True)


print(national_carPassenger_electric)
print(national_carPassenger_petrol)

all_national = [national_bus, national_carDriver_petrol, national_carDriver_electric, national_carPassenger_petrol, national_carPassenger_electric, national_ferry, national_train, national_plane]
mode_strs = ['Bus', 'CarDriverPetrol', 'CarDriverElectric', 'CarPassengerPetrol', 'CarPassengerElectric', 'Ferry', 'Train', 'Plane']
mode_strs2 = ['Bus', 'Petrol car, driver', 'Electric car, driver', 'Petrol car, passenger', 'Electric car, passenger', 'Ferry', 'Train', 'Plane']

N_strs = ['times', 'times', 'times', 'times', 'times', 'ferry_travels', 'times', 'flight_dk']

# Number of respondants (and how many where used in the analysis) (from excel sheet)
N_response = 123
N_use = 79 # Rest have not travelled in the last half year before survey
N_not_use = N_response - N_use
N_ENVS = 170
N_no_answer = N_ENVS - N_response

# Plot response rate as pie chart
labels = 'Travelled in last 1/2 year', 'No travel in last 1/2 year'
colors = ['gold', 'lightgrey']
sizes = [N_use, N_not_use]
percentages = ["{0:.1%}".format(value / N_response) for value in sizes]

fig1, ax1 = plt.subplots(figsize=(8,5))
fig1.suptitle(r'$\bf{National}$ $\bf{business}$ $\bf{travels}$' + f'\n(Answers: {N_response}, ENVS employees: {N_ENVS})')
ax1.pie(x=sizes,
        labels=percentages,
        startangle=90,
        colors=colors,
        # colors=sns.color_palette("Set2"),
        explode=[0.05, 0.05])
ax1.legend(labels,loc=(1.02,0.25))

fig1.tight_layout()

fig1.savefig(PATH_FIGS + 'national_response_rate.png', dpi=300, bbox_inches='tight')



#####################
#                   #
# NUMBER OF TRAVELS #
#                   #
#####################

# Total number of travels with different modes of transport
# For each mode of transport, calculate the total number of travels
total_travels = []
for i, mode in enumerate(all_national):
    print(f'\n\n{mode_strs[i]} travels:')
    print(mode[N_strs[i]].sum())
    total_travels.append(mode[N_strs[i]].sum())
N_all = sum(total_travels)
percentages = ["{0:.1%}".format(value / N_all) for value in total_travels]

# Select nice colors
colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'lightgreen', 'lightpink', 'lightblue', 'palegoldenrod']
# Explode only small slices (adjust values as needed)
explode = [0.1 if value < 0.01 * sum(total_travels) else 0 for value in total_travels]

# Plot total number of travels with different modes of transport as pie chart
fig2, ax2 = plt.subplots(figsize=(8,5))
fig2.suptitle(r'$\bf{National}$' + f'\nTotal number of travels N = {sum(total_travels)}\nDifferent modes of transport in [%]')
ax2.pie(total_travels,
        labels=percentages,
        startangle=90,
        counterclock=False,
        colors=colors,
        explode = explode,
        labeldistance=1.1
        # wedgeprops=dict(edgecolor='black', width=0.3)
        )
legend = ax2.legend(mode_strs2,loc='center left', bbox_to_anchor=(1, 0.5), title=r'$\bf{Mode}$ $\bf{of}$ $\bf{transport}$')

fig2.tight_layout()


fig2.savefig(PATH_FIGS + 'national_travels_pTransport_pie.png', dpi=300, bbox_inches='tight')

# plt.close(fig2)






#######################
#                     #
# DISTANCES TRAVELLED #
#                     #
#######################
print('\n\n\n\n\n')
# Total distance travelled by each mode of transport
# For each mode of transport, calculate the total distance travelled
total_distances = []
for i, mode in enumerate(all_national):
    print(mode['distance'])
    print(f'\n\n{mode_strs[i]} travels:')
    print(mode['distance'].sum())
    total_distances.append(mode['distance'].sum())

percentages = ["{0:.1%}".format(value / sum(total_distances)) for value in total_distances]

# Exploding small slices if needed (adjust explosion values as needed)
explode = [0.1 if value < 0.05 * sum(total_distances) else 0 for value in total_distances]
explode[3] = 0.2

# Plot total distance travelled by each mode of transport as pie chart
fig3, ax3 = plt.subplots(figsize=(10,5))
fig3.suptitle(r'$\bf{National}$' + f'\nTotal distance travelled = {sum(total_distances):,.0f} km\nDifferent modes of transport in [%]')
ax3.pie(total_distances,
        labels=percentages,
        startangle=90,
        counterclock=False,
        colors=colors,
        explode=explode,
        )
# Add a legend outside the plot showing both mode names and distances
ax3.legend([f"{mode} ({dist:,.0f} km)" for mode, dist in zip(mode_strs2, total_distances)],
           loc="center left", bbox_to_anchor=(1.05, 0.5), title="Mode of Transport")#, fontsize=10)
#ax3.legend(mode_strs,loc=(1.05,0.25))

fig3.tight_layout()


fig3.savefig(PATH_FIGS + 'national_distance_pTransport_pie.png', dpi=300, bbox_inches='tight')

# plt.close(fig3)

# # Average distance travelled by each mode of transport

# For each mode of transport, calculate the average and median distance travelled
average_distances = []
median_distances = []
std_distances = []
for i, mode in enumerate(all_national):
    print(f'\n\n{mode_strs[i]} travels:')
    # Mean and median also based on 'times' column
    print(mode[N_strs[i]])
    average_array = mode['distance'] / mode[N_strs[i]]
    print(average_array)
    average = average_array.mean()
    std = average_array.std()
    median = average_array.median()

    # average = mode['distance'].sum() / mode[N_strs[i]].sum()
    # std = mode['distance'].std() / mode[N_strs[i]].mean()
    # median = mode['distance'].median() / mode[N_strs[i]].median()
    print(f'Average distance travelled per travel: {average:.1f} km')
    print(f'Standard deviation: {std:.1f} km')
    print(f'Median distance travelled per travel: {median:.1f} km')
    
    average_distances.append(average)
    median_distances.append(median)
    std_distances.append(std)

    

# Plot in one bar chart (one bar per mode of transport)
fig4, ax4 = plt.subplots(figsize=(8,5))
fig4.suptitle(r'$\bf{National}$' + f'\nAverage distance travelled per travel, N = {N_all}')

# Allow for x-axis labels to be rotated for better readability
ax4.bar(mode_strs2,
        median_distances,
        color=colors,
        alpha=0.3,
        edgecolor='black',
        linewidth=0.5,
        hatch='//'
        )
ax4.bar(mode_strs2,
        average_distances,
        color=colors,
        alpha=0.7,
        edgecolor='black',
        linewidth=0.5,
        )
# Add error bars for standard deviation
ax4.errorbar(mode_strs2, average_distances, yerr=std_distances, fmt='.', color='black', ecolor='black', capsize=4, capthick=1, elinewidth=0.8)


plt.xticks(rotation=30, ha='right')

# Add gridlines for better readability
ax4.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.5)

# Add text annotations for each bar
ax4.set_ylabel('Distance travelled [km]')#, fontsize=12)
# ax4.set_xlabel('Mode of transport', fontsize=12)
# Set y-axis to start at 0
ax4.set_ylim(bottom=0)

# Add legend for median/mean bar types
ax4.legend(['Median', 'Mean'], loc='upper left')


fig4.tight_layout()

fig4.savefig(PATH_FIGS + 'national_distance_pTravel_bar.png', dpi=300, bbox_inches='tight')

# plt.close(fig4)



#############
#           #
# EMISSIONS #
#           # 
#############

# Total emissions per mode of transport
# For each mode of transport, calculate the total emissions
total_emissions = []
for i, mode in enumerate(all_national):
    print(f'\n\n{mode_strs[i]} travels:')
    print(mode['emissions'].sum())
    total_emissions.append(mode['emissions'].sum())
percentages = ["{0:.1%}".format(value / sum(total_emissions)) for value in total_emissions]

# Explode small slices if needed (adjust explosion values as needed)
explode = [0.06 if value < 0.01 * sum(total_emissions) else 0 for value in total_emissions]
explode[4] = 0.35
# Plot total emissions by each mode of transport as pie chart
fig7, ax7 = plt.subplots(figsize=(10,5))
fig7.suptitle(r'$\bf{National}$' + f'\nTotal emissions = {sum(total_emissions):.1f} kg CO2\nDifferent modes of transport in [%]')
ax7.pie(total_emissions,
        labels=percentages,
        startangle=90,
        counterclock=False,
        colors=colors,
        explode=explode,
        labeldistance=1.1
        )
ax7.legend(mode_strs2,loc='center right', bbox_to_anchor=(-0.1, 0.5), title=r'$\bf{Mode}$ $\bf{of}$ $\bf{transport}$')

fig7.tight_layout()


fig7.savefig(PATH_FIGS + 'national_emissions_pTransport_pie.png', dpi=300, bbox_inches='tight')

# plt.close('all')




# For each mode of transport, calculate the average and median emissions
average_emissions = []
median_emissions = []
std_emissions = []
for i, mode in enumerate(all_national):
    print(f'\n\n{mode_strs[i]} travels:')
    # Mean and median also based on 'times' column
    print(mode[N_strs[i]])
    average_array = mode['emissions'] / mode[N_strs[i]]
    print(average_array)
    average = average_array.mean()
    std = average_array.std()
    median = average_array.median()

    # average = mode['emissions'].sum() / mode[N_strs[i]].sum()
    # std = mode['emissions'].std() / mode[N_strs[i]].mean()
    # median = mode['emissions'].median() / mode[N_strs[i]].median()
    print(f'Average emissions per travel: {average:.1f} kg CO2')
    print(f'Standard deviation: {std:.1f} kg CO2')
    print(f'Median emissions per travel: {median:.1f} kg CO2')
    
    average_emissions.append(average)
    median_emissions.append(median)
    std_emissions.append(std)


# Plot in one bar chart (one bar per mode of transport)
fig8, ax8 = plt.subplots(figsize=(8,5))
fig8.suptitle(r'$\bf{National}$' + f'\nAverage emissions per travel, N = {N_all}')

# Allow for x-axis labels to be rotated for better readability
ax8.bar(mode_strs2,
        median_emissions,
        color=colors,
        alpha=0.3,
        edgecolor='black',
        linewidth=0.5,
        hatch='//'
        )
ax8.bar(mode_strs2,
        average_emissions,
        color=colors,
        alpha=0.7,
        edgecolor='black',
        linewidth=0.5,
        )
# Add error bars for standard deviation
ax8.errorbar(mode_strs2, average_emissions, yerr=std_emissions, fmt='.', color='black', ecolor='black', capsize=4, capthick=1, elinewidth=0.8)


plt.xticks(rotation=30, ha='right')

# Add gridlines for better readability
ax8.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.5)

# Add text annotations for each bar
ax8.set_ylabel('Emissions [kg CO2]')#, fontsize=12)
# ax8.set_xlabel('Mode of transport', fontsize=12)
# Set y-axis to start at 0
ax8.set_ylim(bottom=0)

# Add legend for median/mean bar types
ax8.legend(['Median', 'Mean'], loc='upper left')


fig8.tight_layout()

fig8.savefig(PATH_FIGS + 'national_emissions_pTravel_bar.png', dpi=300, bbox_inches='tight')




plt.show()

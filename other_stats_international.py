'''

    Before adding to emission inventory:
        - Add commuting (multiply by two to get yearly average-ish)
        - Multiply everything by two bc. of half year (and maybe a bit more to accomodate for missing Greenland-season?)



'''



import requests
import subprocess
import os
import time

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

# Define figure path
PATH_FIGS = 'Figures/International_BusinessTravels/'
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




# Load in all international data
international_bus = pd.read_csv('csv/international_bus_travels.csv')
international_carDriver = pd.read_csv('csv/international_carDriver_travels.csv')
international_carPassenger = pd.read_csv('csv/international_carPassenger_travels.csv')
international_train = pd.read_csv('csv/international_train_travels.csv')
international_plane = pd.read_csv('csv/international_plane_travels.csv')

# Divide 'electric' and 'petrol' cars into two separate dataframes
international_carDriver_electric = international_carDriver[international_carDriver['electric'] == 1]
international_carDriver_petrol = international_carDriver[international_carDriver['electric'] == 0]

# Divide 'electric' and 'petrol' cars into two separate dataframes
international_carPassenger_electric = international_carPassenger[international_carPassenger['electric'] == 1]
international_carPassenger_petrol = international_carPassenger[international_carPassenger['electric'] == 0]

all_international = [international_bus, international_carDriver_electric, international_carDriver_petrol, international_carPassenger_electric, international_carPassenger_petrol, international_train, international_plane]
mode_strs = ['Bus', 'CarDriverPetrol', 'CarDriverElectric', 'CarPassengerPetrol', 'CarPassengerElectric', 'Train', 'Plane']
mode_strs2 = ['Bus', 'Petrol car, driver', 'Electric car, driver', 'Petrol car, passenger', 'Electric car, passenger', 'Train', 'Plane']
N_strs = ['times', 'times', 'times', 'times', 'times', 'times', 'times']
# Select nice colors
colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'lightgreen', 'lightpink', 'lightblue']

# Go through dfs, and remove df if it is empty
all_int_nonempty = []
mode_strs_nonempty = []
N_strs_nonempty = []
colors_nonempty = []
for i, mode in enumerate(all_international):
    if not mode.empty:
        all_int_nonempty.append(mode)
        mode_strs_nonempty.append(mode_strs[i])
        N_strs_nonempty.append(N_strs[i])
        colors_nonempty.append(colors[i])





# Number of respondants (and how many where used in the analysis)
N_response = 123
N_use = 52
N_not_use = N_response - N_use
N_ENVS = 170
N_no_answer = N_ENVS - N_response

# Plot response rate as pie chart
labels = 'Travelled in last 1/2 year', 'No travel in last 1/2 year'
colors_YN = ['gold', 'lightgrey']
sizes = [N_use, N_not_use]
percentages = ["{0:.1%}".format(value / N_response) for value in sizes]

fig1, ax1 = plt.subplots(figsize=(8, 5))
fig1.suptitle(r'$\bf{International}$ $\bf{business}$ $\bf{travels}$' + f'\n(Answers: {N_response}, ENVS employees: {N_ENVS})')
ax1.pie(sizes,
        labels=percentages,
        startangle=90,
        colors=colors_YN,
        explode=[0.05, 0.05],
        )
ax1.legend(labels, loc=(1.02, 0.2), fontsize=12)

fig1.tight_layout()


# Save figure showing rate of employees that have travelled in the last 1/2 year 
fig1.savefig(PATH_FIGS + 'international_response_rate.png', dpi=600, bbox_inches='tight')


#####################
#                   #
# NUMBER OF TRAVELS #
#                   #
#####################

# Total number of travels with different modes of transport
# For each mode of transport, calculate the total number of travels
total_travels = []
print('\n\n')
print('#'*50)
print('INTERNATIONAL TRAVELS, NUMBER OF TRAVELS')
print('#'*50)
for i, mode in enumerate(all_international):
    print(f'\n\n{mode_strs[i]} travels:')
    print(mode[N_strs[i]].sum())

    total_travels.append(mode[N_strs[i]].sum())

# Go through lists and remove empty dataframes
total_travels_nonempty = []
mode_strs_nonempty = []
mode_strs2_nonempty = []
colors_nonempty = []
all_international_nonempty = []
for i, mode in enumerate(all_international):
    if not mode[N_strs[i]].sum() == 0:
        total_travels_nonempty.append(mode[N_strs[i]].sum())
        mode_strs_nonempty.append(mode_strs[i])
        mode_strs2_nonempty.append(mode_strs2[i])
        colors_nonempty.append(colors[i])
        all_international_nonempty.append(mode)

total_travels = total_travels_nonempty
mode_strs = mode_strs_nonempty
mode_strs2 = mode_strs2_nonempty
colors = colors_nonempty
all_international = all_international_nonempty



N_all = sum(total_travels)
percentages = ["{0:.1%}".format(value / N_all) for value in total_travels]

# Plot total number of travels with different modes of transport as pie chart
fig2, ax2 = plt.subplots()
fig2.suptitle(r'$\bf{International}$' + f'\nTotal number of travels N = {sum(total_travels)}\nDifferent modes of transport in [%]')
ax2.pie(total_travels,
        labels=percentages,
        startangle=90,
        colors=colors,
        )
ax2.legend(mode_strs, loc=(1.02, 0.25))

fig2.tight_layout()

# Save figure showing different modes of transport in terms of number of travels
fig2.savefig(PATH_FIGS + 'international_travels_pTransport_pie.png',
             dpi=600, bbox_inches='tight')











#######################
#                     #
# DISTANCES TRAVELLED #
#                     #
#######################

# Total distance travelled by each mode of transport
# For each mode of transport, calculate the total distance travelled
total_distances = []
print('\n\n')
print('#'*50)
print('INTERNATIONAL TRAVELS, DISTANCE TRAVELLED')
print('#'*50)
for i, mode in enumerate(all_international):
    print(f'\n\n{mode_strs[i]} travels, total sum:')
    print(mode['distance'].sum())
    total_distances.append(mode['distance'].sum())
percentages = ["{0:.1%}".format(value / sum(total_distances)) for value in total_distances]

# Exploding small slices of pie chart
explode = [0.15 if value < 0.005 * sum(total_distances) else 0 for value in total_distances]
# Plot total distance travelled by each mode of transport as pie chart
fig3, ax3 = plt.subplots(figsize=(8,5))
fig3.suptitle(r'$\bf{International}$' + f'\nTotal distance travelled = {sum(total_distances):.1f} km\nDifferent modes of transport in [%]')
ax3.pie(total_distances,
        labels=percentages,
        startangle=90,
        colors=colors,
        explode=explode
        )
# Add legend outside of plot showing mode names and distances
ax3.legend([f"{mode} ({dist:,.0f} km)" for mode, dist in zip(mode_strs2, total_distances)],
           loc="center left", bbox_to_anchor=(1.05, 0.5), title="Mode of Transport")#, fontsize=10)

fig3.tight_layout()

# Save figure showing different modes of transport in terms of distance travelled
fig3.savefig(PATH_FIGS + 'international_distance_pTransport_pie.png',
             dpi=600, bbox_inches='tight')


# # Average distance travelled by each mode of transport

# For each mode of transport, calculate the average and median distance travelled
average_distances = []
median_distances = []
std_distances = []
print('\n\n')
print('#'*50)
print('INTERNATIONAL TRAVELS, DISTANCE STATISTICS')
print('#'*50)
for i, mode in enumerate(all_international):
    print(f'\n\n{mode_strs[i]} travels:')
    # Mean and median also dependent on 'times' column
    average_array = mode['distance'] / mode[N_strs[i]]
    average = average_array.mean()
    median = average_array.median()
    std = average_array.std()

    print(f'Mean distance travelled per travel: {average:.1f} km')
    print(f'Median distance travelled per travel: {median:.1f} km')
    print(f'Standard deviation of distance travelled per travel: {std:.1f} km')

    average_distances.append(average)
    median_distances.append(median)
    std_distances.append(std)

# Plot in one bar chart (one bar per mode of transport)
fig4, ax4 = plt.subplots(figsize=(8,5))
fig4.suptitle(r'$\bf{International}$' + f'\nAverage distance travelled per travel, N = {N_all}')

# Allow for x-axis labels to be rotated for better readability
ax4.bar(mode_strs2,
        average_distances,
        color=colors,
        alpha=0.7,
        edgecolor='black',
        linewidth=0.5,
        )
ax4.bar(mode_strs2,
        median_distances,
        color=colors,
        alpha=0.3,
        edgecolor='black',
        linewidth=0.5,
        hatch='//'
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
ax4.legend(['Mean', 'Median'], loc='upper left')


fig4.tight_layout()


fig4.savefig(PATH_FIGS + 'international_distance_pTravel_bar.png', dpi=300, bbox_inches='tight')





# FOCUS ON PLANE TRAVELS #
# For plane travels, seperate into short-haul, medium-haul and long-haul distances and plot
international_plane_short = international_plane['short_haul']
international_plane_medium = international_plane['medium_haul']
international_plane_long = international_plane['long_haul']
# Print the column names

total_distances = [international_plane_short.sum(), international_plane_medium.sum(), international_plane_long.sum()]
percentages = ["{0:.1%}".format(value / sum(total_distances)) for value in total_distances]

print('\n\n')
print('#'*50)
print('INTERNATIONAL TRAVELS, PLANE TRAVEL TYPE DISTANCES')
print('#'*50)

print('\n\nPlane travels:')
print(f'Short-haul distance travelled: {international_plane_short.sum()} km')
print(f'Medium-haul distance travelled: {international_plane_medium.sum()} km')
print(f'Long-haul distance travelled: {international_plane_long.sum()} km')

plane_hauls = [international_plane_short, international_plane_medium, international_plane_long]

# Loop through plane hauls and calculate number of travels, average distance and median distance
print('\n\nPLANE TRAVELS, DISTANCE STATISTICS')
for i, plane_haul in enumerate(plane_hauls):
    print(f'\n{["Short-haul", "Medium-haul", "Long-haul"][i]}')
    # Number of travels is the count of non-zero values
    N_travels = plane_haul[plane_haul > 0].count()
    print(f'Number of travels: {N_travels}')
    # Mean and median computed based on N_travels and total_distances
    average = plane_haul.sum() / N_travels 
    print(f'Average distance travelled: {average:.1f} km')

# Calculate number of stop-overs

N_stopovers = international_plane['stops'].sum()
print(f'\nNumber of stop-overs: {N_stopovers}')
# See if any rows have more than 1 stop-over
print(f'\nNumber of travels with more than 1 stop-over: {international_plane[international_plane["stops"] > 1].shape[0]}')



# Plot plane travels as pie chart
fig7, axs7 = plt.subplots(figsize=(10,5))
fig7.suptitle(r'$\bf{International}$' + '\nPlane travels\nShort, medium and long haul in [%]')
axs7.pie([international_plane_short.sum(), international_plane_medium.sum(), international_plane_long.sum()],
        labels=percentages,
        startangle=90,
        colors=['lightcoral', 'lightskyblue', 'lightgreen'],
        )

# Add legend with distance travelled for each category
axs7.legend([f"Short-haul, < 1500 km ({international_plane_short.sum():,.0f} km)", f"Medium-haul, 1500-4000 km ({international_plane_medium.sum():,.0f} km)", f"Long-haul, > 4000 km ({international_plane_long.sum():,.0f} km)"], loc=(1.02, 0.25))

fig7.tight_layout()

fig7.savefig(PATH_FIGS + 'international_plane_haul_pie.png',
             dpi=600, bbox_inches='tight')


# Make a plot of the number of short, medium and long haul travels with plane
fig7, ax7 = plt.subplots(figsize=(10,7))
fig7.suptitle(r'$\bf{International}$' + '\nPlane travels\nShort, medium and long haul')


# Compute percentage of number of travels for each category
N_short = international_plane_short[international_plane_short > 0].count()
N_medium = international_plane_medium[international_plane_medium > 0].count()
N_long = international_plane_long[international_plane_long > 0].count()
N_total = N_short + N_medium + N_long

percentages = ["{0:.1%}".format(value / N_total) for value in [N_short, N_medium, N_long]]

# Plot pie chart with number of short, medium and long haul travels
ax7.pie([N_short, N_medium, N_long],
        labels=percentages,
        startangle=90,
        colors=['lightcoral', 'lightskyblue', 'lightgreen'],
        counterclock=False
        )

# Add legend with number of travels for each category
ax7.legend([f"Short-haul, < 1500 km ({N_short*2})", f"Medium-haul, 1500-4000 km ({N_medium*2})", f"Long-haul, > 4000 km ({N_long*2})"], loc=(1.02, 0.25))

fig7.tight_layout()
fig7.savefig(PATH_FIGS + 'international_plane_haul_pie_N.png', dpi=600, bbox_inches='tight')
plt.show()


#############
#           #
# EMISSIONS #
#           # 
#############

# Total emissions per mode of transport
# For each mode of transport, calculate the total emissions
total_emissions = []
print('\n\n')
print('#'*50)
print('INTERNATIONAL TRAVELS, TOTAL EMISSIONS')
print('#'*50)
for i, mode in enumerate(all_international):
    print(f'\n\n{mode_strs[i]} travels:')
    print(mode['emissions'].sum())
    total_emissions.append(mode['emissions'].sum())
percentages = ["{0:.1%}".format(value / sum(total_emissions)) for value in total_emissions]

explode = [0.07 if value < 0.05 * sum(total_emissions) else 0 for value in total_emissions]
explode[0] = 0.2
# Plot total emissions by each mode of transport as pie chart
fig5, ax5 = plt.subplots(figsize=(8,5))
fig5.suptitle(r'$\bf{International}$' + f'\nTotal emissions = {sum(total_emissions):.1f} kg CO2\nDifferent modes of transport in [%]')
ax5.pie(total_emissions,
        labels=percentages,
        startangle=90,
        counterclock=False,
        colors=colors,
        explode=explode,
        labeldistance=1.1
        )
ax5.legend(mode_strs2,loc='center right', bbox_to_anchor=(0, 0.5), title=r'$\bf{Mode}$ $\bf{of}$ $\bf{transport}$')
fig5.tight_layout()

fig5.savefig(PATH_FIGS + 'international_emissions_pTransport_pie.png',
             dpi=600, bbox_inches='tight')


# For each mode of transport, calculate the average and median emissions
average_emissions = []
median_emissions = []
std_emissions = []

print('\n\n')
print('#'*50)
print('INTERNATIONAL TRAVELS, EMISSION STATISTICS')
print('#'*50)
for i, mode in enumerate(all_international):
    print(f'\n\n{mode_strs[i]} travels:')
    # Mean and median also based on 'times' column
    average_array = mode['emissions'] / mode[N_strs[i]]
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
fig8.suptitle(r'$\bf{International}$' + f'\nAverage emissions per travel, N = {N_all}')

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

fig8.savefig(PATH_FIGS + 'international_emissions_pTravel_bar.png', dpi=300, bbox_inches='tight')


# FOCUS ON PLANE TRAVELS #
# For plane travels, seperate into short-haul, medium-haul, long-haul and stop-overs emissions and plot
international_plane_short = international_plane['emissions_short']
international_plane_medium = international_plane['emissions_medium']
international_plane_long = international_plane['emissions_long']
international_plane_stop = international_plane['emissions_stopovers']

total_emissions = [international_plane_short.sum(), international_plane_medium.sum(), international_plane_long.sum(), international_plane_stop.sum()]

print('\n\n')
print('#'*50)
print('INTERNATIONAL TRAVELS, PLANE TYPE TOTAL EMISSION')
print('#'*50)

print(f'\nShort-haul plane emissions: {international_plane_short.sum()} kg CO2')
print(f'Medium-haul plane emissions: {international_plane_medium.sum()} kg CO2')
print(f'Long-haul plane emissions: {international_plane_long.sum()} kg CO2')
print(f'Stop-over plane emissions: {international_plane_stop.sum()} kg CO2')


# Calculate average emissions per travel for each plane type:
print('\n\nPLANE TRAVELS, EMISSION STATISTICS')
for i, plane_haul in enumerate([international_plane_short, international_plane_medium, international_plane_long, international_plane_stop]):
    str_name = ["Short-haul", "Medium-haul", "Long-haul", "Stop-overs"][i]
    print(f'\n{str_name}')
    # Number of travels is the count of non-zero values
    N_travels = plane_haul[plane_haul > 0].count()
    if str_name == 'Stop-overs':
        print(f'Number of travels with stopovers: {N_travels}')
        print(f'Number of stop-overs in total: {N_stopovers}')
    else:
        print(f'Number of travels: {N_travels}')
    # Mean and median computed based on N_travels and total_distances
    average = plane_haul.sum() / N_travels 
    print(f'Average emissions per travel: {average:.1f} kg CO2')

percentages = ["{0:.1%}".format(value / sum(total_emissions)) for value in total_emissions]

# Plot plane emissions as pie chart
fig8, axs8 = plt.subplots(figsize=(8,5))
fig8.suptitle(r'$\bf{International}$' + '\nPlane emissions\nShort, medium, long haul and stop-overs in [%]')
axs8.pie([international_plane_short.sum(), international_plane_medium.sum(), international_plane_long.sum(), international_plane_stop.sum()],
        labels=percentages,
        startangle=90,
        colors=['lightcoral', 'lightskyblue', 'lightgreen', 'lightpink'],
        )
axs8.legend(['Short-haul', 'Medium-haul', 'Long-haul', 'Stop-overs'], loc=(1.02, 0.25))

fig8.tight_layout()

fig8.savefig(PATH_FIGS + 'international_plane_emissions_pie.png',
                dpi=600, bbox_inches='tight')


plt.close('all')

##################################################
#                                                #
# COMPARISON WITH SPENT-BASED EMISSION INVENTORY #
#                                                #
##################################################


emissions_spent = 1824.56  # t CO2
emissions_national = 36.096  # t CO2
emissions_international = 229.28 # t CO2

# Plot comparison of emissions from spent-based inventory and survey (bar plot on top of each other)
fig9, ax9 = plt.subplots(figsize=(8,5))
fig9.suptitle(r'$\bf{Comparison}$')

# Plot spent-based inventory emissions
ax9.barh('Spent-based inventory\n(2022)', emissions_spent, color='palegreen', alpha=0.9, edgecolor='black', linewidth=0.5, label=f'{emissions_spent:.2f} t CO2')
# Plot survey emissions
ax9.barh('International emissions, survey\n(autumn 2023 - spring 2024)', emissions_international, color='sandybrown', alpha=0.9, edgecolor='black', linewidth=0.5, label=f'{emissions_international:.2f} t CO2')
# Plot national emissions
ax9.barh('National emissions, survey\n(autumn 2023 - spring 2024)', emissions_national, color='thistle', alpha=0.9, edgecolor='black', linewidth=0.5, label=f'{emissions_national:.2f} t CO2')

ax9.set_xlabel('Emissions [t CO2]')

ax9.legend()

# Rotate x-axis labels for better readability
# plt.xticks(rotation=30, ha='right')

# Set gridlines for better readability
ax9.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.5)


fig9.tight_layout()

fig9.savefig(PATH_FIGS + 'survey_v_spentbased_emissions.png', dpi=300, bbox_inches='tight')





# Make dataframe with Scope 1, 2, and 3 with categories:
# Scope 1: Fuel (105.4136839 t CO2)
# Scope 2: Electricity (828.9156931 t CO2), Water (0.539779112 t CO2), Heat (85.9096697 t CO2)
# Scope 3: Shipping_costs (91.97 t CO2), Hardware_and_IT_equipment (93.28 t CO2), Catering (175.76 t CO2), Hotel (218.77 t CO2), Maintenance (145.52 t CO2), Travel_expenses (1824.56 t CO2), Purchases_services (918.61 t CO2), Purchases_goods (933.79 t CO2)

df_scope = pd.DataFrame({'Category': ['Fuel', 'Electricity', 'Water', 'Heat', 'Shipping costs', 'Hardware and IT equipment', 'Catering', 'Hotel', 'Maintenance', 'Travel expenses', 'Purchases services', 'Purchases goods'],
                         'Emissions': [105.4136839, 828.9156931, 0.539779112, 85.9096697, 91.97, 93.28, 175.76, 218.77, 145.52, 1824.56, 918.61, 933.79],
                         'Scope': ['Scope 1', 'Scope 2', 'Scope 2', 'Scope 2', 'Scope 3', 'Scope 3', 'Scope 3', 'Scope 3', 'Scope 3', 'Scope 3', 'Scope 3', 'Scope 3']})

cat_names = ['S1: Fuel', 'S2: Electricity', 'S2: Water', 'S2: Heat', 'S3: Shipping costs', 'S3: Hardware and IT equipment', 'S3: Catering', 'S3: Hotel', 'S3: Maintenance', 'S3: Travel expenses', 'S3: Purchases, services', 'S3: Purchases, goods']
cat_names_2 = ['Fuel', 'Electricity', 'Water', 'Heat', 'Shipping costs', 'Hardware and IT equipment', 'Catering', 'Hotel', 'Maintenance', 'Travel expenses', 'Purchases, services', 'Purchases, goods']

# Set colors to different shades of yellow, red and blue
colors = ['gold', 'lightcoral', 'lightsalmon', 'peachpuff', 'lightblue', 'skyblue', 'lightsteelblue', 'powderblue', 'lightcyan', 'paleturquoise', 'aliceblue', 'lavender']
explode = [0.1 if value < 0.01 * df_scope['Emissions'].sum() else 0 for value in df_scope['Emissions']]
explode[2] = 0.2
explode[4] = 0.1

# Plot all scopes in one pie chart
fig10, ax10 = plt.subplots(figsize=(13,8))
fig10.suptitle(r'$\bf{Scope}$' + f'\nTotal emissions = {df_scope["Emissions"].sum():.1f} t CO2\nDifferent scopes in [%]')
ax10.pie(df_scope['Emissions'],
         labels=["{0:.1%}".format(value / df_scope['Emissions'].sum()) for value in df_scope['Emissions']],
         startangle=90,
         counterclock=False,
         colors= colors,
         explode=explode,
         )
ax10.legend(cat_names, loc=(1.1, 0.25))

fig10.tight_layout()


# Plot all scopes in one bar chart (three different colors, one color for each scope) horizontally
fig11, ax11 = plt.subplots(figsize=(13,6))
fig11.suptitle(r'$\bf{Scope}$' + f'\nTotal emissions = {df_scope["Emissions"].sum():.1f} t CO2')

# Plot Scope 1 as gold and horizontal, with equidistant space between categories
y_pos_1 = np.arange(len(df_scope['Category'][df_scope['Scope'] == 'Scope 1']))
ax11.barh(y_pos_1,
          df_scope['Emissions'][df_scope['Scope'] == 'Scope 1'],
          color='gold', alpha=0.7, edgecolor='black', linewidth=0.5)

# Plot Scope 2 as lightcoral and horizontal, with equidistant space between categories and empty space between Scope 2 and Scope 3
y_pos_2 = np.arange(len(df_scope['Category'][df_scope['Scope'] == 'Scope 2'])) + len(df_scope['Category'][df_scope['Scope'] == 'Scope 1']) + 1
ax11.barh(y_pos_2,
          df_scope['Emissions'][df_scope['Scope'] == 'Scope 2'],
          color='lightcoral', alpha=0.7, edgecolor='black', linewidth=0.5)

# Plot Scope 3 as lightblue
y_pos_3 = np.arange(len(df_scope['Category'][df_scope['Scope'] == 'Scope 3'])) + len(df_scope['Category'][df_scope['Scope'] == 'Scope 1']) + len(df_scope['Category'][df_scope['Scope'] == 'Scope 2']) + 2
ax11.barh(y_pos_3,
          df_scope['Emissions'][df_scope['Scope'] == 'Scope 3'],
          color='lightblue', alpha=0.7, edgecolor='black', linewidth=0.5)

# Set the ticks to be cat names
y_pos = np.concatenate((y_pos_1, y_pos_2, y_pos_3))
ax11.set_yticks(y_pos, cat_names_2)

ax11.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.5)

ax11.set_xlabel('Emissions [t CO2]')
plt.xticks(rotation=30, ha='right')
ax11.legend(['Scope 1', 'Scope 2', 'Scope 3'])
        
fig11.tight_layout()


# Plot the sum of emissions for each scope as bar chart
fig12, ax12 = plt.subplots(figsize=(8,5))
fig12.suptitle(r'$\bf{Scope}$' + f'\nTotal emissions = {df_scope["Emissions"].sum():.1f} t CO2')

# Plot Scope 1 as gold
ax12.barh('Scope 1', df_scope['Emissions'][df_scope['Scope'] == 'Scope 1'].sum(), color='gold', alpha=0.7, edgecolor='black', linewidth=0.5)
# Plot Scope 2 as lightcoral
ax12.barh('Scope 2', df_scope['Emissions'][df_scope['Scope'] == 'Scope 2'].sum(), color='lightcoral', alpha=0.7, edgecolor='black', linewidth=0.5)
# Plot Scope 3 as lightblue
ax12.barh('Scope 3', df_scope['Emissions'][df_scope['Scope'] == 'Scope 3'].sum(), color='lightblue', alpha=0.7, edgecolor='black', linewidth=0.5)

ax12.set_xlabel('Emissions [t CO2]')

ax12.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.5)
fig12.tight_layout()







# Save figures
fig10.savefig(PATH_FIGS + 'scope_pie.png', dpi=600, bbox_inches='tight')
fig11.savefig(PATH_FIGS + 'scope_bar.png', dpi=600, bbox_inches='tight')
fig12.savefig(PATH_FIGS + 'scope_sum_bar.png', dpi=600, bbox_inches='tight')



plt.show()
#plt.close('all')
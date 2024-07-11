'''
    Script to plot destinations of business travels on maps
'''

import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point
from mpl_toolkits.basemap import Basemap

# Read the .csv files with destination coordinates
national_destinations = pd.read_csv('national_destinations.csv')
international_destinations = pd.read_csv('international_destinations.csv')



# Initialize the figure and basemap
fig, axs = plt.subplots(1, 2, figsize=(12, 8))

# Basemap of Denmark
lats_dk = [54.5, 58]
lons_dk = [8, 14]
m = Basemap(projection='merc', llcrnrlat=lats_dk[0], urcrnrlat=lats_dk[1], llcrnrlon=lons_dk[0], urcrnrlon=lons_dk[1], resolution='i', ax=axs[0])
m.drawmapboundary(fill_color='lightcyan')
m.fillcontinents(color='ForestGreen', lake_color='lightcyan', alpha=0.35)
m.drawcoastlines(linewidth=0.1)
m.drawcountries(linewidth=0.2)

plot_city_labels = ['København', 'Ølstykke', 'Helsingør', 'Sjællands Odde', 'Sorø', 'Køge',
                    'København', 'Odense', 'Nyborg', 'Svendborg', 'Fredericia', 'Vejle', 'Sønderborg',
                    'Esbjerg', 'Aarhus', 'Silkeborg', 'Herning', 'Viborg', 'Skive', 'Aalborg']
# Plot each city on the map
for index, row in national_destinations.iterrows():
    x, y = m(row['Longitude'], row['Latitude'])
    # Add city labels
    if row['Destination'] in plot_city_labels:
        m.plot(x, y, 'o', markersize=3, color='navy')
        axs[0].text(x, y+3500, row['Destination'], fontsize=8, ha='center', va='bottom', color='navy')
    else:
        m.plot(x, y, 'o', markersize=2, color='navy', alpha=0.5)
    
axs[0].set_title('National Travel Destinations')


# Basemap of Sjælland
lats = [55.2, 56.15]
lons = [11.05, 12.7]
m2 = Basemap(projection='merc', llcrnrlat=lats[0], urcrnrlat=lats[1], llcrnrlon=lons[0], urcrnrlon=lons[1], resolution='i', ax=axs[1])
m2.drawmapboundary(fill_color='lightcyan')
m2.fillcontinents(color='ForestGreen', lake_color='lightcyan', alpha=0.35)
m2.drawcoastlines(linewidth=0.1)
m2.drawcountries(linewidth=0.2)

plot_city_labels = ['København', 'Roskilde', 'Helsingør', 'Sjællands Odde', 'Flakkebjerg', 'Slagelse',
                    'Korsør', 'Sorø', 'Køge', 'Hundested', 'Lejre', 'Hvalsø', 'Risø', 'DTU Lyngby',
                    'København', 'Taastrup', 'Greve', 'Ølstykke', 'Tårnby', 'Vedskølle']
# Plot each city (within Sjælland) on the map
for index, row in national_destinations.iterrows():
    # Check if the city is located in Sjælland
    if (lats[0] <= row['Latitude'] <= lats[1]) and (lons[0] <= row['Longitude'] <= lons[1]):
        x2, y2 = m2(row['Longitude'], row['Latitude'])

        if row['Destination'] in plot_city_labels:
            m2.plot(x2, y2, 'o', markersize=3, color='navy')
            axs[1].text(x2, y2+2000, row['Destination'], fontsize=8, ha='center', va='bottom', color='navy')
        else:
            m2.plot(x2, y2, 'o', markersize=2, color='navy', alpha=0.5)
        
axs[1].set_title('National Travel Destinations in Sjælland')

fig.tight_layout()
fig.savefig('Figures/national_destinations_map.png', dpi=300, bbox_inches='tight')


# International destinations (Europe) with Basemap
fig, ax = plt.subplots(1, figsize=(12, 8))
# Basemap of Europe
lats_eu = [35, 70]
lons_eu = [-10, 30]
m3 = Basemap(projection='merc', llcrnrlat=lats_eu[0], urcrnrlat=lats_eu[1], llcrnrlon=lons_eu[0], urcrnrlon=lons_eu[1], resolution='i', ax=ax)
m3.drawmapboundary(fill_color='lightcyan')
m3.fillcontinents(color='ForestGreen', lake_color='lightcyan', alpha=0.35)
m3.drawcoastlines(linewidth=0.1)
m3.drawcountries(linewidth=0.2)

plot_city_labels = ['København', 'Thorshavn', 'Ålesund', 'Oslo', 'Oulu', 'Umeå', 'Bergen', 'Stockholm',
                    'Helsinki', 'Edinburgh', 'Newcastle', 'Dublin', 'London', 'Hamburg', 'Berlin', 'Utrecht', 
                    'Bruxelles', 'München', 'Paris', 'Wien', 'Geneva', 'Grenoble', 'Milan', 'Venedig',
                    'Toulouse', 'Spain', 'Faro', 'Innsbruck', 'Leipzig']
# Plot each city (within Sjælland) on the map
for index, row in international_destinations.iterrows():
    # Check if the city is located in Sjælland
    if (lats_eu[0] <= row['Latitude'] <= lats_eu[1]) and (lons_eu[0] <= row['Longitude'] <= lons_eu[1]):
        x3, y3 = m3(row['Longitude'], row['Latitude'])

        if row['Destination'] in plot_city_labels:
            m3.plot(x3, y3, 'o', markersize=3, color='navy')
            if row['Destination'] in ['Grenoble', 'Venedig', 'København', 'Stockholm', 'Innsbruck']:
                ax.text(x3, y3-10000, row['Destination'], fontsize=8, ha='center', va='top', color='navy')
            else:
                ax.text(x3, y3+10000, row['Destination'], fontsize=8, ha='center', va='bottom', color='navy')
        else:
            m3.plot(x3, y3, 'o', markersize=2, color='navy', alpha=0.5)
        
ax.set_title('European travels')

fig.tight_layout()
fig.savefig('Figures/european_destinations_map.png', dpi=300, bbox_inches='tight')






# International destinations (World) with Basemap
fig, ax = plt.subplots(1, figsize=(12, 8))
# Basemap of the world
m4 = Basemap(projection='merc', llcrnrlat=-60, urcrnrlat=85, llcrnrlon=-180, urcrnrlon=180, resolution='i', ax=ax)
m4.drawmapboundary(fill_color='lightcyan')
m4.fillcontinents(color='ForestGreen', lake_color='lightcyan', alpha=0.35)
m4.drawcoastlines(linewidth=0.1)
m4.drawcountries(linewidth=0.2)

plot_city_labels = ['San Francisco', 'Banff', 'Athen', 'Florianopolis', 'Australine', 'Shanghai',
                    'Station Nord', 'Nuuk', 'Heraklion', 'Cyprus', 'Marrakesh', 'Faro', 'Berlin'
                    'Paris', 'Toulouse', 'København', 'Thorshavn', 'Oslo', 'Oulu', 'Edinburgh', 
                    'Venedig', 'longyearbyen']

# Plot each city (within Sjælland) on the map
for index, row in international_destinations.iterrows():
    x4, y4 = m4(row['Longitude'], row['Latitude'])

    if row['Destination'] in plot_city_labels:
        m4.plot(x4, y4, 'o', markersize=3, color='navy')
        if row['Destination'] in ['København', 'Venedig', 'Marrakesh', 'Faro']:
            ax.text(x4, y4-50000, row['Destination'], fontsize=9, ha='center', va='top', color='navy')
        else:
            ax.text(x4, y4+50000, row['Destination'], fontsize=9, ha='center', va='bottom', color='navy')
    else:
        m4.plot(x4, y4, 'o', markersize=2, color='navy', alpha=0.5)

fig.tight_layout()
fig.savefig('Figures/worldwide_destinations_map.png', dpi=300, bbox_inches='tight')



plt.show()




# geometry_europe =[Point(lonlat) for lonlat in zip(international_destinations['Longitude'], international_destinations['Latitude'])]
# gdf_europe = gpd.GeoDataFrame(international_destinations, geometry=geometry_europe)

# # Create plot with world map
# fig, ax = plt.subplots(1, 1, figsize=(12, 8))
# world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
# world.boundary.plot(ax=ax, linewidth=1)

# # Define the region of Europe
# region_europe = gdf_europe.cx[-10:30, 35:70]
# # Omit Denmark from the European destinations
# region_europe = region_europe[region_europe['Destination'] != 'København']

# # Plot the European destinations
# region_europe.plot(ax=ax, color='red', markersize=20)

# for x, y, label in zip(region_europe.geometry.x, region_europe.geometry.y, region_europe['Destination']):
#     ax.text(x, y, label, fontsize=8, ha='right')

# ax.set_title('International Travel Destinations in Europe')
# ax.set_xlabel('Longitude')
# ax.set_ylabel('Latitude')

# # Set the plot limits to focus on Europe
# ax.set_xlim(-10, 30)
# ax.set_ylim(35, 70)




# plt.show()






# # Setting the map type
# world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))




# # Create a plot for national destinations
# lons_use = [8, 13]
# lats_use = [54.5, 58]

# fig, ax = plt.subplots(1, 1, figsize=(10, 10))
# world.boundary.plot(ax=ax, linewidth=1)


# # Set the plot limits to focus on Denmark
# ax.set_xlim(lons_use[0], lons_use[1])
# ax.set_ylim(lats_use[0], lats_use[1])

# # Set the title and labels
# ax.set_title('National Travel Destinations')
# ax.set_xlabel('Longitude')
# ax.set_ylabel('Latitude')

# plt.show()


# print(national_destinations)




# # Plot the destinations on maps, one for national and one for international travel
# def plot_travel_destinations(df, title, ax, world=gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))):
#     '''
#         Plot travel destinations on a map
#     '''
#     gdf = gpd.GeoDataFrame(df, geometry=[Point(lonlat) for lonlat in zip(df['Longitude'], df['Latitude'])])
#     world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

#     # Plotting
#     world.plot(ax=ax, color='white', edgecolor='black')
#     gdf.plot(ax=ax, color='red', markersize=20)

#     for x, y, label in zip(gdf.geometry.x, gdf.geometry.y, gdf['Destination']):
#         print(gdf['Destination'])
#         ax.text(x, y, label, fontsize=8, ha='right')

#     ax.set_title(title)
#     ax.set_xlabel('Longitude')
#     ax.set_ylabel('Latitude')


# # Plot national destinations on Denmark map
# fig, ax = plt.subplots(1, 1, figsize=(20, 10))
# plot_travel_destinations(national_destinations, 'National Travel Destinations', ax,)



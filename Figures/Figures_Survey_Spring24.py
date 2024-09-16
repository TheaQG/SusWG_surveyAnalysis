import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap

#####################
# COMMUTING TO RISØ #
#####################

# Risø's latitude and longitude
riso_lat, riso_lon = 55.6953, 12.0876

# Initialize the figure and basemap
fig = plt.figure(figsize=(10, 8))
m = Basemap(projection='merc', llcrnrlat=54.5, urcrnrlat=58, llcrnrlon=8, urcrnrlon=15, resolution='i')
#m.drawmapboundary(fill_color='aqua')
m.fillcontinents(color='ForestGreen', lake_color='aqua', alpha=0.3)
m.drawcoastlines()
m.drawcountries()


# Convert Risø's lat and lon to x and y on the map
xpt, ypt = m(riso_lon, riso_lat)
m.plot(xpt, ypt, 'ro')  # Mark Risø's location
plt.text(xpt, ypt, 'Risø', fontsize=9, ha='center', va='bottom', color='white', fontweight='bold')


# List of European capitals with their latitudes and longitudes
cities = {
    'Copenhagen': (55.6761, 12.5683),  # Copenhagen included as reference
    'Aarhus': (56.1629, 10.2039),
    'Odense': (55.4038, 10.4024),
    'Aalborg': (57.0488, 9.9217),
    'Esbjerg': (55.4667, 8.4500),
    'Roskilde': (55.6415, 12.0803),
    'Helsingør': (56.0365, 12.6136),
    'Kalundborg': (55.6915, 11.0896),
    'Køge': (55.4586, 12.1825),
    'Næstved': (55.2249, 11.7609),
    'Nyborg': (55.3122, 10.7896),
    'Nykøbing Falster': (54.7723, 11.8688),
    'Middelfart': (55.5050, 9.7300),
}

# Plot each capital on the map
for city, (lat, lon) in cities.items():
    x, y = m(lon, lat)
    m.plot(x, y, 'r.')  # red dot for each capital
    # Plot with a little space 
    if city == 'Esbjerg' or city == 'Copenhagen' or city == 'Middelfart' or city == 'Odense':
        plt.text(x, y, city, fontsize=9, ha='left', va='bottom', color='white')
    else:
        plt.text(x, y, city, fontsize=9, ha='left', va='top', color='white')#, fontweight='bold')




# Draw and fill circles for commuting zones
zones = [15, 35, 55, 90, 140, 220, 300]  # Extended zones to cover potential commuters from farther areas
colors = ['green', 'yellow', 'orange', 'red', 'purple', 'blue', 'cyan']  # Colors for different zones
for i, radius in enumerate(zones):
    # The number 111.12 is used for converting kilometers to degrees (approximate)
    # Decrease alpha value to make bands semi-transparent
    m.tissot(riso_lon,
             riso_lat,
             radius/111.12,
             100,
             facecolor=colors[i],
             edgecolor='none',
             alpha=0.3)
    
for i, radius in enumerate(zones):
    m.tissot(riso_lon,
             riso_lat,
             radius/111.12,
             100,
             facecolor='none',
             edgecolor='k')

plt.text(xpt, ypt+0.45e5, '1', fontsize=8, ha='center', va='center', bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))
plt.text(xpt, ypt+0.8e5, '2', fontsize=8, ha='center', va='center', bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))
plt.text(xpt, ypt+1.3e5, '3', fontsize=8, ha='center', va='center', bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))
plt.text(xpt, ypt+2.05e5, '4', fontsize=8, ha='center', va='center', bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))
plt.text(xpt, ypt+3.25e5, '5', fontsize=8, ha='center', va='center', bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))
plt.text(xpt, ypt+4.4e5, '6', fontsize=8, ha='center', va='center', bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))

#fig.savefig('Commuting_to_Risø_DK.png', dpi=600)


plt.close()










#############################
# EUROPEAN BUSINESS TRAVELS #
#############################


# Initialize the figure and basemap with chosen projection
fig = plt.figure(figsize=(10, 10))
m = Basemap(projection='merc', llcrnrlat=35, urcrnrlat=70, llcrnrlon=-12, urcrnrlon=35, resolution='i')
#m.drawmapboundary(fill_color='aqua')
m.fillcontinents(color='ForestGreen', lake_color='aqua', alpha=0.15)
m.drawcoastlines(linewidth=1.5)
m.drawcountries(linewidth=1.1)

# Sector labels and their positions (adjust as needed)
# This assumes 16 sectors for simplicity, adjust according to your actual sector count
sector_labels = list('ABCDEFGHIJKLMNOP')
num_sectors = len(sector_labels)



# Copenhagen's latitude and longitude
cph_lat, cph_lon = 55.6761, 12.5683
# Convert Risø's lat and lon to x and y on the map
xpt, ypt = m(cph_lon, cph_lat)
m.plot(xpt, ypt, 'bo')  # Mark Copenhagen's location

x_offsets = [1e5]
y_offsets = [1e6]  

plt.text(xpt+2.5e5, ypt+3.8e6, 'A', fontsize=12, ha='center', va='center', bbox=dict(facecolor='white', alpha=0.7))
plt.text(xpt+1.5e6, ypt+3.8e6, 'B', fontsize=12, ha='center', va='center', bbox=dict(facecolor='white', alpha=0.7))
plt.text(xpt+2.7e6, ypt+2.4e6, 'C', fontsize=12, ha='center', va='center', bbox=dict(facecolor='white', alpha=0.7))
plt.text(xpt+2.7e6, ypt+.6e6, 'D', fontsize=12, ha='center', va='center', bbox=dict(facecolor='white', alpha=0.7))
plt.text(xpt+2.7e6, ypt-.5e6, 'E', fontsize=12, ha='center', va='center', bbox=dict(facecolor='white', alpha=0.7))
plt.text(xpt+2.7e6, ypt-1.65e6, 'F', fontsize=12, ha='center', va='center', bbox=dict(facecolor='white', alpha=0.7))
plt.text(xpt+2e6, ypt-3.55e6, 'G', fontsize=12, ha='center', va='center', bbox=dict(facecolor='white', alpha=0.7))
plt.text(xpt+.4e6, ypt-3.55e6, 'H', fontsize=12, ha='center', va='center', bbox=dict(facecolor='white', alpha=0.7))
plt.text(xpt-1.35e6, ypt-3.55e6, 'I', fontsize=12, ha='center', va='center', bbox=dict(facecolor='white', alpha=0.7))
plt.text(xpt-2.9e6, ypt-2.55e6, 'J', fontsize=12, ha='center', va='center', bbox=dict(facecolor='white', alpha=0.7))
plt.text(xpt-2.9e6, ypt-1.1e6, 'K', fontsize=12, ha='center', va='center', bbox=dict(facecolor='white', alpha=0.7))
plt.text(xpt-2.9e6, ypt-.2e5, 'L', fontsize=12, ha='center', va='center', bbox=dict(facecolor='white', alpha=0.7))
plt.text(xpt-2.9e6, ypt+1.6e6, 'M', fontsize=12, ha='center', va='center', bbox=dict(facecolor='white', alpha=0.7))
plt.text(xpt-2.1e6, ypt+3.8e6, 'N', fontsize=12, ha='center', va='center', bbox=dict(facecolor='white', alpha=0.7))
plt.text(xpt-.6e6, ypt+3.8e6, 'O', fontsize=12, ha='center', va='center', bbox=dict(facecolor='white', alpha=0.7))

# Draw and fill circles for commuting zones
zones = [200, 400, 700, 1000, 1300, 1600, 1900, 2200, 2500, 2800]  # Extended zones to cover potential commuters from farther areas
zone_labels = [str(i) for i in range(1, len(zones) + 1)] # Labels for different zones
colors = ['green', 'yellow', 'orange', 'red', 'purple', 'blue', 'cyan', 'magenta', 'brown', 'black']  # Colors for different zones

zones.reverse()
colors.reverse()

for i, (radius, color) in enumerate(zip(zones, colors)):
    # The number 111.12 is used for converting kilometers to degrees (approximate)
    # Decrease alpha value to make bands semi-transparent
    m.tissot(cph_lon,
             cph_lat,
             radius/111.12,
             100,
             facecolor=color,
             edgecolor='none',
             alpha=0.3)
    


for i, radius in enumerate(zones):
    m.tissot(cph_lon,
             cph_lat,
             radius/111.12,
             100,
             facecolor='none',
             edgecolor='k')


angles = np.linspace(0, 2 * np.pi, 16)  # Create 16 lines equally spaced around the circle
for angle in angles:
    # Calculate the line's end point. 2000 km is used to ensure it goes beyond the last circle.
    # Convert distance to degrees
    end_lat = cph_lat + (2700 / 111.12) * np.sin(angle)
    end_lon = cph_lon + (2700 / 111.12) * np.cos(angle) / np.cos(np.radians(cph_lat))
    # Convert end points to map's x and y
    x_end, y_end = m(end_lon, end_lat)
    # Draw the line
    m.plot([xpt, x_end], [ypt, y_end], color='k', linewidth=1)


# List of European capitals with their latitudes and longitudes
capitals = {
    'Oslo': (59.9139, 10.7522),
    'Stockholm': (59.3293, 18.0686),
    'Helsinki': (60.1699, 24.9384),
    'Copenhagen': (55.6761, 12.5683),  # Copenhagen included as reference
    'Berlin': (52.5200, 13.4050),
    'London': (51.5074, -0.1278),
    'Paris': (48.8566, 2.3522),
    'Madrid': (40.4168, -3.7038),
    'Rome': (41.9028, 12.4964),
    'Vienna': (48.2082, 16.3738),
    'Prague': (50.0755, 14.4378),
    'Warsaw': (52.2297, 21.0122),
    'Budapest': (47.4979, 19.0402),
    'Brussels': (50.8503, 4.3517),
    'Amsterdam': (52.3676, 4.9041),
    'Dublin': (53.3498, -6.2603),
    'Edinburgh': (55.9533, -3.1883),
    'Lisboa': (38.7223, -9.1393),
    'Barcelona': (41.3851, 2.1734),
    'Ljubljana': (46.0569, 14.5058),
    'Zagreb': (45.8150, 15.9819),
    'Sarajevo': (43.8563, 18.4131),
    'Podgorica': (42.4304, 19.2594),
    'Athens': (37.9838, 23.7275),
    'Belgrade': (44.7866, 20.4489),
    'Sofia': (42.6977, 23.3219),
    'Tirana': (41.3275, 19.8187),
    'Skopje': (41.9973, 21.4280),
    'Bucharest': (44.4268, 26.1025),
    'Minsk': (53.9006, 27.5590),
    'Kiev': (50.4501, 30.5234),
    'Ankara': (39.9334, 32.8597),
    'Istanbul': (41.0082, 28.9784),
    'Tallinn': (59.4370, 24.7536),
    'Vilnius': (54.6872, 25.2797),
    'Riga': (56.9496, 24.1052),
    'Milan': (45.4642, 9.1900),
    'Palermo': (38.1157, 13.3615),
    'Zurich': (47.3769, 8.5417),
    'Bern': (46.9480, 7.4474),
    'Lyon': (45.7640, 4.8357),
    'Manchester': (53.4808, -2.2426),
    'Hamburg': (53.5511, 9.9937),
    'Frankfurt': (50.1109, 8.6821),
    'Cologne': (50.9375, 6.9603),
    'Munich': (48.1351, 11.5820),
    'Krakow': (50.0647, 19.9450),
    'Reykjavik': (64.1466, -21.9426),
    'Trondheim': (63.4305, 10.3951),
    'Uppsala': (59.8586, 17.6389),
    'Bergen': (60.3929, 5.3245),
    'Tromsö': (69.6492, 18.9553),
    'Murmansk': (68.9585, 33.0827),
    'Thorshavn': (62.0079, -6.7900)
    # Add more capitals if needed
}

# Plot each capital on the map
for city, (lat, lon) in capitals.items():
    x, y = m(lon, lat)
    m.plot(x, y, 'r.')  # red dot for each capital
    plt.text(x, y, city, fontsize=9, ha='right', va='bottom', color='white')#, fontweight='bold')



# Add space fpr legend on the right
legend_ax = fig.add_axes([0.85, 0.1, 0.03, 0.8])
legend_ax.axis('off')


import matplotlib.patches as mpatches

# Build the stacked color legend
legend_colors = ['#8d842b',
                 '#cb863e',
                 '#b5535a',
                 '#963082',
                 '#6945bb',
                 '#6063d5',
                 '#8a8ec4',
                 '#c65eab',
                 '#ae8888',
                 '#b2b2b2']
legend_colors.reverse()
for i, color in enumerate(legend_colors):
    # Each subsequent rectangle has a slightly reduced height to create a stacked effect
    legend_ax.add_patch(mpatches.Rectangle((0, 1-(i+1)/len(colors)), 1, 1/len(colors), color=color, ec="none"))
    # Add text label - the zone number
    legend_ax.text(1.05, 1-(i+0.5)/len(colors), f'Zone {len(zones)-i}', va='center')


# Save the figure
#fig.savefig('European_Business_Travels.png', dpi=600)
plt.close()

# fig.tight_layout()
##################################
# INTERNATIONAL BUSINESS TRAVELS #
##################################

# Initialize the figure and basemap with chosen projection
plt.figure(figsize=(16, 8))  # Adjust figure size to accommodate whole world map
m = Basemap(projection='robin', lon_0=0, resolution='c')  # Centered on the Prime Meridian
m.drawmapboundary(fill_color='aqua')
m.fillcontinents(color='ForestGreen', lake_color='aqua')
m.drawcoastlines()
m.drawcountries()

# Copenhagen's latitude and longitude
cph_lat, cph_lon = 55.6761, 12.5683


# Define regions with lists of countries (ISO ALPHA-3 country codes)
regions = {
    'Nordic Countries': ['DNK', 'FIN', 'ISL', 'NOR', 'SWE'],
    'Western Europe': ['AUT', 'BEL', 'FRA', 'DEU', 'IRL', 'LIE', 'LUX', 'MCO', 'NLD', 'CHE', 'GBR'],
    'Eastern Europe & Central Asia': ['ALB', 'ARM', 'AZE', 'BLR', 'BIH', 'BGR', 'HRV', 'CZE', 'EST', 'GEO', 'HUN', 'KAZ', 'KGZ', 'LVA', 'LTU', 'MKD', 'MDA', 'MNE', 'POL', 'ROU', 'RUS', 'SRB', 'SVK', 'SVN', 'TJK', 'TKM', 'UKR', 'UZB'],
    'Middle East & North Africa': ['DZA', 'BHR', 'EGY', 'IRN', 'IRQ', 'ISR', 'JOR', 'KWT', 'LBN', 'LBY', 'MAR', 'OMN', 'QAT', 'SAU', 'SYR', 'TUN', 'ARE', 'YEM'],
    'Sub-Saharan Africa': ['AGO', 'BEN', 'BWA', 'BFA', 'BDI', 'CMR', 'CPV', 'CAF', 'TCD', 'COM', 'COD', 'DJIB', 'GAB', 'GMB', 'GHA', 'GIN', 'GNB', 'CIV', 'KEN', 'LSO', 'LBR', 'MDG', 'MWI', 'MLI', 'MRT', 'MUS', 'MYT', 'MOZ', 'NAM', 'NER', 'NGA', 'REU', 'RWA', 'STP', 'SEN', 'SYC', 'SLE', 'SOM', 'ZAF', 'SSD', 'SDN', 'SWZ', 'TZA', 'TGO', 'UGA', 'ZMB', 'ZWE'],
    'South Asia': ['AFG', 'BGD', 'BTN', 'IND', 'MDV', 'NPL', 'PAK', 'LKA'],
    'East Asia & Oceania': ['AUS', 'BRN', 'KHM', 'CHN', 'FJI', 'IDN', 'JPN', 'KIR', 'LAO', 'MYS', 'MHL', 'FSM', 'MNG', 'MMR', 'NRU', 'NCL', 'NZL', 'PLW', 'PNG', 'PHL', 'PRK', 'KOR', 'WSM', 'SGP', 'SLB', 'THA', 'TLS', 'TON', 'TUV', 'VUT', 'VNM'],
    'Southeast Asia': ['BRN', 'KHM', 'IDN', 'LAO', 'MYS', 'MMR', 'PHL', 'SGP', 'THA', 'TLS', 'VNM'],
    'North America': ['ATG', 'BHS', 'BRB', 'BLZ', 'CAN', 'CRI', 'CUB', 'DMA', 'DOM', 'SLV', 'GRD', 'GTM', 'HTI', 'HND', 'JAM', 'MEX', 'NIC', 'PAN', 'STP', 'KNA', 'LCA', 'VCT', 'TTO', 'USA'],
    'Central America & the Caribbean': ['BLZ', 'CRI', 'SLV', 'GTM', 'HND', 'NIC', 'PAN'],
    'South America': ['ARG', 'BOL', 'BRA', 'CHL', 'COL', 'ECU', 'GUY', 'PRY', 'PER', 'SUR', 'URY', 'VEN']
}

# Colors for each region
region_colors = {
    'Nordic Countries': 'cyan',
    'Western Europe': 'blue',
    'Eastern Europe & Central Asia': 'purple',
    'Middle East & North Africa': 'orange',
    'Sub-Saharan Africa': 'green',
    'South Asia': 'red',
    'East Asia & Oceania': 'magenta',
    'Southeast Asia': 'lime',
    'North America': 'yellow',
    'Central America & the Caribbean': 'teal',
    'South America': 'brown'
}

# Color each region
for region, countries in regions.items():
    for country in countries:
        try:
            m.drawcountries(linewidth=1.25)
            m.drawmapboundary(fill_color='aqua')
            m.fillcontinents(color=region_colors[region], lake_color='aqua', alpha=0.3)
            m.drawcoastlines()
        except:
            print('Country code not recognized')
            pass  # If the country code is not recognized, skip it

plt.title('International Travel Zones from Copenhagen')

plt.show()









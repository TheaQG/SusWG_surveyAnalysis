# SusWG_surveyAnalysis

This is the repository for emission invetoring of the Department of Environmental Science business travels.

### Overview of the repository
- csv: Contains the data (mainly .csv files) used in the emission inventory
- figures: Contains code and figures generated in the emission inventory (so far only the map of the travels)
- create_destination_files.py: Script for creating the destination files ((lat, lon)coordinates for locations in survey) for the national_travels_emissions.py and international_travels_emissions.py scripts.
- international_travels_emissions.py: Script for calculating the emissions from international travels
- national_travels_emissions.py: Script for calculating the emissions from national travels
- SurveyAnalysis_BusinessTravel.py: ???
- SurveyAnalysis_BusinessTravel_maps.py: Script for creating the map of the travels
- suswg_env.yaml: Environment file for setting up the environment for running the scripts
- utils.py: Utility functions used in the emission inventory (Haversine distance calculation and OSRRM request)
- README.md: This file



### Setting up the environment
To be able to run the national_travels_emissions.py and international_travels_emissions.py scripts, you need to set up a osrm (Open Source Routing Machine) backend. The scripts use the OSRM backend to calculate the distance between two points. The distance is used to calculate the emissions from the travels.

1. Install Docker (e.g. from https://www.docker.com/products/docker-desktop) to avoid the need to install the osrm backend on your local machine.
2. Download the necessary map data: Download the ´.osm.pbf´ map file for the region of interested, e.g. from https://download.geofabrik.de/. Select country (or region) of interest, e.g. denmark-latest.osm.pbf or europe-latest.osm.pbf.
3. Set up OSRM with Docker. 
    1. Open a terminal and navigate to the folder where the .osm.pbf file is located.
    2. Pull the OSRM Docker backend image with ´docker pull osrm/osrm-backend´ 
    3. Prepare the map data (e.g. the denmark-latest.osm.pbf file) with ´docker run -t -v $(pwd):/data osrm/osrm-backend osrm-extract -p /opt/car.lua /data/denmark-latest.osm.pbf´
    4. Create routing data from the prepared data: ´docker run -t -v $(pwd):/data osrm/osrm-backend osrm-contract /data/denmark-latest.osrm´
4. Run the OSRM server: ´docker run -t -i -p 5000:5000 -v $(pwd):/data osrm/osrm-backend osrm-routed /data/denmark-latest.osrm´
5. Test the setup with a simple request: curl ´http://localhost:5000/route/v1/driving/10.2134046,56.1496278;12.520215144442094,55.785414450000005?overview=false´
    - This request calculates a route between Aarhus University and DTU Lyngby in meters.

The scripts should now be able to be executed without any problems. Run them (in an env corresponding to the ´suswg_env.yaml´-file) using ´python national_travels_emissions.py´ and ´python international_travels_emissions.py´.

### Work in progress:
- Cleaning up the code: Simplify code (especially in international_travels_emissions.py and national_travels_emissions.py) by looping through transportation types
- Make more general: Use the knowledge from this script to develop a general emission inventory script for business travels (e.g. input: excel file with travels, output: excel file with emissions)
- Make more advanced emissions calculations (emissions from planes different depending on distance, emissions from cars different depending on fuel type, etc.)
- Make the script more user-friendly: Add a GUI for inputting the data, add a GUI for selecting the map data, etc.
- Make OSRM setup easier: Make a script for setting up the OSRM backend
- Make figures: Make more figures, e.g. emissions per department, emissions per transportation type, etc.

- Add more data: Add more data to the emission inventory, e.g. emissions from food, emissions from electricity, etc.


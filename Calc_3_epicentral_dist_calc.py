# ------------------------------------------
# --- Author: Chanthujan Chandrakumar
# --- Date: 4/08/23
# --- Python Ver: 3.8
# ------------------------------------------

### Calculate distance between 2 coordinate points. Return the final file with the earthquake distance to the epicenter.

import pandas as pd
from math import radians, sin, cos, sqrt, atan2

# Function to calculate epicentral distance using haversine formula
def haversine(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    r = 6371.0  # Radius of the Earth in kilometers
    distance = r * c

    return distance

# Read data from csv sheet
csv_file = 'tables/eventTable/major_events_info.csv' #result form the code Calc_2_epicentre_info.py
df = pd.read_csv(csv_file)

# Calculate epicentral distance for each row
for index, row in df.iterrows():
    station_lat = row['station_lat']
    station_long = row['station_long']
    epi_lat = row['epi_lat']
    epi_long = row['epi_long']

    epicentral_distance = haversine(station_lat, station_long, epi_lat, epi_long)

    # Update epicentral_distance column in the DataFrame
    df.at[index, 'epicentral_distance'] = epicentral_distance

# Save the updated DataFrame back to Excel
df.to_csv('tables/eventTable/DATASET', index=False)  #you can change the name

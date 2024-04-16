# ------------------------------------------
# --- Author: Chanthujan Chandrakumar
# --- Date: 4/08/23
# --- Python Ver: 3.8
# ------------------------------------------

### Retrieve seismic station coordinates"

import time
import pandas as pd
from obspy.clients.fdsn import Client as FDSN_Client

def get_station_coordinates(client, station_name):
    try:
        inventory = client.get_stations(network="NZ", station=station_name, channel="*", starttime="2013-01-01 00:00:00.000",
                                        endtime="2022-12-31 23:59:59.000")
        #print(inventory)
        
        if len(inventory) > 0:
            network = inventory[0]
            for i in network:
                latitude = i.latitude
                longitude =i.longitude
                return latitude, longitude
        else:
            return None, None
    except Exception as e:
        print(f"Error getting coordinates for {station_name}: {e}")
        return None, None

time1=time.time()
# Read data from CSV sheet
csv_file = 'tables/eventTable/INPUTS.csv' #to change with your original file
df = pd.read_csv(csv_file)

# Initialize FDSN client
client = FDSN_Client("GEONET")
print(client)
# Loop through each row in the DataFrame
for index, row in df.iterrows():
    station_name = row['Station Name']
    latitude, longitude = get_station_coordinates(client, station_name)
    # Update station_lat and station_long columns in the DataFrame
    df.at[index, 'station_lat'] = latitude
    df.at[index, 'station_long'] = longitude

# Save updated DataFrame back to CSV
#df.to_excel('/Users/chanthujan/PycharmProjects/eco_system_db_com_EEW/s_wave_intensity_estimation/plots/epicentre_distance_est/major_eq_details_with_station_coordinates.xlsx', index=False)
df.to_csv('tables/eventTable/major_eq_details_with_station_coordinates2.csv', index=False) #you can change the name

time2=time.time()
duree= time1-time2
print(duree)
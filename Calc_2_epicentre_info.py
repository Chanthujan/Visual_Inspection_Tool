# ------------------------------------------
# --- Author: Chanthujan Chandrakumar
# --- Date: 4/08/23
# --- Python Ver: 3.8
# ------------------------------------------


###This code to get the epicentre info for each station and save it in the excel file

import pandas as pd

# Read data from Excel sheets
sheet1_file = 'tables/eventTable/major_eq_details_with_station_coordinates2.csv' #result of the code Calc_1_station_info.py
sheet2_file = 'search_13_22/list_13_22.csv' #obtain from the geonet website and QuakeSearch
df_sheet1 = pd.read_csv(sheet1_file)
df_sheet2 = pd.read_csv(sheet2_file)

df_sheet1["EarthquakeID"] = df_sheet1["EarthquakeID"].astype(str)
df_sheet2["publicid"] = df_sheet2["publicid"].astype(str)
print(df_sheet1['EarthquakeID'].unique())
print(df_sheet2['publicid'].unique())
# Merge the two DataFrames based on EarthquakeID and publicid columns
merged_df = df_sheet1.merge(df_sheet2, left_on='EarthquakeID', right_on='publicid', how='left')

# Update epi_lat and epi_long columns in the first DataFrame
merged_df['epi_lat'] = merged_df['latitude']
merged_df['epi_long'] = merged_df['longitude']

# Drop unnecessary columns from the merged DataFrame
merged_df.drop(columns=['publicid', 'longitude', 'latitude'], inplace=True)

# Save the updated DataFrame back to Excel
merged_df.to_csv('tables/eventTable/major_events_info.csv', index=False) #you can change the name

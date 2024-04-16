import obspy
from obspy import UTCDateTime
from obspy.clients.fdsn import Client
import matplotlib
import os
import csv
from obspy import read_events


""" This is the code used to select the data from GEONET with S and P wave picks (order 1)"""

def create_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
    return dir

def check_value_in_csv(csv_file, value, column_index):
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) > column_index and row[column_index] == value:
                return True
    return False

def check_first_two_values(csv_file, value1, value2):
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 2 and row[0] == value1 and row[1] == value2:
                return True
    return False

def add_data_to_csv(csv_file, value1, value2, data_to_add):
    rows = []
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 2 and row[0] == value1 and row[1] == value2:
                row.extend(data_to_add)  # Add the new data to the row
            rows.append(row)

    # Write the modified rows to the CSV file
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)


def add_data_to_specific_csv(csv_file, value1, value2, column_index, data_to_add):
    rows = []
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 2 and row[0] == value1 and row[1] == value2:
                row[column_index] = data_to_add  # Update the specific column with new data
            rows.append(row)

    # Write the modified rows to the CSV file
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

path_temp = "/home/durando/Documents/STAGE/mon_env/tables/eventTable/" #change with your path
#create_dir(path_temp)
with open(path_temp + "basic_eq_data_test.csv", "a") as csv_file:
    writer = csv.writer(csv_file, delimiter=',')
    writer.writerow(["EarthquakeID",	"Station Name", "Reported P-wave Time",	"Reported S-wave time", "eq_starttime"])


matplotlib.use('TkAgg')

# set parameters here
network = "NZ"
location = "*"
channel = "?N?"  # or "HHZ", "??E", "*N" etc.
station = "????"
output = "ACC"  # also"VEL" "DISP" or "ACC"


# starttime = UTCDateTime("2019-07-20T11:51:42.00Z")

def create_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
    return dir


rotate_to_radial_transverse = False

array_time = ["2011-12-24T00:00:00.000Z"]

# coordinate of the epicentre of the earthquakes


coordinate_array = [[-43.519960, 172.143519]]

c = Client("GEONET")
start_time = UTCDateTime(2013, 1, 1, 0, 0, 0)
end_time = UTCDateTime(2022, 12, 31, 23, 59, 59)
min_magnitude = 6
min_lat = -47.5617
max_lat = -34.2192
min_lon = 165.8271
max_lon = 179.6050


"""Catalog creation"""

# for each catalog in the catalogue directory
for filename in os.listdir("catalogue_2013_2022"): #change with the name of your catalogue directory
# #   read the catalog
    print(filename)
    catalog = obspy.read_events("catalogue_2013_2022/" + filename, format="QUAKEML")
    print(catalog)
    for event in catalog:
        #print(event)
        for pick in event.picks:
            if pick.phase_hint == "P": # and pick.waveform_id.station_code[-1] == "C":  #or Pn
                #print("P-wave pick time:", pick.time)
                if not check_first_two_values(path_temp + "basic_eq_data_test.csv", str(event.resource_id.id),
                                            str(pick.waveform_id.station_code)):
                    with open(path_temp + "basic_eq_data_test.csv", "a") as csv_file:
                    #check whether the event.resource_id.id is already in the csv file
                        writer = csv.writer(csv_file, delimiter=',')
                        writer.writerow([str(event.resource_id.id), str(pick.waveform_id.station_code), str(pick.time)])
                else:
                    add_data_to_specific_csv(path_temp + "basic_eq_data_test.csv", str(event.resource_id.id), str(pick.waveform_id.station_code), 2, str(pick.time))

            if pick.phase_hint == "S": #"Sn" and pick.waveform_id.station_code[-1] == "C": #or Sn
                #print("S-wave pick time:", pick.time)
                if not check_first_two_values(path_temp + "basic_eq_data_test.csv", str(event.resource_id.id),
                                            str(pick.waveform_id.station_code)):
                    with open(path_temp + "basic_eq_data_test.csv", "a") as csv_file:
                        writer = csv.writer(csv_file, delimiter=',')
                        writer.writerow([str(event.resource_id.id), str(pick.waveform_id.station_code), "N/A", str(pick.time)])
                else:
                    add_data_to_csv(path_temp + "basic_eq_data_test.csv", str(event.resource_id.id), str(pick.waveform_id.station_code), [str(pick.time)])
                # with open("pick_data.txt", "a") as f:
                #     f.write("S_wave pick time: " + str(pick.time) + "at" + str(pick.waveform_id.station_code))
                #     f.write("\n")

#"""
from obspy import UTCDateTime
from obspy.clients.fdsn import Client
import matplotlib
import os
import csv

matplotlib.use('TkAgg')

"""This is the code used to download the data from GEONET after creating the merged csv file (order 3)"""

# starttime = UTCDateTime("2019-07-20T11:51:42.00Z")

def create_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
    return dir

rotate_to_radial_transverse = False

c = Client("GEONET")
network = "NZ"
location = "*"
channel = "?N?"  # or "HHZ", "??E", "*N" etc.
station = "????"
output = ["ACC", "VEL", "DISP"]  # also"VEL" "DISP" or "ACC"

count = 0
with open('tables/eventTable/DATA.csv', 'r') as csv_file:  #change with your file
    csv_reader = csv.reader(csv_file)
    for line in csv_reader:
        try:
            #print(str(line[0]))
            earthquakeID = line[0].split('/')[-1] #or earthquakeID = line[0] if there is no /
            start_time = line[2]
            station_code = line[1]
            starttime = UTCDateTime(start_time) -30
            endtime = UTCDateTime(start_time) + 60
            for output_i in output:
                st = c.get_waveforms(network=network, station=station_code,
                                     location=location, channel=channel,
                                     starttime=starttime, endtime=endtime, attach_response=True)
                st.remove_response(output=output_i)
                st.trim(starttime=starttime, endtime=endtime)
                st.sort()

                if rotate_to_radial_transverse:
                    #print("rotating N/E/Z to R/T/Z", end="...")
                    st.rotate(method="NE->RT")

                path_temp = '/home/durando/Documents/STAGE/mon_env/Data/' + earthquakeID + '/' #The path you want the data to go to
                create_dir(path_temp)
                path_temp_2 = '/home/durando/Documents/STAGE/mon_env/Data/' + earthquakeID + '/' + station_code + '/'
                create_dir(path_temp_2)
                if(output_i == "ACC"):
                    path_temp_3 = '/home/durando/Documents/STAGE/mon_env/Data/' + earthquakeID + '/' + station_code + '/' + output_i + '/'
                    count = count + 1
                    create_dir(path_temp_3)
                elif(output_i == "VEL"):
                    path_temp_3 = '/home/durando/Documents/STAGE/mon_env/Data/' + earthquakeID + '/' + station_code + '/' + output_i + '/'
                    create_dir(path_temp_3)
                elif(output_i == "DISP"):
                    path_temp_3 = '/home/durando/Documents/STAGE/mon_env/Data/' + earthquakeID + '/' + station_code + '/' + output_i + '/'
                    create_dir(path_temp_3)
                for tr in st:
                        if tr.stats.channel[-1] == "1":
                            tr.stats.channel = tr.stats.channel[:-1] + "N"
                        elif tr.stats.channel[-1] == "2":
                            tr.stats.channel = tr.stats.channel[:-1] + "E"
                        filename = path_temp_3 + '/' + tr.stats.channel + "-" + "DATA" + ".mseed"
                        tr.write(filename, format='MSEED')
        except:
            #print("error")
            continue

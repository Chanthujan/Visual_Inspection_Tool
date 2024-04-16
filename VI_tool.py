import os
import csv
from datetime import timedelta
import shutil
from scipy import signal
import matplotlib.pyplot as plt
from scipy import integrate
import scipy
import numpy as np
from obspy.core import read
import matplotlib
import math
from obspy import UTCDateTime
from matplotlib.widgets import Button
import sys
matplotlib.use('TkAgg')
sys.setrecursionlimit(100000)

def create_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
    return dir


path_temp = "tables/eventTable/"
create_dir(path_temp)

with open(path_temp + "save_earthquake_info.csv", "a") as csv_file:
    writer = csv.writer(csv_file, delimiter=',')
    writer.writerow(
        ["EarthquakeID", "Station Name", "Site Class", "P-wave Pick Time", "Magnitude", "PGA_P", "PGV_P", "Pd_P", "PGA_P_Ind",
         "PGV_P_Ind", "Pd_P_Ind", "TauC", "PGA_S", "PGV_S", "Pd_S", "PGA_S_Ind", "PGV_S_Ind", "Pd_S_Ind"])
with open(path_temp + "save_incorrect_info.csv", "a") as csv_file:
    writer = csv.writer(csv_file, delimiter=',')
    writer.writerow(["EarthquakeID", "Station Name"])


def check_first_two_values(csv_file, value1, value2):
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 2 and row[0] == value1 and row[1] == value2:
                return [row[2], row[3], row[4]]
    return []


def check_first_value(csv_file, value1):
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 1 and str(row[0]) == value1:
                print("row[1]: ", row[1])
                return row[1]
    return []


def butter_highpass(cutoff, fs, order=2):
    # nyq = 0.5 * fs
    # normal_cutoff = cutoff / nyq
    sos = signal.butter(order, cutoff, btype='high', fs=fs, output='sos')
    return sos


def butter_highpass_filter(data, cutoff, fs, order=2):
    sos = butter_highpass(cutoff, fs, order=order)
    y = signal.sosfiltfilt(sos, data)
    return y


def site_class_returner(site_csv):
    with open(site_csv, 'r') as file:
        count = 0
        reader = csv.reader(file)
        for row in reader:
            # assign the row[0] to the site class
            print("row values:", row)
            site_param = str(row[0])
            print("site_param: ", site_param)
            site_class = site_param.split(",")
            # skip the first row
            if (count == 0):
                count = count + 1
                continue
            print("site_class: ", site_class[1])
            print("site_class: ", site_class[0])
            # add siteclass[0] and siteclass[1] to a CSV file
            with open('tables/eventTable/site_class.csv', 'a') as file:
                writer = csv.writer(file)
                writer.writerow([site_class[0], site_class[1]])
            # print("site_class: ", site_class)
            # if len(row) >= 2 and row[0] == "Site Class":
            #     return row[1


def peak_calculator(channel1, channel2, channel3, channel1_Av, channel2_Av, channel3_Av, channel1_Ad, channel2_Ad,
                    channel3_Ad, pick_time, df):
    print("I am in peak_calculator")
    channel1_p = channel1.slice(pick_time, pick_time + 3)
    channel2_p = channel2.slice(pick_time, pick_time + 3)
    channel3_p = channel3.slice(pick_time, pick_time + 3)
    channel1_v = channel1_Av.slice(pick_time, pick_time + 3)
    channel2_v = channel2_Av.slice(pick_time, pick_time + 3)
    channel3_v = channel3_Av.slice(pick_time, pick_time + 3)
    channel1_d = channel1_Ad.slice(pick_time, pick_time + 3)
    channel2_d = channel2_Ad.slice(pick_time, pick_time + 3)
    channel3_d = channel3_Ad.slice(pick_time, pick_time + 3)
    PGA_P = [max(np.abs(channel1_p[0].data)), max(np.abs(channel2_p[0].data)), max(np.abs(channel3_p[0].data))]
    # find the time value of the peaks
    PGA_P_Ind = [np.argmax(np.abs(channel1_p[0].data)), np.argmax(np.abs(channel2_p[0].data)),
                 np.argmax(np.abs(channel3_p[0].data))]
    print("PGA_P_Ind: ", PGA_P_Ind)
    PGV_P = [max(np.abs(channel1_v[0].data)), max(np.abs(channel2_v[0].data)), max(np.abs(channel3_v[0].data))]
    PGV_P_Ind = [np.argmax(np.abs(channel1_v[0].data)), np.argmax(np.abs(channel2_v[0].data)),
                 np.argmax(np.abs(channel3_v[0].data))]
    Pd_P = [max(np.abs(channel1_d[0].data)), max(np.abs(channel2_d[0].data)), max(np.abs(channel3_d[0].data))]
    Pd_P_Ind = [np.argmax(np.abs(channel1_d[0].data)), np.argmax(np.abs(channel2_d[0].data)),
                np.argmax(np.abs(channel3_d[0].data))]
    TauC = tauc_calculator(channel1_d, channel1_v, df)
    PGA_S = [max(np.abs(channel1[0].data)), max(np.abs(channel2[0].data)), max(np.abs(channel3[0].data))]
    PGA_S_Ind = [np.argmax(np.abs(channel1[0].data)), np.argmax(np.abs(channel2[0].data)),
                 np.argmax(np.abs(channel3[0].data))]
    PGV_S = [max(np.abs(channel1_Av[0].data)), max(np.abs(channel2_Av[0].data)), max(np.abs(channel3_Av[0].data))]
    PGV_S_Ind = [np.argmax(np.abs(channel1_Av[0].data)), np.argmax(np.abs(channel2_Av[0].data)),
                 np.argmax(np.abs(channel3_Av[0].data))]
    Pd_S = [max(np.abs(channel1_Ad[0].data)), max(np.abs(channel2_Ad[0].data)), max(np.abs(channel3_Ad[0].data))]
    Pd_S_Ind = [np.argmax(np.abs(channel1_Ad[0].data)), np.argmax(np.abs(channel2_Ad[0].data)),
                np.argmax(np.abs(channel3_Ad[0].data))]
    return PGA_P, PGV_P, Pd_P, PGA_P_Ind, PGV_P_Ind, Pd_P_Ind, TauC, PGA_S, PGV_S, Pd_S, PGA_S_Ind, PGV_S_Ind, Pd_S_Ind


def move_folder(source_dir, destination_dir):
    try:
        shutil.move(source_dir, destination_dir)
        print("Folder moved successfully.")
    except Exception as e:
        print("An error occurred while moving the folder:", str(e))


def tauc_calculator(displacement, velocity, df):
    df = int(df)
    dt = 1 / df
    vel_coeff = np.square(velocity[0].data)
    disp_coeff = np.square(displacement[0].data)
    vel_val = integrate.cumtrapz(vel_coeff, dx=dt)
    disp_val = integrate.cumtrapz(disp_coeff, dx=dt)
    tauc = 2 * scipy.pi * np.sqrt(disp_val[-1] / vel_val[-1])
    log_tauc = np.log(tauc)
    return tauc, log_tauc


def close_plot(event):
    global counter1, station_arr
    global counter2
    global max_limit
    plt.close()

def exit_program(event):
    exit()


def save_correct_info(event):
    with open("tables/eventTable/save_earthquake_info.csv", "a") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(excel_data)
        print("excel_data is added to excel sheet", excel_data)
        plt.close()


def save_incorrect_info(event):
    with open("tables/eventTable/save_incorrect_info.csv", "a") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(incorrect_data)
        plt.close()


# site_class_returner("tables/eventTable/site_characteristics.csv")

directory_1 = "Data/New_Data/" #download the data from the GeoNet website and put it in the Data folder using the Data_3_data_downloader.py script
# print the log of pi to the power of 2
def main_func():
    global excel_data, incorrect_data
    for event in os.listdir(directory_1):
        if not event.startswith('.'):
            directory_2 = directory_1 + event + '/'
            for station in os.listdir(directory_2):
                if not station.startswith('.'):
                    if os.path.exists(directory_2 + station + '/' + "ACC" + "/" + 'HNZ-DATA.mseed'):
                        st = read(directory_2 + station + '/' + "ACC" + "/" + 'HNZ-DATA.mseed')
                        st1 = read(directory_2 + station + '/' + "ACC" + "/" + 'HNE-DATA.mseed')
                        st2 = read(directory_2 + station + '/' + "ACC" + "/" + 'HNN-DATA.mseed')
                        st_v = read(directory_2 + station + '/' + "VEL" + "/" + 'HNZ-DATA.mseed')
                        st_v1 = read(directory_2 + station + '/' + "VEL" + "/" + 'HNE-DATA.mseed')
                        st_v2 = read(directory_2 + station + '/' + "VEL" + "/" + 'HNN-DATA.mseed')
                        st_d = read(directory_2 + station + '/' + "DISP" + "/" + 'HNZ-DATA.mseed')
                        st_d1 = read(directory_2 + station + '/' + "DISP" + "/" + 'HNE-DATA.mseed')
                        st_d2 = read(directory_2 + station + '/' + "DISP" + "/" + 'HNN-DATA.mseed')
                    else:
                        st = read(directory_2 + station + '/' + "ACC" + "/" + 'BNZ-DATA.mseed')
                        st1 = read(directory_2 + station + '/' + "ACC" + "/" + 'BNE-DATA.mseed')
                        st2 = read(directory_2 + station + '/' + "ACC" + "/" + 'BNN-DATA.mseed')
                        st_v = read(directory_2 + station + '/' + "VEL" + "/" + 'BNZ-DATA.mseed')
                        st_v1 = read(directory_2 + station + '/' + "VEL" + "/" + 'BNE-DATA.mseed')
                        st_v2 = read(directory_2 + station + '/' + "VEL" + "/" + 'BNN-DATA.mseed')
                        st_d = read(directory_2 + station + '/' + "DISP" + "/" + 'BNZ-DATA.mseed')
                        st_d1 = read(directory_2 + station + '/' + "DISP" + "/" + 'BNE-DATA.mseed')
                        st_d2 = read(directory_2 + station + '/' + "DISP" + "/" + 'BNN-DATA.mseed')

                    start_trace = st[0].stats.starttime
                    # filter all nine traces
                    st.filter('bandpass', freqmin=0.1, freqmax=20)
                    st1.filter('bandpass', freqmin=0.1, freqmax=20)
                    st2.filter('bandpass', freqmin=0.1, freqmax=20)
                    st_v.filter('bandpass', freqmin=0.1, freqmax=20)
                    st_v1.filter('bandpass', freqmin=0.1, freqmax=20)
                    st_v2.filter('bandpass', freqmin=0.1, freqmax=20)
                    st_d.filter('bandpass', freqmin=0.1, freqmax=20)
                    st_d1.filter('bandpass', freqmin=0.1, freqmax=20)
                    st_d2.filter('bandpass', freqmin=0.1, freqmax=20)
                    # filter the velocity and displacement traces using butter_highpass_filter(acc, 0.075, fs)
                    st_v[0].data = butter_highpass_filter(st_v[0].data, 0.075, st_v[0].stats.sampling_rate)
                    st_v1[0].data = butter_highpass_filter(st_v1[0].data, 0.075, st_v1[0].stats.sampling_rate)
                    st_v2[0].data = butter_highpass_filter(st_v2[0].data, 0.075, st_v2[0].stats.sampling_rate)
                    st_d[0].data = butter_highpass_filter(st_d[0].data, 0.075, st_d[0].stats.sampling_rate)
                    st_d1[0].data = butter_highpass_filter(st_d1[0].data, 0.075, st_d1[0].stats.sampling_rate)
                    st_d2[0].data = butter_highpass_filter(st_d2[0].data, 0.075, st_d2[0].stats.sampling_rate)
                    # demean all nine traces
                    st.detrend(type='demean')
                    st1.detrend(type='demean')
                    st2.detrend(type='demean')
                    st_v.detrend(type='demean')
                    st_v1.detrend(type='demean')
                    st_v2.detrend(type='demean')
                    st_d.detrend(type='demean')
                    st_d1.detrend(type='demean')
                    st_d2.detrend(type='demean')
                    EarthquakeID = "smi:nz.org.geonet/" + event
                    list_picks = check_first_two_values("tables/eventTable/basic_eq_data_2015_2022_wt_mag_2.csv", EarthquakeID, station)
                    if len(list_picks) == 0 or list_picks[0] == "":
                        continue
                    if list_picks[0] != "":
                        print("P and S picks are available")
                        print("P_pick: ", list_picks[0])
                        P_pick = UTCDateTime(str(list_picks[0]))
                        P_pick_three_sec = P_pick + 3
                        if (list_picks[1] != ""):
                            print("S_pick: ", list_picks[1])
                            S_pick = UTCDateTime(str(list_picks[1]))
                            S_pick_time = S_pick - start_trace
                        # # add the start time to the P_pick
                        P_pick_time = P_pick - start_trace
                        P_pick_three_sec = P_pick_three_sec - start_trace
                        st_name = st[0].stats.station
                        fs = st[0].stats.sampling_rate
                        npts = st[0].stats.npts
                        t = np.arange(npts, dtype=np.float32) / fs

                        peak_array = peak_calculator(st, st1, st2, st_v, st_v1, st_v2, st_d, st_d1, st_d2, P_pick,
                                                     fs)  # calculation of peak values
                        site_class = check_first_value("tables/eventTable/site_class.csv", station)
                        if(site_class == ""):
                            site_class = "site class not available"
                        excel_data = [str(event), str(station), str(site_class), str(P_pick), str(list_picks[2])]
                        incorrect_data = [str(event), str(station)]
                        excel_data.extend(peak_array)
                        print("excel_data", excel_data)
                        # site class returning function

                        fig = plt.figure()
                        # main plot

                        ax1 = fig.add_subplot(411)
                        # avoid titles of the plot touching the figure
                        # put a title to the figure

                        ax1.plot(t, st[0].data, 'k')
                        # add a vertical line at the P wave arrival
                        ax1.axvline(x=P_pick_time, color='r', linestyle='--', label="P-Pick", zorder=0)
                        if (list_picks[1] != ""):
                            ax1.axvline(x=S_pick_time, color='b', linestyle='--', label="S-Pick", zorder=0)
                        # legend the vertical axes
                        ax1.legend()
                        ax1.set_ylabel('Acceleration (m/s/s)')
                        ax1.set_xlabel('Time (s)')

                        ax1.set_title(
                            "Vertical acceleration record and P and S-wave picks - Event_ID: " + event + " - Station Name: " + st_name + " - Site Class: " + site_class)
                        # add a vertical line at the 3 sec
                        # ax1.axvline(x=P_pick_three_sec, color='b', linestyle='--')
                        print("P_pick", P_pick)
                        print("P_pick time:", P_pick + timedelta(seconds=peak_array[3][0] / fs))

                        # 3 seconds window
                        ax2 = fig.add_subplot(412)
                        st_3_Sec = st.slice(P_pick - 1, P_pick + 4)
                        t_2 = np.arange(0, 5 + 1 / fs, 1 / fs)
                        ax2.plot(t_2, np.abs(st_3_Sec[0].data), 'k')
                        # add a title to the figure 2
                        ax2.set_title("5 second window around the P-wave pick")
                        ax2.set_ylabel('Acceleration (m/s/s)')
                        ax2.set_xlabel('Time (s)')
                        # peak_PGA_indice = start_trace + timedelta(seconds=peak_array[3][0]/fs) - start_trace
                        peak_PGA_indice = peak_array[3][0] / fs
                        print("peak PGA value", peak_PGA_indice)
                        print("P_pick", P_pick)
                        print("P_pick_Time", P_pick_time)
                        #ax2.axvline(x=peak_PGA_indice + 1, color='g', linestyle='--', label="PEAK PGA_P" , zorder=0)
                        ax2.axvline(x=1, color='r', linestyle='--', label="P_Pick", zorder=0)
                        ax2.axvline(x=4, color='b', linestyle='--', label="3 sec window", zorder=0)
                        ax2.legend()

                        # s-wave plots
                        ax3 = fig.add_subplot(413)
                        ax3.plot(t, st1[0].data, 'k')
                        if (list_picks[1] != ""):
                            ax3.axvline(x=S_pick_time, color='b', linestyle='--', label="S-Pick", zorder=0)
                        peak_PGA_S_indice_1 = start_trace + timedelta(seconds=peak_array[10][1] / fs) - start_trace
                        #ax3.axvline(x=peak_PGA_S_indice_1, color='r', linestyle='--', label="Peak PGA-S")
                        ax3.set_title("HNE Channel accleration data with peak PGA")
                        ax3.legend()
                        ax3.set_ylabel('Acceleration (m/s/s)')
                        ax3.set_xlabel('Time (s)')
                        ax4 = fig.add_subplot(414)
                        ax4.plot(t, st2[0].data, 'k')
                        if (list_picks[1] != ""):
                            ax4.axvline(x=S_pick_time, color='b', linestyle='--', label="S-Pick", zorder=0)
                        peak_PGA_S_indice_2 = start_trace + timedelta(seconds=peak_array[10][2] / fs) - start_trace
                        #ax4.axvline(x=peak_PGA_S_indice_2, color='r', linestyle='--', label="Peak PGA-S")
                        ax4.set_title("HNN Channel accleration data with peak PGA")
                        ax4.set_ylabel('Acceleration (m/s/s)')
                        ax4.set_xlabel('Time (s)')
                        ax4.legend()
                        axcut_1 = plt.axes([0.8, 0.0, 0.1, 0.05])

                        bcut_1 = Button(axcut_1, 'Next', color='blue', hovercolor='green')
                        axcut_2 = plt.axes([0.2, 0.0, 0.1, 0.05])
                        bcut_2 = Button(axcut_2, 'Correct', color='Green', hovercolor='blue')
                        axcut_3 = plt.axes([0.4, 0.0, 0.1, 0.05])
                        bcut_3 = Button(axcut_3, 'Incorrect', color='red', hovercolor='blue')
                        axcut_4 = plt.axes([0.6, 0.0, 0.1, 0.05])
                        bcut_4 = Button(axcut_4, 'Exit', color='red', hovercolor='blue')
                        bcut_1.on_clicked(close_plot)
                        bcut_2.on_clicked(save_correct_info)

                        bcut_3.on_clicked(save_incorrect_info)
                        bcut_4.on_clicked(exit_program)


                        # avoid axis and title cutting each other
                        plt.tight_layout()
                        #make the plots close to each other reducing the space between them
                        plt.subplots_adjust(hspace=0.5)

                        # put a tile to the plot at the top of the figure
                        # plt.title("First page of a new station!!!!!!", loc='center', fontsize=16)

                        plt.show()

                        # plot the same figures for the velocity

                        fig = plt.figure()
                        # main plot
                        ax1 = fig.add_subplot(411)
                        ax1.plot(t, st_v[0].data, 'k')
                        # add a vertical line at the P wave arrival
                        ax1.axvline(x=P_pick_time, color='r', linestyle='--', label="P-Pick")
                        if (list_picks[1] != ""):
                            ax1.axvline(x=S_pick_time, color='b', linestyle='--', label="S-Pick")
                        ax1.legend()
                        ax1.set_ylabel('Velocity (m/s)')
                        ax1.set_title("Velocity plots: " +  event + "  " + st_name + " P-Pick and S-Pick" + "  site class: " + site_class)
                        # add a vertical line at the 3 sec
                        # plot velocity
                        ax2 = fig.add_subplot(412)
                        stv_3_Sec = st_v.slice(P_pick - 1, P_pick + 4)
                        ax2.plot(t_2, np.abs(stv_3_Sec[0].data), 'k')
                        # ax2.axvline(x=S_pick_time, color='b', linestyle='--')
                        # PGA_P, PGV_P, Pd_P, PGA_P_Ind, PGV_P_Ind, Pd_P_Ind, TauC, PGA_S, PGV_S, Pd_S, PGA_S_Ind, PGV_S_Ind, Pd_S_Ind
                        peak_PGV_indice = peak_array[4][0] / fs
                        print("peak PGV P-wave indice", peak_PGV_indice)
                        ax2.set_title("5 second window around the P-wave pick")
                        ax2.axvline(x=peak_PGV_indice + 1, color='g', linestyle='-', label="PEAK PGV_P")
                        ax2.axvline(x=1, color='r', linestyle='--', label="P_Pick")
                        ax2.axvline(x=4, color='b', linestyle='--', label="3 sec window")
                        ax2.legend()
                        ax3 = fig.add_subplot(413)
                        ax3.plot(t, st_v1[0].data, 'k')
                        if (list_picks[1] != ""):
                            ax3.axvline(x=S_pick_time, color='b', linestyle='--', label="S-Pick")

                        peak_PGV_S_indice_1 = start_trace + timedelta(seconds=peak_array[11][1] / fs) - start_trace
                        ax3.axvline(x=peak_PGV_S_indice_1, color='r', linestyle='--', label="Peak PGV-S")
                        ax3.set_title("HNE Channel velocity data with peak PGV")
                        ax3.legend()
                        ax4 = fig.add_subplot(414)
                        ax4.plot(t, st_v2[0].data, 'k')
                        if (list_picks[1] != ""):
                            ax4.axvline(x=S_pick_time, color='b', linestyle='--', label="S-Pick")
                        peak_PGV_S_indice_2 = start_trace + timedelta(seconds=peak_array[11][2] / fs) - start_trace
                        ax4.axvline(x=peak_PGV_S_indice_2, color='r', linestyle='--', label="Peak PGV-S")
                        ax4.set_title("HNN Channel velocity data with peak PGV")
                        ax4.legend()
                        axcut_1 = plt.axes([0.8, 0.0, 0.1, 0.05])
                        bcut_1 = Button(axcut_1, 'Next', color='blue', hovercolor='green')
                        bcut_1.on_clicked(close_plot)
                        # avoid axis and title cutting each other
                        plt.tight_layout()
                        plt.show()

                        # plot the same figures for the displacement
                        fig = plt.figure()
                        # main plot
                        ax1 = fig.add_subplot(411)
                        ax1.plot(t, st_d[0].data, 'k')
                        # add a vertical line at the P wave arrival
                        ax1.axvline(x=P_pick_time, color='r', linestyle='--', label="P-Pick")
                        if (list_picks[1] != ""):
                            ax1.axvline(x=S_pick_time, color='b', linestyle='--', label="S-Pick")
                        ax1.legend()
                        ax1.set_ylabel('Displacement (m)')
                        ax1.set_title("Displacement plots: " + event + "  " + st_name + " P-Pick and S-Pick" + "  site class: " + site_class)
                        ax2 = fig.add_subplot(412)
                        std_3_Sec = st_d.slice(P_pick - 1, P_pick + 4)
                        ax2.plot(t_2, np.abs(std_3_Sec[0].data), 'k')
                        # ax2.axvline(x=S_pick_time, color='b', linestyle='--')
                        # PGA_P, PGV_P, Pd_P, PGA_P_Ind, PGV_P_Ind, Pd_P_Ind, TauC, PGA_S, PGV_S, Pd_S, PGA_S_Ind, PGV_S_Ind, Pd_S_Ind
                        peak_Pd_indice = peak_array[5][0] / fs
                        print("peak Pd P-wave indice", peak_Pd_indice)
                        ax2.set_title("5 second window around the P-wave pick")
                        ax2.axvline(x=peak_Pd_indice + 1, color='g', linestyle='-', label="PEAK Pd_P")
                        ax2.axvline(x=1, color='r', linestyle='--', label="P_Pick")
                        ax2.axvline(x=4, color='b', linestyle='--', label="3 sec window")
                        ax2.legend()
                        ax3 = fig.add_subplot(413)
                        ax3.plot(t, st_d1[0].data, 'k')
                        if (list_picks[1] != ""):
                            ax3.axvline(x=S_pick_time, color='b', linestyle='--', label="S-Pick")

                        peak_Pd_S_indice_1 = start_trace + timedelta(seconds=peak_array[12][1] / fs) - start_trace
                        ax3.axvline(x=peak_Pd_S_indice_1, color='r', linestyle='--', label="Peak Pd-S")
                        ax3.set_title("HNE Channel displacement data with peak Pd")
                        ax3.legend()
                        ax4 = fig.add_subplot(414)
                        ax4.plot(t, st_d2[0].data, 'k')
                        if (list_picks[1] != ""):
                            ax4.axvline(x=S_pick_time, color='b', linestyle='--', label="S-Pick")
                        peak_Pd_S_indice_2 = start_trace + timedelta(seconds=peak_array[12][2] / fs) - start_trace
                        ax4.axvline(x=peak_Pd_S_indice_2, color='r', linestyle='--', label="Peak Pd-S")
                        ax4.set_title("HNN Channel displacement data with peak Pd")
                        ax4.legend()
                        axcut_1 = plt.axes([0.8, 0.0, 0.1, 0.05])
                        bcut_1 = Button(axcut_1, 'Next', color='blue', hovercolor='green')
                        bcut_1.on_clicked(close_plot)

                        # avoid axis and title cutting each other
                        plt.tight_layout()
                        plt.show()

            move_folder( directory_2, "Data/Analysed_Data/")
            #move the event folder to the analysed folder in the data directory






# call the main function to run the code
if __name__ == "__main__":
    main_func()

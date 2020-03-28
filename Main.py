from tqdm import tqdm
import re
import numpy as np
from matplotlib import pyplot as plt
import os
import time
from datetime import datetime

# Formats the data arrays into single lines when printed
np.set_printoptions(linewidth=np.inf)

# Data Arrays
time = []
fVoltageCavityX = []
fVoltageCavityY = []
fVoltagePumpX = []
fVoltagePumpY = []
fSignal = []
fPumpDiodeCurrent = []
fMtrPosn = []


def plot_file(file):
    # TODO still need to find a way to map this this function to both log files
    """Seperates Data Into CSVs for each given data point
        ie. all fVoltageCavityX data will be in it own seperate .csv file for further processing

        Use out put from get_lines as file ie test(get_lines(Original Log File))
    """
    with open(file, 'r') as infile:
        # variable for each line in infile
        # lines = infile.readlines()

        # Allows function to access global Data Arrays
        global time
        global fVoltageCavityX
        global fVoltageCavityY
        global fVoltagePumpX
        global fVoltagePumpY
        global fSignal
        global fPumpDiodeCurrent
        global fMtrPosn
        first_line = infile.readline()
        epoch = datetime(1970, 1, 1)
        log_start_time = datetime.strptime(first_line[:19], '%Y-%m-%d %H:%M:%S')
        start_time_seconds = (log_start_time - epoch).total_seconds()

        # Searches for key word Piezo in lines then seperates all data into corresponding arrays
        for line in tqdm(infile, total=file_len(file)):
            # if re.search('PD-PmpDiodeCrnt-MtrPos', line):

            current_time = line[:19]
            current_time_object = datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S')
            current_time_seconds = (current_time_object - epoch).total_seconds()
            current_minute = round((current_time_seconds - start_time_seconds) / 60)
            time = np.append(time, current_minute)

            # extract data
            measurementData = line[70:]

            # put data in array
            dataArray = np.array(measurementData.split())

            # turn string array into float array
            float_data_array = dataArray.astype(np.float)

            # indexing the fVoltageCavityX  data and adding to array
            fVoltageCavityX = np.append(fVoltageCavityX, float_data_array[0])

            # indexing the fVoltageCavityY  data and adding to array
            fVoltageCavityY = np.append(fVoltageCavityY, float_data_array[1])

            # indexing the fVoltagePumpX  data and adding to array
            fVoltagePumpX = np.append(fVoltagePumpX, float_data_array[2])

            # indexing the fVoltagePumpY  data and adding to array
            fVoltagePumpY = np.append(fVoltagePumpY, float_data_array[3])

            # indexing the fSignal  data and adding to array
            fSignal = np.append(fSignal, float_data_array[4])

            # indexing the fPumpDiodeCurrent  data and adding to array
            fPumpDiodeCurrent = np.append(fPumpDiodeCurrent, float_data_array[5])

            # indexing the fMtrPosn  data and adding to array
            fMtrPosn = np.append(fMtrPosn, float_data_array[6])

        multi_graph_data_mean(fPumpDiodeCurrent,fVoltagePumpX,fVoltagePumpY,fVoltageCavityY)



def save_data_mean_graph(array, title, x_axis, y_axis, sample_size, file_name):
    """Plots a single array and saves the file....working use this two plot the averaged array. use 60 as sample
    sized to average every minute """
    print("Strarting to graph: ")
    remainder = np.mod(len(array), sample_size)
    print("now truncating")
    data1 = array[:-remainder]
    averaged_array = np.mean(data1.reshape(-1, sample_size), axis=1)
    plt.title(title)
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    plt.plot(averaged_array)
    plt.savefig(file_name + ".png")
    plt.clf()
    print('finished plotting')


def histogram(array1):
    "histograms"
    plt.hist(array1)
    plt.show()


def histogram_2D():
    "2d histograms"
    figHist = plt.figure();
    axHist = figHist.add_subplot(1, 1, 1);
    axHist.hist2d(time, fPumpDiodeCurrent, bins=100, cmax=10000);  # , [10len(listTime), 10]);
    axHist.set_xlabel("Time [hr]");
    axHist.set_ylabel("Diagnostic PD [V]");
    plt.show();


def graph_data_mean(array, title, x_axis, y_axis, sample_size):
    """Returns a plot. Set Sample Size to 60 for average of every hour"""
    print("Strarting to graph: ")
    remainder = np.mod(len(array), sample_size)
    print("now truncating")
    data1 = array[:-remainder]
    trunc_time = time[:-remainder]
    averaged_array = np.mean(data1.reshape(-1, sample_size), axis=1)
    plt.title(title)
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    return plt.plot(averaged_array)



def multi_graph_data_mean(array1, array2, array3, array4):
    """Subplots"""

    # remainder = np.mod(len(array1), sample_size) i dont think we need this. This is handled by graph_data_mean
    plt.figure()
    plt.subplot(4, 1, 1)
    graph_data_mean(array1, "Voltage Cavity X", "hours", "Voltage", 60)

    plt.subplot(4, 1, 2)
    # plt.title("fVoltageCavityY")
    graph_data_mean(array2, "Voltage Cavity Y", "hours", "Voltage", 60)

    plt.subplot(4, 1, 3)
    # plt.title("fVoltageCavityY")
    graph_data_mean(array3, "Voltage Pump X", "hours", "Voltage", 60)

    plt.subplot(4, 1, 4)
    # plt.title("fVoltageCavityY")
    graph_data_mean(array4, "Voltage Pump Y", "hours", "Voltage", 60)
    plt.savefig("sub_test" + ".png")
    plt.clf()
    print('finished plotting')


def averaged_array(array, sample_size):
    print("Strarting to graph: ")
    arrayLength = len(array)
    remainder = np.mod(arrayLength, sample_size)
    print("now truncating")
    data1 = array[:-remainder]
    averaged_data = np.mean(data1.reshape(-1, sample_size), axis=1)
    return averaged_data


def file_len(f_name):
    """gets the length of file """
    with open(f_name) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def get_lines(file):
    """Takes the raw log files and extracts Piezo Lines"""
    with open(file, 'r') as infile:
        with open('Combined_Data_File', 'a') as write_file:
            for line in tqdm(infile, total=file_len(file)):
                if re.search('PD-PmpDiodeCrnt-MtrPos', line):
                    write_file.write(line)


# get_lines("2019-04-10T14-09-08.log")
# get_lines("2019-05-01T18-31-59.log")
plot_file("test_test")


""""

Clean File Again

Commit to git

Create Subplot of averages

Create Sublot of histograms

Create Subplot of 2d histgrams

Make data less dense

"""

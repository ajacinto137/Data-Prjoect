from tqdm import tqdm
import re
import numpy as np
from matplotlib import pyplot as plt

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

        # Searches for key word Piezo in lines then seperates all data into corresponding arrays
        for line in tqdm(infile, total=file_len(file)):

            # if re.search('PD-PmpDiodeCrnt-MtrPos', line):
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

        graph_data_mean(fVoltageCavityX, 1000, "fVoltageCavityX_graph")
        graph_data_mean(fVoltageCavityY, 1000, "fVoltageCavityY_graph")
        graph_data_mean(fVoltagePumpX, 1000, "fVoltagePumpX_graph")
        graph_data_mean(fVoltagePumpY, 1000, "fVoltagePumpY_graph")
        graph_data_mean(fSignal, 1000, "fSignal_graph")
        graph_data_mean(fPumpDiodeCurrent, 1000, "fPumpDiodeCurrent_graph")
        graph_data_mean(fMtrPosn, 1000, "fMtrPosn_graph")


def graph_data_mean(array, sample_size, file_name):
    """Graph file by desired sample size"""
    print("Strarting to graph: ")
    arrayLength = len(array)
    remainder = np.mod(arrayLength, sample_size)
    print("now truncating")
    data1 = array[:-remainder]
    averaged_array = np.mean(data1.reshape(-1, sample_size), axis=1)
    plt.plot(averaged_array)
    plt.savefig(file_name + ".png")
    plt.clf()
    print('finished plotting')


def file_len(f_name):
    """gets the length of file """
    with open(f_name) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def get_lines(file):
    """Takes the raw log files and extracts Piezo Lines"""
    with open(file, 'r') as infile:
        lines = infile.readlines()
        with open('Combined_Data_File', 'a') as write_file:
            for line in tqdm(lines):
                if re.search('PD-PmpDiodeCrnt-MtrPos', line):
                    write_file.write(line)


get_lines("2019-04-10T14-09-08.log")
get_lines("2019-05-01T18-31-59.log")
plot_file("Combined_Data_File")

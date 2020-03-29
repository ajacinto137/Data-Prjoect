import datetime;

import numpy as np;
import matplotlib.pyplot as plt;

listPD = [];
listTime = [];


def parse_file(strFilename, listData, listTime):
    nLine = 0;

    with open(strFilename) as fData:
        for strLine in fData:
            if (strLine[30:33] == "[Pi"):
                if (nLine == 0 or nLine == 240000):
                    print(strLine);
                nLine += 1;
                try:
                    if (strLine[30:69] == "[Piezo(Cxy/Pxy)-PD-PmpDiodeCrnt-MtrPos]"):
                        listData.append(float(strLine[70:].split()[4]));
                    else:
                        listData.append(float(strLine[50:].split()[4]));
                    listTime.append(
                        datetime.datetime.strptime(strLine[:23], "%Y-%m-%d %H:%M:%S:%f").timestamp() / 60 / 60);
                except:
                    raise Exception("Error parsing\r\n\t" + strLine);


parse_file("2019-04-10T14-09-08.log", listPD, listTime);
parse_file("2019-05-01T18-31-59.log", listPD, listTime);

listTime = np.array(listTime);
listPD = np.array(listPD);

nSamples = len(listTime);

nDownsamplingPeriod = 1000;
# Truncate to a multiple of the down sampling period.
listTime = listTime[:-(nSamples % nDownsamplingPeriod)];
listPD = listPD[:-(nSamples % nDownsamplingPeriod)];

listMaxPD = listPD.reshape((-1, nDownsamplingPeriod)).max(1);
listMinPD = listPD.reshape((-1, nDownsamplingPeriod)).min(1);

"""
figMain = plt.figure();
axMain = figMain.add_subplot(1, 1, 1);
axMain.plot(listTime[::1000] - listTime[0], listPD[::1000]);
axMain.plot(listTime[::1000] - listTime[0], listMaxPD, "r");
axMain.plot(listTime[::1000] - listTime[0], listMinPD, "r");
axMain.grid();
axMain.set_ylim(0, None);
"""

figHist = plt.figure();
axHist = figHist.add_subplot(1, 1, 1);
axHist.hist2d(listTime - listTime[0], listPD, 100, cmax=10000);  # , [10len(listTime), 10]);
axHist.set_xlabel("Time [hr]");
axHist.set_ylabel("Diagnostic PD [V]");

plt.show();
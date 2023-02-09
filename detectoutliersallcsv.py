import datetime
import csv
import os
import numpy as np

def getsavedcsvfiles():
    try:
        csvfilelist = [x[:-4] for x in os.listdir() if x.endswith(".csv") ]   # select all file names with extension .csv,  remove .csv part
        return csvfilelist
    except:
        csvfilelist = []
    return csvfilelist  # returns list of files with csv extension

def getrows(filename, numberofrows):
    try:
        r = csv.reader(open(filename))
        print("existing file ", filename,"read success...")
        return list(r)[1:][-numberofrows:]   # remove first row always, gather numberoftows number of data
    except:
        print("read error ", filename)
        return 0 

def detectbreakinsequence(array):
    seq1 = int((array[0,0] + array[-1,0])/2)  
    seq2 = int(np.average(array[:,0]))  
    return seq1 != seq2  # detect if there is any break in time sequence, True is there is break

def sliding_window_outliers(array, window_size):  # this funtion from ChatGPT
    breaks = []
    if detectbreakinsequence(array):  # detect if there is any break in time sequence
        breaks.append((int(array[0,0]), int(array[-1,0])))
    outliers = []
    for i in range(len(array) - window_size + 1):
        oneoutlier = []
        window = array[i : i + window_size]
        q1, q3 = np.percentile(window[:, 1], [2, 98])
        iqr = q3 - q1
        lower_bound = q1 - (1.5 * iqr)  
        upper_bound = q3 + (1.5 * iqr)
        oneoutlier =  window[np.where((window[:, 1] < lower_bound) | (window[:, 1] > upper_bound))]        
        if any(np.in1d(outliers,oneoutlier)):
            continue
        outliers.extend(oneoutlier)
    return outliers, breaks

def main(runoncenopromts = False):
    numberofrowstoget = 3500
    windowtoanalyze = 50
    print(">> ",(("run forver","run once and quit")[runoncenopromts == True])," <<")
    listofcollections = []
    listofcollections = getsavedcsvfiles()    # get list of csv files in the working directory
    if len(listofcollections) == 0:
        print("CSV files not found")
        return
    n = 0
    while True:   # forever loop
        for api_symbol in listofcollections:
            print("accessing coin: ", '\033[1;34m', api_symbol, '\033[0;0m')
            filename = api_symbol + ".csv"  # create a filename
            array = np.array(getrows(filename, numberofrowstoget))
            unixtimepricerow = np.array(array[:,[0,2]], dtype = float)

            outliers, breaks = sliding_window_outliers(unixtimepricerow, windowtoanalyze)  
            for i in outliers:
                print(datetime.datetime.fromtimestamp(int(i[0])),i[1])  # print outliers
            for i in breaks:
                print("break in series between", '\033[1;31m',i[0], i[1], '\033[0;0m',"from:" ,datetime.datetime.fromtimestamp(i[0]), "to:", datetime.datetime.fromtimestamp(i[1]))
            n += 1
            print("round: ",n,". Press Ctrl-C to exit." ,sep="")
        if runoncenopromts:
            break

if __name__ == "__main__":
    main(runoncenopromts=True)   # set value True if running only once and quit, good for scheduling; False if to make this script to run forever loop 
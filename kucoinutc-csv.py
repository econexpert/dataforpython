import requests
import time, datetime
import random
import sys
import csv
import os

def savetocsv(datatosave, filename, doyouwantcolumntitles = True):
    try:
        f = csv.writer(open(filename,"a+"))
        firstrow = list(datatosave[0])
        print("saving columns: ", firstrow)
        if doyouwantcolumntitles:
            f.writerow(firstrow)
        for item in datatosave:
            f.writerow([item[gg] for gg in firstrow])
    except:
        sys.exit("error with saving csv file. quiting")

def getsavedcsvfiles():
    try:
        csvfilelist = [x[:-4] for x in os.listdir() if x.endswith(".csv") ]   # select all file names with extension .csv,  remove .csv part
        timeendings = ("1min", "3min", "5min", "15min", "30min", "1hour", "2hour", "4hour","6hour","8hour","12hour", "1day", "1week")
        coinlist,intervalist = zip(*[(x[:x.find("int")],x[x.find("int")+3:]) for x in csvfilelist if x.endswith(timeendings) ]) #select those csv files which ends with interval names
    except:
        coinlist, intervalist = [],[]
    return coinlist, intervalist  # returns list of coins, intervals from saved file names in the working directory

def getlastunix(filename):
    try:
        r = csv.reader(open(filename))
        print("existing file ", filename,"read success...")
        return int(list(r)[-1][0])   # read first column of the last row where is unix timestamp
    except:
        print("did not find file with filename ", filename)
        return 0 

def insertcoinprice(unixtime, pricedate, price, volume):
    pricedate = datetime.datetime.strptime(str(pricedate),"%a %b  %d %H:%M:%S %Y")  # string pricedate to date format
    first = {"unix": unixtime , "date": pricedate ,"price": float(price),"vol": float(volume)} # compose JSON datarow
    return first

def main(runoncenopromts = False):
    # to read more API documentation here https://docs.kucoin.com/#get-klines 
    interval = "1hour"   # change for other interval choices: 1min, 3min, 5min, 15min, 30min, 1hour, 2hour, 4hour,6hour,8hour,12hour, 1day, 1week
    print(">> ",(("run forver","run once and quit")[runoncenopromts == True])," <<")
    listofcollections = []
    listofintervals = []
    try:
        firstpromt = sys.argv  
        gg = [x.upper() for x in firstpromt]
        listofcollections = gg[1:]  # get user input if he or she wants to add new coins
        listofintervals = [interval for x in listofcollections]  # add default time interval for coresponding user input
        if listofcollections == []:
            raise Exception
        print("whole collection:", *listofcollections, "time interval is:", interval)
        savedcoins, savedint = getsavedcsvfiles()    # check if listed coins can be updated in csv files
        addcoins, addint = [],[]
        for c1, int1 in zip(savedcoins,savedint):
            for c2, int2 in zip(listofcollections,listofintervals):
                if (c1 == c2 and int1 != int2):
                    addcoins.append(c1)
                    addint.append(int1)
        listofcollections.extend(addcoins)
        listofintervals.extend(addint)
        if len(listofcollections) > 0:
            print("Found more csv files to update: ", ", ".join("{} {}".format(z1,z2) for z1,z2 in zip(addcoins,addint)))
    except:
        print("no coin pair given. Usage is follows: python3 kucoinutc-csv.py BTC-USDT EHT-USDT")
        listofcollections, listofintervals = getsavedcsvfiles()
        if len(listofcollections) == 0:  # no values given by user, no files in directory - use deault coin and interval
            print("could not fine any saved files, using default values of BTC-USDT with interval of 1hour")
            listofcollections = ["BTC-USDT"]  # some default values if no csv files given
            listofintervals = [interval]  
    n = 0
    while True:   # forever loop
        for api_symbol, interval in zip(listofcollections, listofintervals):
            collection = [] #empy collection before start
            print('\033[1;34m', "updating coin: ", api_symbol, '\033[0;0m')
            filename = api_symbol.replace("/","-") + "int" + str(interval)  + ".csv"  # sanitize file name string replacing unacceptable symbols, add interval indicator
            startunix = getlastunix(filename)
            URL = "https://api.kucoin.com/api/v1/market/candles?type=" + interval + "&symbol=" + api_symbol + "&startAt=" + str(startunix)

            print("API url: ", URL, sep="")
            print("unix time to start: ",startunix) 
            try:
                r = requests.get(url = URL) 
            except: 
                print("some error when getting API data")
            print("api returned status code: ",r.status_code)
            if r.status_code != 200:
                print("some error while accesing api URL.")
                continue

            data = r.json()
            data = data["data"][::-1][:-1]  #get data section, reverse, remove last column (waiting for the final data of the time period)
            if len(data)<1:  # no new data, skip to the next coin
                continue
            for gg in data:
                if startunix < int(gg[0]):    #  time.asctime(time.gmtime(now))  include only new entries, reduce number of zeros in unix time
                    collection.append(insertcoinprice(int(gg[0]),time.asctime(time.gmtime(int(gg[0]))),gg[2],gg[6])) #add more if needed after time gg["high"]
                else:
                    print('\033[1;33m',"waiting for new data...",'\033[0;0m'," last unixtime: ", str(startunix), " now is: ", int(time.time()), sep="")
            if collection != []:
                print(*collection, sep = "\n")
                savetocsv(collection, filename,((False,True)[startunix == 0])) # update database with JSON collection 
                print("csv file updated with ", len(collection), " entries of ", '\033[1;33m', api_symbol, '\033[0;0m', sep="")
            n += 1
            sleeptime = 2 + random.randint(1, 10)  
            print("round: ",n,". sleeping for: ", sleeptime, " sec. press Ctrl-C to exit"," file name: " ,filename, " interval: ", interval ,sep="")
            time.sleep(sleeptime) 
        if runoncenopromts:
            break
        sleeptime = 999 + random.randint(1, 1100)   
        print("===== sleeping for: ", sleeptime, "sec. press Ctrl-C to exit.")
        time.sleep(sleeptime)

if __name__ == "__main__":
    main(runoncenopromts=True)   # set value True if running only once and quit, good for scheduling; False if to make this script to run forever loop 
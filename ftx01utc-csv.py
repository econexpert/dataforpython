import requests
import time, datetime
import random
import sys
import csv

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

    # API request URL example
    # URL = "https://ftx.com/api/markets/BTC/USD/candles?resolution=3600&start_time=1559881511"
def main():
    interval = 60   # 60 (minute) #300 #900 # 3600 (hourly) change here interval 
    collection = []
    try:
        firstpromt = sys.argv  
        gg = [x.upper() for x in firstpromt]
        listofcollections = gg[1:]
        if listofcollections == []:
            raise Exception
        print("whole collection:", *listofcollections, "time interval is:", interval)
    except:
        print("no coin pair given. Usage is follows: python3 ftxutc-csv.py BTC/USD EHT/USD")
        listofcollections = ["BTC/USD"]
    n = 0
    while True:   # forever loop
        for api_symbol in listofcollections:
            collection = [] #empy collection before start
            print('\033[1;34m', "updating coin: ", api_symbol, '\033[0;0m')
            filename = api_symbol.replace("/","-") + "int" + str(interval)  + ".csv"  # sanitize file name string replacing unacceptable symbols, add interval indicator
            startunix = getlastunix(filename)
            URL = "https://ftx.com/api/markets/" + api_symbol + "/candles?resolution=" + str(interval) + "&start_time=" + str(startunix)
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
            data = data["result"]
            data = data[:-1]
            if len(data)<1:  # no new data
                continue
            for gg in data:
                if str(startunix) < str(int(gg["time"]/1000)):    #  time.asctime(time.gmtime(now))  include only new entries, reduce number of zeros in unix time
                    collection.append(insertcoinprice(int(gg["time"]/1000),time.asctime(time.gmtime(gg["time"]/1000)),gg["close"],gg["volume"])) #add more if needed after time gg["high"]
                else:
                    print('\033[1;33m',"waiting for new data...",'\033[0;0m'," last unixtime: ", str(startunix), " now is: ", int(time.time()), sep="")
            if collection != []:
                print(*collection, sep = "\n")
                savetocsv(collection, filename,((False,True)[startunix == 0])) # update database with JSON collection 
                print("csv file updated with ", len(collection), " entries of ", '\033[1;33m', api_symbol, '\033[0;0m', sep="")
            n += 1
            sleeptime = 5 + random.randint(1, 20)  
            print("round: ",n,". sleeping for: ", sleeptime, " sec. press Ctrl-C to exit"," file name: " ,filename, sep="")
            time.sleep(sleeptime)   
        sleeptime = 999 + random.randint(1, 1100)   
        print("===== sleeping for: ", sleeptime, "sec. press Ctrl-C to exit.")
        time.sleep(sleeptime)

if __name__ == "__main__":
    main()
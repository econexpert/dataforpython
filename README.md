# API crypto data saver csv in python

## bybitutc-csv.py

note: uses **Bybit** exchange API   
usage example command line: 
```
python3 bybituts-csv.py BTCUSDT ETHUSDT       
```
add as many pairs as needed or change interval inside the script     

It is better to run each scirpt in seperate directory   



https://github.com/econexpert/dataforpython/assets/7473991/d539dc06-9bb8-4078-b3e8-e3cc1290fa0f



## krakenutc-csv.py    
note: uses **Kraken** exchange API   
usage example command line: 
```
python3 krakenutccsv.py ADAUSD ETHUSD       
```
add as many pairs as needed or change interval inside the script     

It is better to run each scirpt in seperate directory   


## kucoinutc-csv.py  
note: uses **Kucoin** exchange API  
usage example command line: 
```
python3 kucoinutccsv.py BTC-USDT ETH-USDT       
```
add as many pairs as needed or change interval inside the script   

If running on public notebook, place either one of these lines in top of script:    
in Datalore:    
%%python3 kucoinutccsv.py BTC-USDT ETH-USDT     
in Kaggle:     
sys.argv = ("anything","BTC-USDT","ETH-USDT")          
in Deepnote:   
sys.argv = ("anything","BTC-USDT","ETH-USDT")         

## ftx01utc-csv.py  
note: uses FTX exchange API  (discontinued)   
usage example command line: 
```
python3 ftx01utc-csv.py BTC/USD ETH/USD      
```
add as many pairs as needed or change interval inside the script      

![](https://github.com/econexpert/dataforpython/blob/main/images/coinpricecsvsaver.jpg)

## detectoutliersallcsv.py

This program analyzes CSV files containing time series data, detect outliers within sliding windows, and identify breaks in the time series sequence. For analysis it uses all csv files in working directory.

Usage example command line in directory contaning csv files: 
```
python3 detectoutliersallcsv.py
```

Use together with other files to monitor API saving performance. 

![](https://github.com/econexpert/dataforpython/blob/main/images/breakinseries.jpg)

Here is video demonstration how this script works: 

https://github.com/econexpert/dataforpython/assets/7473991/c99e13a6-d304-48ff-a0b6-810d345f248f


# Suggested use in public notebook service

Create empty python notebook and paste following content. Then upload files to the same folder:

```
import importlib, sys
sys.argv = ("anything","BTC-USDT","ETH-USDT") # Change or add other coins
importlib.import_module("kucoinutccsv", sys.argv[1]).main(True)  # True - run once and quit

sys.argv = ("anything","ADAUSD","MANAUSD","DOTUSD")  # Change or add other coins
importlib.import_module("krakenutc-csv", sys.argv[1]).main(True)  # True - run once and quit

print("all done")
```

Tested on Datalore. 

Updates always on my Twitter: 

[![Twitter URL](https://img.shields.io/twitter/url/https/twitter.com/bukotsunikki.svg?style=social&label=Follow%20%40econexpert)](https://twitter.com/econexpert)

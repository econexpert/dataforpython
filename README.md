# API crypto data saver csv in python

## file name: krakenutc-csv.py    
note: uses Kraken exchange API   
usage example command line: **python3 krakenutccsv.py BTCUSD ETHUSD**         
add as many pairs as needed or change interval inside the script     

It is better to run each scirpt in seperate directory   


## file name: kucoinutc-csv.py  
note: uses Kucoin exchange API  
usage example command line: **python3 kucoinutccsv.py BTC-USDT ETH-USDT**       
add as many pairs as needed or change interval inside the script   

If running on public notebook, place either one of these lines in top of script:    
in Datalore:    
%%python3 kucoinutccsv.py BTC-USDT ETH-USDT     
in Kaggle:     
sys.argv = ("anything","BTC-USDT","ETH-USDT")          
in Deepnote:   
sys.argv = ("anything","BTC-USDT","ETH-USDT")         

## file name: ftx01utc-csv.py  
note: uses FTX exchange API  (discontinued)   
usage example command line: **python3 ftx01utc-csv.py BTC/USD ETH/USD**      
add as many pairs as needed or change interval inside the script      

![](https://github.com/econexpert/dataforpython/blob/main/images/coinpricecsvsaver.jpg)

## file name: detectoutliersallcsv.py

This file checks saved csv in working directory for outliers and for break in time sequence. 

Use together with other file to monitor API saving performance. 

# csv data for python
csv files to use in python apps. Updated only occasionally

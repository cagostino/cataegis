import pandas_datareader.data as web
from pandas_datareader.data import Options
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import os
import numpy as np
###
datfold = './data/'
today =  datetime.today().date()
def getstockopts(stockname,save =True):
	opts = Options(stockname,'yahoo')
	expirydates = opts.expiry_dates
	dateexp = datetime(2017,12,15)#manually set to this
	calldata = opts.get_call_data(expiry=dateexp)
	putdata = opts.get_put_data(expiry=dateexp)
	prices = web.DataReader(stockname,'yahoo',today)

	call_impt = calldata[['Last','Open_Int','Underlying_Price']]
	call_indexed_impt = call_impt.reset_index()

	put_impt = putdata[['Last','Open_Int','Underlying_Price']]
	put_indexed_impt = put_impt.reset_index()
	datstr=str(today.date())
	comb_indexed_impt = pd.concat([call_indexed_impt,put_indexed_impt])
	comb_indexed_impt.index = [datstr]*len(comb_indexed_impt.index)
	prices_indexed =prices.reset_index()
	prices_indexed.index = [datstr]*len(prices_indexed.index)
	if save:
		foldlists = os.listdir(datfold)
		
		foldname = stockname +'/'

		if stockname not in foldlists:
			os.mkdir(datfold+foldname)
			os.mkdir(datfold+foldname+'options/')
			os.mkdir(datfold+foldname+'prices/')
		stockoptlist = os.listdir(datfold+foldname+'options/')
		stockpricelist = os.listdir(datfold+foldname+'prices/')
		stockoptname = stockname+'-options.csv'
		stockpricename=stockname+'-prices.csv'
		if stockoptname not in stockoptlist:
				
			comb_indexed_impt.to_csv(datfold+foldname+'options/'+stockoptname)	
		else:
			comb_indexed_impt.to_csv(datfold+foldname+'options/'+stockoptname,mode='a',header=False)
		
		if stockpricename not in stockpricelist:
			prices_indexed.to_csv(datfold+foldname+'prices/'+stockpricename)	
		else:
			prices_indexed.to_csv(datfold+foldname+'prices/'+stockpricename,mode='a',header=False)
	print('stock : ' +stockname + ' DONE')
	#callstrikes = call_indexed_impt['Strike'].iloc[:]
	#callexpiries = call_indexed_impt['Expiry'].iloc[:]
	#calltypes = call_indexed_impt['Type'].iloc[:]
	#callsymbols = call_indexed_impt['Symbol'].iloc[:]
	#calllasts = call_indexed_impt['Last'].iloc[:]
	#callopens = call_indexed_impt['Open_Int'].iloc[:]
	#callunderlying_prices = call_indexed_impt['Underlying_Price'].iloc[:]

	#putstrikes = put_indexed_impt['Strike'].iloc[:]
	#putexpiries =put_indexed_impt['Expiry'].iloc[:]
	#puttypes =put_indexed_impt['Type'].iloc[:]
	#putsymbols = put_indexed_impt['Symbol'].iloc[:]
	#putlasts = put_indexed_impt['Last'].iloc[:]
	#putopens = put_indexed_impt['Open_Int'].iloc[:]
	#putunderlying_prices = put_indexed_impt['Underlying_Price'].iloc[:]
def runstocklist(listofstocks):
	for stock in stocklist:
		getstockopts(stock)
stocklist = ['SPY','SSO','SDS']	
runstocklist(stocklist)

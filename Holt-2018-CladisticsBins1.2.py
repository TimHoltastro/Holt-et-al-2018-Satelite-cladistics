# -*- coding: utf-8 -*-
"""
Created on Thu Aug  3 10:21:25 2017


-------------------Cladistical Binning Program-----------------------

Version 1.2

@author: Tim

The aim of this program is to take continious data and put it into bins, in prperation for use in cladistical analysis. This program itterates each characteristic individually. Note: it will fail if there is only one known datapoin for a specific characteristic. 
"""

#modules
import numpy as np
from scipy import stats
import pandas as pd
import time
import sys


'''
----------------------------Variables------------------------------
These are to be inputted
'''

#csv file
file = 'SatDataLarge.csv'

#Columns to be binned - remember it starts with 0, which should be names anyway
allcol = [3,4,5,6,7] #a,e,i,Density,Albedo
#allcol = [3,4,5,6,7,8,9,10,11] #With colours


#reversed columns - if the bins need to be itterated largest to smallest
revcol = [6] #or [5]                    #-----need to use 'or' oporator between them, use 0 for none. 

#r^2 threshold - the threshold for an acceptable r^2 value
r2thresh = 0.99


'''
Generated values
'''
#Current date and time
DatetimeNow = time.strftime("%Y%m%d-%H%M%S")

#sending the output to a text file.
outputfile = '{}-CladisticsBins-{}-{}'.format(file, r2thresh, DatetimeNow)
outputtext = outputfile+'.txt'
sys.stdout = open(outputtext,'wt')

 #to make sure it doesn't truncate.
pd.set_option('max_rows', None)  
pd.set_option('max_columns', None) 
pd.set_option('display.max_columns', None)  
pd.set_option('display.max_rows', None)  
np.set_printoptions(threshold=np.inf)

#---Print at the top of the Text file
print('----------Cladistics bining Program------------')
print('--Version 1.1---')
print('--Created by Timothy Holt--')
print('')
print('Bins Created:', DatetimeNow)
print('')
print('Matrix used:',file)
print('r^2 thresthold:', r2thresh)


'''
--------Matricies-------------
'''

#-importing the matrix
data = pd.read_csv(file, encoding = "ISO-8859-1")

#print(data)

binstats = np.empty((0,5))              # statics without names get's overridden

#-creating parameters based on matrix



'''
----Finding the bins------
'''
#select the columns
selcol = data.iloc[:,allcol]
revselcol = data.iloc[:,revcol]





#print(selcol)

##-do this for each of the columns-

for column in selcol:
           
    print('')
    print('-----', column, '-----')                           #Printing the column name
        
        
        #--need to deal with ? - changes them to NaN
    seleccolcol = pd.to_numeric(selcol[column], errors='coerce')
        
        #Nans need to be excluded
    selcolnonan = seleccolcol[np.isfinite(seleccolcol)]
        #print(selcolnonan)
        
        
    binNum = 0
    
       #--- bin loop start--- 
    while True:     
        binNum = binNum + 1
        
        #Creating and assinging bins
        bins = pd.cut(selcolnonan, binNum, labels=False, retbins=True)
        binvalues = bins[0]
        bindelims = bins[1]
         
    
            
  
                    
        #------Stats ---------- 
               
        #print(binsnonan)
    
        #slope(0), intercept(1), r_value(2), p_value(3), std_err(4) = stats.linregress(x,y)
        
        m, b, r, p, err = stats.linregress(selcolnonan, binvalues)
        stat = [m,b,r,p,err]
        binstats = np.append(binstats, [stat], axis=0)
        
        ####-check the r2value- 
            #--if the r2 value is less than r2thresh, redo the binning, with numbin+1. if r2 > r2thresh, stop the loop
        if stat[2]**2 > r2thresh:
            break
        #--bin loop end-----
        
        
#Reversal
    if column == revselcol.columns:
        bindelimsrev = np.flipud(bindelims)             #flipping the deliminaters
        #binning the values
        binvaluesrevv = np.digitize(selcolnonan, bindelimsrev)   
        binvaluesrev = pd.Series(binvaluesrevv, index=binvalues.index)
        
        
        
         

        
    #####-Loop values-
        #--print out the bin values to a text file, with the header and r^2 value

###---Common to forward and reverse----
    #printing the final bin numbers
    print('Bin Number:', binNum)
    #R^2 value.
    print('R^2 value:', stat[2]**2)




    
    
    
#Printing forward Bin delimators 
    if column != revselcol.columns:
        #print('Bin deliminators:',  bindelims)
        print("Bin Deliminators: {}".format(bindelims))
        #--update the matrix--  
        data[column].update(binvalues)
    
##---reverse-----    
    if column == revselcol.columns:
        print('Reversed')
        print('Bin deliminators:',  bindelimsrev)
        #--update the matrix--  
        data[column].update(binvaluesrev)
        
        
'''
Output the data
'''

print('')
print(data)


#--create a new csv file based on the updated matrix--

outputcsv = outputfile+'.csv'
data.to_csv(outputcsv, index=False)



















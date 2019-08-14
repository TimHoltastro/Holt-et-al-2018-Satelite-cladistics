# -*- coding: utf-8 -*-
"""

-----------Dispersal Velocity Calculator--------

@author: Tim Holt
Version 1.11

This program is designed to calculate the dispersal velocity of orbiral objects in semi-major axis (a), eccentricity (e), inclination (i) space. 

--Input--
The input matrix must be a csv file, in the format name,a,e,i. a values must be in kilometers. e is a non-parametric value. i is in degrees. Only values must be used in the matrix, no units. The first object is used as the reference object. Name of the reference object is taken as name of the cluster.  
The true anomaly (w) and perihelion argument (f) are from the point of impact and dispersion. As this is generally unkown, values muct be inputted. 
The period of the reference object needs to be inputted directly. Must be in days. 

--Output--
A text file with the dispersal velocities for each object to the reference object. Only values are given not units. 
minimum, maximum mean and SD values for the cluster
"""

#modules
import numpy as np
import matplotlib.pyplot as plt 
import pandas as pd
import math
import sys
import time
from mpl_toolkits.mplot3d import Axes3D



#--- input peramiters---

file = 'PasiphaeSub2.csv'                            #csv file
p = 708                                  #period in days

# Unkown values that need to be entered in degrees
fdeg = 90                                       # true anomaly (f) in degrees
fwdeg = 45                                       # perihelion argument (f + w) in degrees


#---Calculation paramiters---
#period translated into seconds - translated into orbital frequency
psec = p * 86400
n = ((2 * math.pi) / psec)

f = math.radians(fdeg)
fw = math.radians(fwdeg)




#bringing in the csv flie
#convert it to a pandas dataframe
data = pd.read_csv(file)

#add on an additional column for the dispersal velocities
data['dV'] = ""
#print (data)


#Creating the name for the family, based on the reference object. 
family = data.iloc[0]['Satellite']
#sending the output to a text file.
DatetimeNow = time.strftime("%Y%m%d-%H%M%S")
outputfile = '{}-DispersalVelocity-{}'.format(file, DatetimeNow)
outputtext = outputfile+'.txt'
sys.stdout = open(outputtext,'wt')

print('')
print('---------------- ', family, 'family ----------------')
print('')
#list of members of the cluster
pd.set_option('max_rows', 999999)   #to make sure it doesn't truncate.
pd.set_option('max_columns', 999999)
members = data.loc[:,'Satellite'].values

print('Members:', members)



#--reference values--
print('')
print ('---Reference values---')
print('Reference object:', family)
ar = 1000*data.iloc[0]['a']                     #Semimajor axis in km to m
print('Semi-major axis:', ar, 'm')
er = data.iloc[0]['e']                          #eccentricity
print('Eccentricity:', er)
ir = math.sin(math.radians(data.iloc[0]['i']))  #inclination in deg to radians
print('Inclination:', ir, 'radians')
print('Peroid:', p, 'days')

'''
#----Graphs----
#a vs e
plt.figure(1) 
plt.grid()
plt.scatter(data['a'], data['e'])  
#plt.annotate((data['a'], data['e']), data['Satellite'])
plt.title(family+' family: Semimajor axis vs Eccentricty')
plt.xlabel('a (km)')
plt.ylabel('e')
saveae = outputfile+'.ae.pdf'
plt.savefig(saveae)
#plt.show()

#a vs i
plt.figure(2) 
plt.grid()
plt.scatter(data['a'], data['i'])  
#plt.annotate((data['a'], data['e']), data['Satellite'])
plt.title(family+' family: Semimajor axis vs Inclination')
plt.xlabel('a (km)')
plt.ylabel('i (degrees)')
saveai = outputfile+'.ai.pdf'
plt.savefig(saveai)
#plt.show()


#a vs e vs i (3d)
threedee = plt.figure().gca(projection='3d')
threedee.scatter(data['a'], data['e'], data['i'])
threedee.set_title(family+' family: Semimajor axis vs Eccentricity vs Inclination')
threedee.set_xlabel('a (km)')
threedee.set_ylabel('e')
threedee.set_zlabel('i (degrees)')
saveaei = outputfile+'.aei.pdf'
plt.savefig(saveaei)
#plt.show()
'''


#----Calculations----
#loop through each of the lines in the array

for index, row in data.iterrows():
    print ('')
    print (row['Satellite'])
    da = (1000*row['a'])-ar                     ##Semimajor axis in km to m
    print ('da = ', da)
    de = row['e']-er                            #eccentricity
    print ('de = ',de)
    di = math.sin(math.radians(row['i']))-ir    #inclination in deg to radians
    print ('di = ', di)

#--delta V--
#each of the derived Gauss equations
    

    dvreq1 = (n*ar)/(math.sin(f)*(math.sqrt(1-er**2)))
    dvreq2 = (de*((1+er*math.cos(f))**2))/(1-er**2)
    dvreq3 = (da*(er+2*math.cos(f)+er*(math.cos(f)*math.cos(f))))/(2*ar)
    dVR = dvreq1*((dvreq2)-(dvreq3)) 
    print ('dVR = ', dVR) 
    
    dvteq1 = (n*ar)*(1+er*math.cos(f))
    dvteq2 = math.sqrt(1-er**2)
    dvteq3 = da/(2*ar)
    dvteq4 = (er*de)/(1-er**2)
    
    dVT = (dvteq1/dvteq2)*(dvteq3-dvteq4)
    #dVT = ((n*ar*(1+er*math.cos(f)))/(math.sqrt(1-er**2)))*((da/2*ar)-((er*de)/(1-er**2)))
    print('dVT =', dVT)    
    
    
    """
    OLD ONES
    dVR = (da/ar)*((n*ar*math.sqrt(1-er**2))/(4*(er*math.sin(f))))
    print ('dVR = ', dVR)
    
    dVR = ((n*ar)/((math.sin(f))*(math.sqrt(1-er**2))))*((de*((1+er*math.cos(f))**2)/(1-er**2))-((da*(er+er*(math.cos(f)*math.cos(f))+(2*math.cos(f))))/(2*ar)))
 
    dVT = ((n*ar*(1+er*math.cos(f)))/(er+2*math.cos(f)+er*(math.cos(f)*math.cos(f))))*((de)/(math.sqrt(1-er**2))-(math.sqrt(1-er**2))/(4*er)*(da/ar))
    print('dVT =', dVT)
    """
    
    dVW = ((n*ar*di)/(math.sqrt(1-er**2)))*((1+er*math.cos(f))/(math.cos(fw)))
    print('dVW =', dVW)
   
#the combined velocity formula
    dV = math.sqrt(dVR**2+dVT**2+dVW**2)
    print('dV =', dV)

#updating the velocity into the dataframe
    data.loc[index,'dV'] = dV
    
#--end of loop--
    
#-----Updated dataframe-------    

print ('')
print ('-------- Summary and statistics --------')
print ('')
print ('f = ',fdeg, 'degrees ---- f + w = ', fwdeg)
print ('')
print (data)
print ('')

#----Statistics-----
#minimum, maximum mean and SD values for the cluster
#print them, perhaps output to a text file. 


data = data.replace(0, np.NaN)              #to get rid of the '0' value for the reference 

Vmin = data['dV'].min()
print ('Minimum deltaV value', Vmin, 'm/s')

Vmax = data['dV'].max()
print ('Maximum deltaV value', Vmax, 'm/s')

Vmean = data['dV'].mean()
print ('Mean deltaV value', Vmean, 'm/s')

Vstd = data['dV'].std()
print ('Standard deviation of deltaV value', Vstd, 'm/s')


import numpy as np
import matplotlib.pyplot as plt 
import pandas as pd
import scipy as sp
from scipy import optimize
from scipy import stats

def line(x,slope,intercept):
    return (slope * x) + intercept
    
    '''sigma values taken from Table 1 of the gain measurement protocol as bin error times sqrt(2)'''

Chip3 = pd.DataFrame({'chip_id' : 3, 
                      'VDDA'    : 1.484 ,
                      'Input Voltage(mV)' : [1816,1280,910,640,460,364,330,292.4,261.2,186.8,164.4,145.6,129,94.4],
                      'Output Voltage(mV)':[1102,1100,1024,781.6,580.8,460.8,414.8,
                                            370.8,328,235.2,207.6,183.8,164.8,119],
                      'sigma':np.sqrt(2)*np.array([2.886751346,2.886751346,2.309401076,2.309401076,2.309401076,
                                                   2.309401076,1.154700538,1.154700538,1.154700538,1.154700538,
                                                   1.154700538,0.57735027,0.57735027,0.57735027])
                    })

Chip5 = pd.DataFrame({'chip_id' : 5, 
                      'Input Voltage(mV)' : [1810.2,1270.2,908,640,465.6,369.6,332,295.2,260,183,162.4,145.4,128.8,94.2],
                      'Output Voltage(mV)':[1078,1076,1026.4,784.8,583.2,468,416.4,
                                            369.2,329.2,235.2,208.2,187.8,166.8,121.2],
                      'sigma':np.sqrt(2)*np.array([2.886751346,2.886751346,2.309401076,2.309401076,1.154700538,
                                                   1.154700538,1.154700538,1.154700538,1.154700538,0.57735027,
                                                   0.57735027,0.57735027,0.57735027,0.57735027])
                     })

Chip10 = pd.DataFrame({'chip_id' : 10, 
                      'Input Voltage(mV)' :[1789.6,1268.4,901.6,629.6,465.2,370,327.6,
                                            291.98,259.5,183.4,162.8,145.2,130.2,94],
                      'Output Voltage(mV)':[1110,1090.4,1022.4,772,572.4,460.8,409.6,
                                            366.8,325.6,229.8,206.4,184.8,163.2,117.8],
                       'sigma':np.sqrt(2)*np.array([2.886751346,2.309401076,2.309401076,2.309401076,1.154700538,
                                                    1.154700538,1.154700538,1.154700538,1.154700538,0.57735027,
                                                    0.57735027,0.57735027,0.57735027,0.57735027])
                     })




#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~VDDA was 1.8V for the data below~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Chip3_2 = pd.DataFrame({'chip_id' : 3, 
                      'Input Voltage(mV)' : [1810,1268.8,898.4,635.2,460,364,330,
                                             292.4,261.2,186.8,164.4,145.6,129,94.4],
                      'Output Voltage(mV)':[1386,1352.8,1124,816.8,596.8,460.8,414.8,
                                            370.8,328,235.2,207.6,183.8,164.8,119]
                    })

Vin  = 'Input Voltage(mV)'
Vout = 'Output Voltage(mV)'

def chip_gain(Chip , n=4 , m=0):
    '''Plots three plots. The first plot contains all data points along with linear fit for the region specified by n, 
       Which is the index number to start the fit from. The second plot is a closeup of the fit along with the predicted
       gain(slope) and intercept values. The third plot contains the resudual values and errobars resulting from bin 
       errors. Also adds a gain column to the chip dataframe.'''
    
    zero = ([0]* Chip['Output Voltage(mV)'])
    
    chip_gain    = Chip['Output Voltage(mV)'] / Chip['Input Voltage(mV)']    #Calculating the gain
    Chip['Gain'] = chip_gain                                                 #Adding the gain to the dataframe
    chip_id      = Chip['chip_id'][0]
    
    
    fit = sp.optimize.curve_fit(line,                       #Scipy curve fitter. Returns fit parametes as first element
                                Chip.loc[n:][Vin],          # and Covariance matrix as second element. The diagonals of 
                                Chip.loc[n:][Vout],         #the covariance matrix contain the errors in the predicted 
                                sigma = Chip['sigma'][n:],  #values squared.
                                absolute_sigma=True)                     
    
    slope     = fit[0][0]
    intercept = fit[0][1]
    residuals = line(Chip.loc[n:][Vin],slope,intercept) - Chip.loc[n:][Vout]  #Predicted - measured


    slope_err     = np.sqrt(np.diag(fit[1]))[0]
    intercept_err = np.sqrt(np.diag(fit[1]))[1]

    
    
    #~~~~~~~~~~~~~~~~~~~~~~~~Plots~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    fig , ax = plt.subplots(3)

    ax[0].plot(Chip.loc[m:][Vin] , Chip.loc[m:][Vout] , 'r8', label = 'VDDA = {}V'.format(Chip['VDDA'][0]))   
    ax[0].plot(Chip.loc[n:][Vin] , line( Chip.loc[n:][Vin] , slope , intercept) , 'c',
        label = 'Region used for linear gain analysis' )
    
    
    ax[1].plot(Chip.loc[n:][Vin] , Chip.loc[n:][Vout] , 'r8',label = '')
    ax[1].plot(Chip.loc[n:][Vin] , line( Chip.loc[n:][Vin] , slope , intercept) , 'c',
                label = r'Gain Fit = {:.3f} $\pm {:.3f}$, '.format(slope , slope_err) + 
                r'intercept = ({:.1f} $\pm {:.1f}$)mV'.format(intercept,intercept_err) )    
    
    ax[2].plot(Chip.loc[n:][Vin] , residuals ,'r8')
    ax[2].plot(Chip.loc[n:][Vin] , zero[n:] ,'r' )
    ax[2].errorbar(Chip.loc[n:][Vin] , residuals ,yerr = Chip['sigma'][n:] ,color ='c')
    
    ax[0].set_title('Chip {} Gain'.format(chip_id))
    ax[0].set_ylabel('Output Voltage(mV)')
    ax[0].set_xlabel('Input Voltage (mV)')
    
    ax[1].set_xlabel('Input Voltage (mV)')
    ax[1].set_ylabel('Output Voltage(mV)')

    ax[2].set_title('Residual Plot')
    ax[2].set_xlabel('Input Voltage (mV)')
    ax[2].set_ylabel('Predicted - Measured(mV)')
      
    ax[0].legend(loc=0)
    ax[1].legend(loc=8)
    
    ax[0].grid()
    ax[1].grid()
    ax[2].grid()
    plt.rcParams['figure.figsize'] = [12,15]
    plt.rcParams['font.size'] = 22
    plt.tight_layout()

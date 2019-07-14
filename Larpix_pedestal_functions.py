
# coding: utf-8

# In[5]:

"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Larpix Pedestal Voltage Testing Functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""

# Some of these modules aren't used but I forgot which
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import h5py
get_ipython().magic('matplotlib inline')
import scipy as sp
from scipy import stats
from pylab import *
import json


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ADC values are roughly linearly related to Vref and Vcm voltage Values, where
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Vcm (measured to be ~0.2V) corresponds to 0 ADCs and Vref(measured to be~0.45V)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~corresponds to 255 ADCs
adc_values=np.linspace(0,255,256)

def adc_to_voltage(adc_vals):
    return(0.2 + adc_vals * (0.45-0.2)/(255))
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Functions used for most tests where an h5 file is to be analyzed:


def dataframe(h5_file_path):
    '''Given an h5 file in the form of a string leading to its directory, this function will first create Python object called 
    file, this will then be fed into pandas to create a dataframe table with the columns for channel, chip, and raw ADC values'''
    
    file = h5py.File(h5_file_path)
    
    #Indexes within h5 file
    Channel = 0 
    Chip_ID = 1
    Raw_ADC = 5
    
    return pd.DataFrame({'Channel': [file['data'][i][Channel] for i in range(len(file['data']))],
                         'Chip':    [file['data'][i][Chip_ID] for i in range(len(file['data']))],
                         'Raw ADC': [file['data'][i][Raw_ADC] for i in range(len(file['data']))]
                  })

def analysis_single_channel(Data,
                             channel,
                             chips = [3,5,10,12]):
    '''Returns the gaussean fit parameters for a single channel. Data is in the form of a pandas dataframe'''
    
    num_chips = range(len(chips))     
    
    Chips = [Data.where(Data['Chip'] == chips[chip]).where(Data['Channel'] == channel).apply(
             lambda x: pd.Series(x.dropna().values)) for chip in num_chips]
    
    data = np.array([Chips[chip]['Raw ADC'].apply(adc_to_voltage).values for chip in num_chips])    
    
    fit = [sp.stats.norm.fit(data[chip]) for chip in num_chips]
    
    return fit
    
def sample_cycles_analysis_individual_channels(
    
    sample_cycles, 
    sample_cycles_vals =[1,2,3,4,5,6,7,8,9,10,15,20,25],
    channels = range(32) ,
    chips = [3,5,10,12]
    ):    
    
    '''New pcb has chips 3,5,10,12 instead of previous 200 series. This function does all channels and all chips by default.
    Sample cycles is a list of dataframes, each corresponding to a different value of sample cycles, the corresponding 
    numerical values are used in sample_cycles_vals. This function will create one plot for each channel in its arguments. 
    Each plot contains plots for each chip's  adc voltage value vs the corresponding value of sample cycles'''
    
    num_chips = range(len(chips))
    num_cycles = range(len(sample_cycles))
    
    for channel in channels :
        
        ch_analysis = [analysis_single_channel(sample_cycles[value] ,channel,chips) for value in num_cycles]
        
        separated_chips = [[ch_analysis[value][chip] for value in num_cycles] for chip in num_chips] 

        pedestal = 0
        rms = 1
        
        chip_pedestals = [[separated_chips[chip][value][pedestal] for value in num_cycles] for chip in num_chips]
        
        chip_rms = [[separated_chips[chip][value][rms] for value in num_cycles] for chip in num_chips]

        '''~~~~~~~~~`~~~~~~~~~~~~~~~~~~~~~~~~Want to graph all chips on same plot~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'''
        plt.figure()
        
        for chip in num_chips:
            plt.errorbar(
                sample_cycles_vals,chip_pedestals[chip],yerr=chip_rms[chip],capsize=5,label='Chip {}'.format(chips[chip])
            )

        plt.legend()
        plt.grid()
        plt.title('Pedestal Voltage measurement and RMS for Channel {}'.format(channel))
        plt.xlabel('Sample Cycles')
        plt.ylabel('Pedestal Voltage(V)')
        plt.rcParams['figure.figsize']=[17,10]
        plt.rcParams['font.size']=25
        plt.show()
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#For cross trigger testing:

def data(json_file_path):
    '''This function is used when JSON files have been created using the run_calibration script. This happend when there is a
    cross-trigger test, and the script removes bad packets from the DAT file along with the channels that were being triggered.
    The output of this function is a Dict object and the argument taken is the JSON file path'''
    with open(json_file_path, "r") as read_file:
        file = json.load(read_file)
    return file

def json_analysis(
    sample_cycles,
    sample_cycles_vals,
    channels = range(32),
    chips =[3,5,10,12]):
    
    '''Sampe cycles is a list containing the data files run through the data function above'''
    chip_strings = [str(chips[i]) for i in range(len(chips))]
    channel_strings = [str(channels[i]) for i in range(len(channels))]
    
    num_chips = range(len(chips))
    num_cycles = range(len(sample_cycles))
    
    
    for channel in channel_strings:
        
        pedestal_v= [[sample_cycles[j][i][channel]['pedestal_v'] for j in num_cycles] for i in chip_strings]
        pedestal_rms= [[sample_cycles[j][i][channel]['pedestal_v_sigma'] for j in num_cycles] for i in chip_strings]
        
        plt.figure()
        
        for chip in num_chips:    
            
            plt.errorbar(sample_cycles_vals , pedestal_v[chip] , yerr=pedestal_rms[chip],capsize=5,
                         label='Chip {}'.format(chips[chip]))
            
        plt.legend()
        plt.grid()
        plt.title('Pedestal Voltage measurement and RMS for Channel {}'.format(channel))
        plt.xlabel('Sample Cycles')
        plt.ylabel('Pedestal Voltage(V)')
        plt.rcParams['figure.figsize']=[17,10]
        plt.rcParams['font.size']=25
        plt.show()


# In[ ]:




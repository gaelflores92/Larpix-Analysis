import numpy as np
import matplotlib.pyplot as plt
from matplotlib.cbook import get_sample_data
import pandas as pd
from IPython.core.display import display, HTML

Chip3 = pd.DataFrame({'chip_id' : 3, 
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

def least_squares(Chip,Sigma,n):
'''Returns array with first element being slope and its unceratinty and second element being the intercept along 
with its uncertainty. n is used to cut off nonlinear parts'''

#~~~~~~~~~~~~~~~~~~~~~~~~~~Data~~~~~~~~~~~~~~~~~~~~~~~~~~~~

x = Chip['Input Voltage(mV)'][n:]
y = Chip['Output Voltage(mV)'][n:]
sigma =Chip['sigma'][n:]                                        #Output voltage uncertainities
chip_id = Chip['chip_id'][0]

#~~~~~~~~~~~~~~~~~~~~~~~~~~Math~~~~~~~~~~~~~~~~~~~~~~~~~~~~

w = 1/(sigma**2)                                                #Weights from uncertainties

Delta = sum(w)*sum(w*x**2) - sum(w*x)**2

A = (sum(w*(x**2))*(sum(w*y)) - sum(w*x) * sum(w*x*y))/Delta    #Intercept prediction
B = (sum(w) * sum(w*x*y) - (sum(w*x)*sum(w*y)))/Delta           #Slope prediction

sigma_A = np.sqrt(sum(w*x**2)/Delta)                            #Intercept Uncertainty 
sigma_B = np.sqrt(sum(w)/Delta)                                 #Slope Uncertainty

#~~~~~~~~~~~~~~~~~~~~~~~~~~Plots~~~~~~~~~~~~~~~~~~~~~~~~~~~~

fig,ax = plt.subplots()

ax.plot(x,y,'r8',label = 'Measured')
ax.plot(x,B*x + A , label = r'$Gain={:.3f}\pm{:.3f}, Intercept:({:.1f} \pm{:.1f})mV$'.format(B,sigma_B,A,sigma_A))

ax.set_xlabel('Input Voltage(mV)')
ax.set_ylabel('Output Voltage(mV)')
ax.set_title('Chip {} Gain'.format(chip_id))
ax.legend()

plt.rcParams['figure.figsize']=[16,8]
plt.rcParams['font.size']=25

return np.array([np.array([B,sigma_B]),np.array([A,sigma_A])])

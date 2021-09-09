
"""
Created on Tue Jun  8 13:40:52 2021

@author: Sandra
-Saves the data into a buffer first, then file
-It's easier when the trigger parameters are adjusted on the device, not in code
"""
import pyvisa
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import os
import time
import math

# os.chdir('c:/Users/Sandra Drusova/Nextcloud/Postdoc/Apps/Python')


rm = pyvisa.ResourceManager()
rm.list_resources()

inst = rm.open_resource('USB0::0x2A8D::0x0397::CN60144301::0::INSTR')
# inst = rm.open_resource('TCPIP0::169.254.63.147::hislip0::INSTR')

# Constants
inst.timeout=15000 
dt=5 # in seconds. Maximum allowed time of data collection
f=1 # Hz, laser repetition rate


inst.write(':WAVeform:UNSigned 1')
inst.write(':WAVeform:BYTeorder LSBFirst')
inst.write(':WAVeform:FORMat WORD ')
inst.write(':ACQuire:COMPlete 100')
inst.write(':WAVeform:POINts:MODE MAXimum')
inst.write(':WAVeform:SOURce MATH')
valuelist=list()

preamble=inst.query('WAVeform:PREamble?')
points=int(preamble.split(",")[2])
timestep=float(preamble.split(",")[4])


# Collects data only for dt interval after the first pulse
start = time.time()

while True:
    try:
        if len(valuelist)>1:
            if time.time() > start + dt :
                break
        valuelist.append(inst.query_binary_values(':WAVeform:DATA?', datatype='H', is_big_endian=False))
        if len(valuelist)==1:
            start = time.time()

    except pyvisa.VisaIOError:
        inst.clear()
        break
 

fired_pulses=math.ceil(dt*f)+1
caught_pulses=len(valuelist)
print(caught_pulses/fired_pulses*100)

        
# PLOT section
data = np.asarray(valuelist)
x = np.array(range(data.shape[1]))*timestep*1e6 #x axis based on nr of columns
# x = np.array(range(data.shape[1])) #x axis based on nr of columns
# data = np.transpose(data)
plt.plot(x,data[0,:]) #plots column 1
plt.xlabel("Time axis (us)")


# Data saving
now=datetime.now().strftime("%Y%m%d-%H%M%S")

with open('Data/'+now+'.txt', "w") as f:
    f.write(preamble)
    f.write("\n")
    np.savetxt(f, data.T, delimiter=" ", newline="\n")
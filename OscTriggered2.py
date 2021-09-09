
"""
Created on Tue Jun  8 13:40:52 2021

@author: Sandra

Saves the data right away into the file, doesn't buffer
"""
import pyvisa
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import os
import time

# os.chdir('c:/Users/Sandra Drusova/Nextcloud/Postdoc/Apps/Python')

rm = pyvisa.ResourceManager()
rm.list_resources()

inst = rm.open_resource('USB0::0x2A8D::0x0397::CN60144301::0::INSTR')
# inst = rm.open_resource('TCPIP0::169.254.63.147::hislip0::INSTR')
inst.timeout=10000

inst.write(':WAVeform:UNSigned 1')
inst.write(':WAVeform:BYTeorder LSBFirst')
inst.write(':WAVeform:FORMat WORD ')
inst.write(':ACQuire:COMPlete 100')
inst.write(':WAVeform:POINts:MODE MAXimum')
inst.write(':WAVeform:SOURce MATH')

valuelist=list()
exectime=list()

preamble=inst.query('WAVeform:PREamble?')
points=int(preamble.split(",")[2])
timestep=float(preamble.split(",")[4])


now=datetime.now().strftime("%Y%m%d-%H%M%S")

with open('Data/'+now+'.txt', "a") as f:
    f.write(preamble)
    f.write("\n")
    
    while True:
        try:
            values=inst.query_binary_values(':WAVeform:DATA?', datatype='H', is_big_endian=False)
            start_time = time.time()
            data = np.asarray([values])
            np.savetxt(f, data, delimiter=" ", newline="\n")
            f.write("\n")
            elapsed = time.time()
            exectime.append((elapsed - start_time))
        except pyvisa.VisaIOError:
            inst.clear()
            break
            
    # PLOT section plots the last dataset
    x = np.array([range(data.shape[1])])*timestep*1e6
    plt.plot(x.T,data.T) #plots column 1





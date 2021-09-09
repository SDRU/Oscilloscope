# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 13:40:52 2021

@author: Yakub and Sandra

Continuously acquires the data and saves them with a timestamp if needed
Good for testing how long time the data transmission and saving takes
"""
import pyvisa
import numpy as np
import time
import pandas as pd
from datetime import datetime

rm = pyvisa.ResourceManager()
print(rm.list_resources())

inst = rm.open_resource('USB0::0x2A8D::0x0397::CN60144301::0::INSTR')
# inst = rm.open_resource('TCPIP0::169.254.63.147::hisplip0::INSTR')


print(inst.query("*IDN?")) # ID of the device
# inst.write(':DIGitize') # Acquire data
print(inst.query(':WAVeform:POINts?'))

inst.write(':WAVeform:UNSigned 1')
inst.write(':WAVeform:BYTeorder LSBFirst')
inst.write(':WAVeform:FORMat WORD')
inst.write(':ACQuire:COMPlete 100')
inst.write(':WAVeform:SOURce MATH')
inst.write(':WAVeform:POINts:MODE MAXimum')
# inst.write(':AUToscale:AMODE NORMal')
# inst.write(':ACQuire:MODE RTIMe')


preamble=inst.query(':WAVeform:PREamble?')
print(preamble)
points=int(preamble.split(",")[2])
timestep=float(preamble.split(",")[4])

exectime=list()

now=datetime.now().strftime("%Y%m%d-%H%M%S")
f=open(now+'.txt', 'a')
f.write(preamble)
f.write("\n")

# One dataset only
# try:
#     # inst.write(':WAVeform:POINTS 50000')
#     values = inst.query_binary_values(':WAVeform:DATA?', datatype='H', is_big_endian=False)


# Loop
try:
    while True:
        start_time = time.time()

        values = inst.query_binary_values(':WAVeform:DATA?', datatype='H', is_big_endian=False)
        data = np.asarray(values)
        
        now=datetime.now()
        times=pd.date_range(start=now,periods=points,freq="16N")
        datasets=pd.DataFrame(data=data,index=times)
        datasets.to_csv(f,sep='\t',line_terminator = '\r')
        np.savetxt(f, datasets, delimiter=" ", newline="\n")
         
        elapsed = time.time()
        print("--- %s seconds ---" % (elapsed - start_time))
        exectime.append((elapsed - start_time)*1000)
      
except KeyboardInterrupt:
    print(np.mean(exectime))
    f.close()
    inst.clear()
    print('Hello user you have pressed ctrl-c button.')
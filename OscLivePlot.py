# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 13:40:52 2021

@author: Yakub and Sandra
Helps us to find out the number of points by manipulating oscil controls
For not triggered oscilloscope
"""
import pyvisa
import numpy as np
import matplotlib.pyplot as plt
import time

rm = pyvisa.ResourceManager()
rm.list_resources()

inst = rm.open_resource('USB0::0x2A8D::0x0397::CN60144301::0::INSTR')
# inst = rm.open_resource('TCPIP0::169.254.30.139::inst0::INSTR')

print(inst.query("*IDN?"))

inst.write(':WAVeform:UNSigned 1')
inst.write(':WAVeform:BYTeorder LSBFirst')
inst.write(':WAVeform:FORMat WORD ')
inst.write(':ACQuire:COMPlete 100')
inst.write(':WAVeform:SOURce MATH')
inst.write(':WAVeform:POINts:MODE MAXimum')
# inst.write(':WAVeform:POINTS 50000')
# inst.write(':CHANnel1:DISPlay 0')
print(inst.query(':WAVeform:POINts?'))
print(inst.query(':WAVeform:POINts:MODE?'))
print(inst.query(':WAVeform:PREamble?'))

values = inst.query_binary_values(':WAVeform:DATA?', datatype='H', is_big_endian=False)
data = np.asarray(values)
plt.plot(data)
  
# to run GUI event loop
plt.ion()

x = np.linspace(0, 1, len(data))
  
# here we are creating sub plots
figure, ax = plt.subplots(figsize=(10, 8))
line1, = ax.plot(x, data)
  
# setting title
plt.title("Voltage [osc units]", fontsize=20)
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
exectime=list()

# f=open('test.txt', 'w')
  
# Loop
try:
    while True:
    # for _ in range(50):
        start_time = time.time()
        print(inst.query(':WAVeform:POINts?'))
        
        # inst.write(':DIGitize Channel1')
        values = inst.query_binary_values(':WAVeform:DATA?', datatype='H', is_big_endian=False)
        data = np.asarray(values)
        plt.plot(data)
        # np.savetxt(f, values, delimiter=" ")

        x = np.linspace(0, 1, len(data))
      
        # updating data values
        line1.set_xdata(x)
        line1.set_ydata(data)
      
        # drawing updated values
        figure.canvas.draw()
      
        # This will run the GUI event
        # loop until all UI events
        # currently waiting have been processed
        figure.canvas.flush_events()
        
        elapsed = time.time()
        print("--- %s seconds ---" % (elapsed - start_time))
        exectime.append((elapsed - start_time)*1000)
        
    plt.ioff()
    plt.show()
      
except KeyboardInterrupt:
    print('Hello user you have pressed ctrl-c button.')
    inst.clear()
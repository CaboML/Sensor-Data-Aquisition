#Libraries import

import serial # import Serial Library

import numpy # Import numpy

import matplotlib.pyplot as plt #import matplotlib library

from drawnow import *



# Variables setup
sec = []
Vib_x = []
Vib_y = []
Vib_z = []

cnt = 0

file = open('Vibration Measurements.txt','w')

Arduino_Data = serial.Serial('/dev/cu.usbmodem14141', 19200)
Arduino_Data.flushInput()

Arduino_Data.write(bytes(1)) #begin arduino communication

plt.ion() # turn matplotlib interactive

#step3:create a function for plot:-

def makeFig(): #Create a function that makes our desired plot
    plt.ylim((-500, 500)) #Set y min and max values

    plt.title('My Live Streaming Sensor Data') #Plot the title

    plt.grid(True) #Turn the grid on

    plt.ylabel('Vib_x') #Set ylabels

    plt.plot(sec, Vib_x, 'ro-', label='X acceleration') #plot the temperature
    # plt.plot(Vib_y)
    # plt.plot(Vib_z)

    plt.legend(loc='upper left') #plot the legend

try:
    while True: # While loop that loops forever
        while (Arduino_Data.inWaiting()==0): # Wait here until there is data
            print('Estou à espera de dados')
            pass #do nothing

        file2.readline()

        dataArray = file2.split(',')  # Split it into an array called dataArray

        sec.append(float(int(dataArray[0])))
        Vib_x.append(float(int(dataArray[1])))  # Convert first element to floating number and put in temp
        #         # Vib_y.append(float(int(dataArray[2])))
        #         # Vib_z.append(float(int(dataArray[3])))
        #         #Vib_y.append(float(int(dataArray[1]))) #Convert second element to floating number and put in P tempF.append(temp) #Build our tempF array by appending temp readings pressure.append(P) #Building our pressure array by appending P readings drawnow(makeFig) #Call drawnow to update our live graph
        #
        drawnow(makeFig)  # Call drawnow to update our live graph

            plt.pause(.0000000000001) #Pause Briefly. Important to keep drawnow from crashing

            cnt = cnt+1
            print(sec)
            print(Vib_y)

            if(cnt > 1000): #If you have 50 or more points, delete the first one from the array tempF.pop(0) #This allows us to just see the last 50 data points
                sec.pop(0)
                Vib_x.pop(0)
                Vib_y.pop(0)
                Vib_z.pop(0)

except KeyboardInterrupt:
    Arduino_Data.close()
file.close()
file2 = open('Vibration Measurements.txt','r')


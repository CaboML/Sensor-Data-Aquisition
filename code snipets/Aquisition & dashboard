#Library import

import serial #Serial communication
import numpy
import pandas
import matplotlib.pyplot as plt

#Data aquisition
file = open('Vibration Measurements.txt','w')
file = open('Vibration Measurements.txt','w')

Arduino_Data = serial.Serial('/dev/cu.usbmodem14141', 19200)
Arduino_Data.flushInput()

Arduino_Data.write(bytes(1)) #begin arduino communication

try:
    cnt = 0
    while True: # While loop that loops forever
        while (Arduino_Data.inWaiting() == 0): # Wait here until there is data
            #print('Estou à espera de dados')
            pass #do nothing

        arduinoString = Arduino_Data.read() #read the line of text from the serial port
        #print(arduinoString)
        arduinoString = arduinoString.decode()
        #print(arduinoString)
        file.write(arduinoString)
        print('a escrever dados no ficheiro', cnt)
        cnt += 1

except KeyboardInterrupt:
    Arduino_Data.close()
    file.close()

#Data display
def data_show():
    file2 = open('Vibration Measurements.txt', 'r')
    sec = []
    Vib_x = []
    for line in file2:
        print(line)
        dataArray = line.split(',')
        sec.append(float(int(dataArray[0]))) #Record the mesurement time
        Vib_x.append(float(int(dataArray[1])))  # Convert to integer then to float. append to Vib_x list

    plt.plot(sec, Vib_x, 'ro')

thread.start_new_thread ( data_show() )

#Library import


def DataAquisition(AquisitionTime, file):
    import serial #Serial communication
    import numpy as np
    import pandas
    import matplotlib.pyplot as plt
    import time

    #Data aquisition

    file = open(file, 'w+')

    Arduino_Data = serial.Serial('/dev/cu.usbmodem14341', 115200)

    Arduino_Data.flushInput()

    Arduino_Data.write(bytes(1))  # begin arduino communication

    start = time.time()
    end_time = 0

    try:
        cnt = 0
        time_cnt = end_time - start

        while time_cnt < AquisitionTime:  # While loop that loops forever
            while (Arduino_Data.inWaiting() == 0):  # Wait here until there is data
                #print('Estou à espera de dados')
                pass #do nothing

            arduinoString = Arduino_Data.read() #read the line of text from the serial port
            #print(arduinoString)
            arduinoString = arduinoString.decode()
            #print(arduinoString)

            file.write(arduinoString)
            #print('a escrever dados no ficheiro', cnt)

            cnt += 1
            end_time = time.time()
            time_cnt = end_time - start

            print(time_cnt)


    except KeyboardInterrupt:
        Arduino_Data.close()
        file.close()

    return file

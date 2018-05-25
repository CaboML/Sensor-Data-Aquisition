#Importing Libraries
#A melhorar colocar a opção de escolher o modo de utilização recolha ou mostrar dados
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from ADXL345Dataaquisition import DataAquisition

class DisplayData:

    def __init__(self,x):
        self.file_name = x  # Class variable. File with the data


    def DataPreparation(self):
        self.sec = []  # List with time values
        self.Vib = []  # List with acceleration Data
        self.freq = None  # Variabel freq for aquisition frequency
        self.fraction_time = None
        self.total_acquisition = None

        #file2 = pd.read_csv('car_engine.csv')
        try:
            file2 = pd.read_csv(self.file_name)
        except:
            print('Wrong file name, please check available files')

        file2 = file2[:-1]  # Last Line Removed


        # Set Data Columns
        self.sec = file2.iloc[:, 0]  # set time column
        self.Vib = file2.iloc[:, 1]  # set Acceleration column

        sec_max = np.max(self.sec)  # Define maximum sampling time
        sec_min = np.min(self.sec)  # Define minimum sampling time
        total_time = sec_max - sec_min  # Overall sampling time

        self.total_acquisition = np.size(self.Vib)  # number of samples

        self.fraction_time = total_time / self.total_acquisition  # Sampling period

        self.freq = (1 / self.fraction_time) * 1000
        print(self.freq, 'Hz')  # Sampling freq

        return self.total_acquisition, self.sec, self.Vib, self.freq

    def AccelerationData(self):  #Method to display data retrieved from Arduino

        fig = plt.figure(1)
        fig.suptitle('Acceleration DashBoard' + ' ' + self.file_name, fontsize=14, fontweight='bold')

        Vx = fig.add_subplot(1, 1, 1)

        plt.grid(True)  # Turn the grid on

        plt.ylabel('Vib_z')  # Set ylabels
        Vx.plot(self.sec, self.Vib, color='b' )
        Vx.set_title('Z Acceleration')
        Vx.set_xlabel('Time [ms]')
        Vx.set_ylabel('acceleration [mg]')

        plt.show()
        return

    def fft(self, t_init, t_end):  # Create fft using a start and end time
        self.t_init = t_init
        self.t_end = t_end

        vec_init = int(round(self.freq * self.t_init, 1))
        vec_end = int(round(self.freq * self.t_end, 1))

        self.Vib = self.Vib[vec_init: vec_end]

        fft_vx = np.fft.fft(self.Vib)

        fft_freq = np.fft.fftfreq(np.size(self.Vib), d=(1 / self.freq))

        # print(freq)
        fig = plt.figure()
        fig.suptitle('FFT DashBoard', fontsize=14, fontweight='bold')

        Vx_fft = fig.add_subplot(1, 1, 1)
        #Vx_fft.set_xlim([0, 500])
        #Vx_fft.set_xscale('Linear')
        Vx_fft.set_ylim(auto=True)
        #Vx_fft.plot(fft_freq, 2.0/np.size(self.Vib) * np.abs(fft_vx.real))
        xf = np.linspace(0.0, 1.0 / (2.0 * (1/self.freq)), np.size(self.Vib)/2)
        yf = np.fft.fft(self.Vib)
        Vx_fft.plot(xf, (2.0/np.size(self.Vib)) * np.abs(yf[0:np.int(np.size(self.Vib)/2)]))
        plt.show()
        return

    def PSD(self):
        fig = plt.figure(1)
        fig.suptitle('PSD DashBoard', fontsize=14, fontweight='bold')
        V_PSD = fig.add_subplot(1, 1, 1)

        V_PSD.psd(self.Vib, NFFT=int(np.size(self.Vib)/100), Fs=self.freq)
        plt.show()
        return


try:

#Use mode collect and Display data or just to display data
    useMode = input("Please, insert 1 for Data display only and 2 for data acquisition and Data Dispaly: ")
    useMode = int(useMode)

    while useMode != 1 and useMode != 2:
        print("Please Try again and insert a value between 1 and 2")
        useMode = input("Please, insert 1 for Data display only and 2 for data acquisition and Data Dispaly: ")
        useMode = int(useMode)
        print(useMode)

    #Use modes configurations
    if useMode == 1:

        file = input('Please insert the data file name') + '.txt'
        print(file)
        data = DisplayData(file)
        data.DataPreparation()
        data.AccelerationData()

        print('Introduza o tempo opara a fft')
        ti = input('Insert FFT start time [s]:')  # manually insert the fft start time for analysis
        to = input('Insert FFT end time [s]:')  # manually insert the fft end time for analysis
        data.fft(float(ti), float(to))
        data.PSD()

    else:
        Time = input("Insert the measurement time [s]")
        Time = int(Time)
        file = input('Please insert the data file name') + '.txt'
        print(file)
        DataAquisition(Time, file)

        data = DisplayData(file)
        data.DataPreparation()
        data.AccelerationData()

        print('Introduza o tempo opara a fft')
        ti = input('Insert FFT start time [s]:')  # manually insert the fft start time for analysis
        to = input('Insert FFT end time [s]:')  # manually insert the fft end time for analysis
        data.fft(float(ti), float(to))
        data.PSD()



except KeyboardInterrupt:
    plt.close('all')

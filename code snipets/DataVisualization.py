#Importing Libraries

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from ArduinoSerialAquisition import DataAquisition  # File that triggers arduino data collection
from PeakDetection import PeakDetection             # Peak detection class
from scipy import signal

class DisplayData:
"""
All parameters are userInput

Prepares acelerometer data to be displayed

Calculates FFt and PSD from signal.

Opens data from txt file using comma separated values
"""
    def DataPreparation(self, file_name):
        """

        :param self:
        :param file_name: Data file from UserImput
        :return: Aquisition sample time, columns o time as sec, column of vibration time, acquisiton freqtime

        """
        sec = []  # List with time values
        Vib = []  # List with acceleration Data

        #open txt file
        try:
            print(file_name)
            file2 = pd.read_csv(file_name + '.txt')
        except:
            print('Wrong file name, please check available files')

        file2 = file2[:-1]  # Last Line Removed

        # Set Data Columns
        sec = file2.iloc[:, 0]  # set time column
        Vib = file2.iloc[:, 1]  # set Acceleration column


        sec_max = np.max(sec)  # Define maximum sampling time
        sec_min = np.min(sec)  # Define minimum sampling time
        total_time = sec_max - sec_min  # Overall sampling time

        total_acquisition = np.size(Vib)  # number of samples

        fraction_time = total_time / total_acquisition  # Sampling period

        freq = (1 / fraction_time) * 1000
        print(freq, 'Hz')  # Sampling freq

        return total_acquisition, sec, Vib, freq

    def AccelerationData(self, other):  #Method to display data retrieved from Arduino
        """
        :param self:
        :param other: Data to show
        :return: A plot
        """

        fig = plt.figure(1)
        fig.suptitle('Acceleration DashBoard', fontsize=14, fontweight='bold')

        Vx = fig.add_subplot(1, 1, 1)

        plt.grid(True)  # Turn the grid on

        plt.ylabel('mg')  # Set ylabels

        #Parameters calculation for all graphs
        for i in other:
            print(i)
            total_aquisition, sec, vib, freq = self.DataPreparation(i)
            Vx.plot(sec, vib)

        Vx.legend(other)


        Vx.set_title('Z Acceleration')
        Vx.set_xlabel('Time [ms]')
        Vx.set_ylabel('acceleration [mg]')

        plt.show()

        return

    #method to retrive the fft results
    def fft_prep(self, t_init, t_end, file_name):
        """

        :param self:
        :param t_init: initial window time
        :param t_end:  end window time
        :param file_name: Base file to calculate fft
        :return:
            xf: frequency values from FFT
            real_yf: FFT values
        """
        total_aquisition, sec, vib, freq = self.DataPreparation(file_name)

        vec_init = int(round(freq * t_init, 1))
        vec_end = int(round(freq * t_end, 1))

        vib = vib[vec_init: vec_end]

        xf = np.linspace(0.0, 1.0 / (2.0 * (1/freq)), np.size(vib)/2)
        yf = np.fft.fft(vib)
        real_yf = (2.0/np.size(vib)) * np.abs(yf[0:np.int(np.size(vib)/2)])

        return xf, real_yf

    # method to display fft
    def fft(self, other):  # Create fft using a start and end time
        """
        :param self:
        :param other: Files to compute FFT. Files selected by userInput
        :return: FFT plot
        """

        # print(freq)
        fig = plt.figure()
        fig.suptitle('FFT DashBoard', fontsize=14, fontweight='bold')

        Vx_fft = fig.add_subplot(1, 1, 1)
        Vx_fft.set_ylim(auto=True)

        print('Introduza o tempo opara a fft')
        ti = input('Insert FFT start time [s]:')  # manually insert the fft start time for analysis
        to = input('Insert FFT end time [s]:')  # manually insert the fft end time for analysis

        for i in other:
            print(i)
            xf, real_yf = self.fft_prep(int(ti), int(to), i)
            Vx_fft.plot(xf, real_yf)

        Vx_fft.legend(other)
        plt.show()

        return

    def PSD_prep(self, t_init, t_end, file_name):
        """

        :param self:
        :param t_init: initial window time
        :param t_end:  end window time
        :param file_name: File to comput PSD values
        :return:
            f: frequency values
            Pxx_den: PSD values
        """

        total_aquisition, sec, vib, freq = self.DataPreparation(file_name)

        vec_init = int(round(freq * t_init, 1))
        vec_end = int(round(freq * t_end, 1))

        vib = vib[vec_init: vec_end]

        f, Pxx_den = signal.welch(vib, freq, nperseg=int(np.size(vib)/5))

        Peaks = PeakDetection(f, Pxx_den)
        Max_x, Max_y = Peaks.PeakDetection_prep()

        return f, Pxx_den



    def PSD(self, other):

        fig = plt.figure(1)
        fig.suptitle('PSD DashBoard', fontsize=14, fontweight='bold')
        V_PSD = fig.add_subplot(1, 1, 1)

        print('Introduza o tempo para a PSD')
        ti = input('Insert PSD start time [s]:')  # manually insert the fft start time for analysis
        to = input('Insert PSD end time [s]:')  # manually insert the fft end time for analysis

        for i in other:
            print(i)
            f, Pxx = self.PSD_prep(int(ti), int(to), i)
            V_PSD.semilogy(f, Pxx)

            i = PeakDetection(f, Pxx)
            Max_x, Max_y = i.PeakDetection_prep()

        V_PSD.legend(other)

        plt.show()

        return

def main():
    try:
        # Use mode collect and Display data or just to display data
        useMode = input("Please, insert 1 for Data display only and 2 for data acquisition and Data Dispaly: ")
        useMode = int(useMode)

        while useMode != 1 and useMode != 2:
            print("Please Try again and insert a value between 1 and 2")
            useMode = input("Please, insert 1 for Data display only and 2 for data acquisition and Data Dispaly: ")
            useMode = int(useMode)
            print(useMode)

        # Use modes configurations
        if useMode == 1:

            #file = input('Please insert the data file name')

            data = DisplayData()

            #Loop object creation
            extra_graph = 0
            class_names = []  # List to store class instances names
            file_names = []
            while extra_graph != 'end':
                extra_graph = input('Please insert the graph name without the .txt or press end')
                if extra_graph == 'end':
                    break
                else:
                    file_names.append(extra_graph)

            print(file_names)

            data.AccelerationData(file_names)

            graph_type = input('press ALL or PSD, or fft')

            if graph_type == 'ALL' or graph_type == 'fft':
                data.fft(file_names)

            if graph_type == 'ALL':
                data.PSD(file_names)

            if graph_type == 'PSD':
                data.PSD(file_names)

        else:
            Time = input("Insert the measurement time [s]")
            Time = int(Time)
            file = input('Please insert the data file name') + '.txt'
            print(file)
            DataAquisition(Time, file)

    except KeyboardInterrupt:
        plt.close('all')


if __name__ == '__main__':
    main()
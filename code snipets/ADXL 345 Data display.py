import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#Data display
def data_show():
    #file2 = pd.read_csv('car_engine.csv')
    file2 = pd.read_csv('Vibration Measurements_2.txt')

    file2 = file2[:-1] #Last Line Removed
    #print(file2)

# Set Data Columns
    sec = file2.iloc[:, 0]
    Vib_x = file2.iloc[:, 1]
    # Vib_y = file2.iloc[:, 2]
    # Vib_z = file2.iloc[:, 3]

    #Calculating milisenconds time

    sec_max = np.max(sec)
    sec_min = np.min(sec)
    total_time = sec_max - sec_min
    total_acquisition = np.size(Vib_x)
    fraction_time = total_time / total_acquisition
    print((1/fraction_time)*1000, 'Hz')
    # i = 0
    # sec2 = []
    # cnt = 0
    #
    # #Creating the new aquisiton time in seconds
    # while i <= total_acquisition:
    #     i = i + 1
    #     cnt = cnt + fraction_time
    #     sec2.append(cnt)


    #sec2.pop(total_acquisition)

    fig = plt.figure(1)
    fig.suptitle('Acceleration DashBoard', fontsize=14, fontweight='bold')

    Vx = fig.add_subplot(3,1,1)
    # Vy = fig.add_subplot(2, 4, 2)
    # Vz = fig.add_subplot(2, 4, 3)
    # V_all = fig.add_subplot(2,4,4)

    Vx_fft = fig.add_subplot(3, 1, 2)
    #Vx_fft.set_xlim([0, 500])
    #Vx_fft.set_ylim([0, 60000])
    # Vy_fft = fig.add_subplot(2, 4, 6)
    # Vz_fft = fig.add_subplot(2, 4, 7)
    # V_all_fft = fig.add_subplot(2, 4, 8)

    Vx_PSD = fig.add_subplot(3,1,3)



    plt.grid(True)  # Turn the grid on

    plt.ylabel('Vib_x')  # Set ylabels
    Vx.plot(sec, Vib_x, color = 'b', )
    Vx.set_title('X Acceleration')
    Vx.set_xlabel('Time [s]')
    Vx.set_ylabel('acceleration [mg]')

    # Vy.plot(sec2, Vib_y,color = 'g')
    # Vy.set_title('Y Acceleration')
    # Vy.set_xlabel('Time [s]')
    # Vy.set_ylabel('acceleration [mg]')
    #
    # Vz.plot(sec2, Vib_z, color = 'c')
    # Vz.set_title('Z Acceleration')
    # Vz.set_xlabel('Time [s]')
    # Vz.set_ylabel('acceleration [mg]')
    #
    # V_all.plot(sec, np.sqrt(Vib_x**2 + Vib_y**2 + Vib_z**2 ), color = 'r')
    # V_all.set_title('Norm Acceleration')
    # V_all.set_xlabel('Time [s]')
    # V_all.set_ylabel('acceleration [mg]')

    #FFT


    fft_vx = np.fft.fft(Vib_x)
    # fft_vy = np.fft.fft(Vib_y, n= total_acquisition)
    # fft_vz = np.fft.fft(Vib_z, n= total_acquisition)
    # fft_vall = np.fft.fft(np.sqrt(Vib_x**2 + Vib_y**2 + Vib_z**2), n= total_acquisition)


    freq = np.fft.fftfreq(total_acquisition, d= fraction_time)
    #print(freq)
    Vx_fft.plot(freq, fft_vx.real)
    # Vy_fft.plot(freq, fft_vy.real)
    # Vz_fft.plot(freq, fft_vz.real)
    # V_all_fft.plot(freq, fft_vall.real)

    ###### PSD
    psd_Vx = Vx_PSD.psd(Vib_x, NFFT=total_acquisition, Fs=1/fraction_time)


    plt.show()

data_show()
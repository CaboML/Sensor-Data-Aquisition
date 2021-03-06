import numpy as np
import matplotlib.pyplot as plt

class PeakDetection:

    def __init__(self, xValues, yValues):
        self.yValues = yValues
        self.xValues = xValues

    def Display_Vib(self):
        fig = plt.figure()
        fig.suptitle("Graph title", fontsize=14, fontweight='bold')
        Graph2 = fig.add_subplot(1, 1, 1)
        Graph2.plot(self.xValues, self.yValues)

        plt.show()

    def PeakDetection_prep(self):

        # Calculate all relative max

        Max_yValues = []
        Max_xValues = []
        Analysis_yValues = []  # Vector do store 3 values to be analized
        Final_yValues = []  # Vector with the maximum using x threshold
        Final_xValues = []  # Vector with the times of the final results

        j = 0
        while j < np.size(self.yValues) - 2:
            for i in range(3):
                Analysis_yValues.append(self.yValues[j + i])


            #Groups of 3 values. Comparison between the meeddle value and the side values
            if Analysis_yValues[0] <= Analysis_yValues[1] >= Analysis_yValues[2]:
                Max_yValues.append(Analysis_yValues[1])
                Max_xValues.append(self.xValues[j+1])

            Analysis_yValues = []
            j = j + 1

        #x Axis threshold condition
        k = 1
        Final_xValues.append(Max_xValues[0])
        Final_yValues.append(Max_yValues[0])
        while k < np.size(Max_xValues):

            Final_xValues.append(Max_xValues[k])
            Final_yValues.append(Max_yValues[k])

            k += 1
        return Final_xValues, Final_yValues

    ### THRESHOLD CODE ####
    # yThr = int(input('Please insert the desired yThreshold: '))
    #     xThr = int(input('Please insert the desired xThreshold: '))


# if Analysis_yValues[0] <= Analysis_yValues[1] >= Analysis_yValues[2]:
#     if Analysis_yValues[1] > yThr:
#         Max_yValues.append(Analysis_yValues[1])
#         Max_xValues.append(self.xValues[j + 1])
#         # x Axis threshold condition
#         k = 1
#         Final_xValues.append(Max_xValues[0])
#         Final_yValues.append(Max_yValues[0])
#         while k < np.size(Max_xValues):
#
#             if (Max_xValues[k] - Final_xValues[-1]) > xThr:
#                 Final_xValues.append(Max_xValues[k])
#                 Final_yValues.append(Max_yValues[k])
#
#             k += 1
#
    def Peak_stats(self):
        Final_xValues, Final_yValues = self.PeakDetection_prep()
        Peaks_mean = np.mean(Final_yValues)
        for i in range(np.size(Final_xValues) - 1):
            Avg_peak_time = np.mean(Final_xValues[i+1]-Final_xValues[i])
        print(Peaks_mean)
        print(Avg_peak_time)

        return Peaks_mean, Avg_peak_time


    def PeakDetection_Disp(self):
        Final_xValues, Final_yValues = self.PeakDetection_prep()

        fig = plt.figure()
        fig.suptitle("Graph title", fontsize=14, fontweight='bold')
        Graph = fig.add_subplot(1, 1, 1)
        Graph.plot(self.xValues,self.yValues)
        Graph.scatter(Final_xValues, Final_yValues, marker="v", color="b")

        for i in range(np.size(Final_yValues)):
            Values = '[' + str(round(Final_xValues[i])) + ',' + str(round(Final_yValues[i])) + ']'
            Graph.annotate(Values, xy=(Final_xValues[i], Final_yValues[i]))

        Graph.scatter(Final_xValues, Final_yValues, marker="v", color="b")

        plt.show()


data = [25.23, 8.23, 15.567678, 5.234, 6, 10, 10, 3, 1, 20, 7]
sec =  [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22]

def main():
    teste = PeakDetection(sec, data)

    teste.Display_Vib()
    teste.PeakDetection_Disp()
    teste.Peak_stats()

if __name__ == '__main__':
    main()


import numpy as np
import matplotlib.pyplot as plt
import scipy.signal

"""     
Scipy uses z**(-n) coefficients to generate both numerator and denominator: 
[a,b,c,d,...] = a*z**(0) + b*z**(-1) + c*z**(-2) + d*z**(-3) ...
"""
class Filter:
    def __init__(self,name,NumeratorZcoefs,DenominatorZcoefs,
                 fs=1,comments="") -> None:
        self.name = name
        self.NumeratorZcoefs = NumeratorZcoefs
        self.DenominatorZcoefs = DenominatorZcoefs
        self.fs = fs
        self.comments = comments

        self.FreqResponse = scipy.signal.freqz(self.NumeratorZcoefs, 
                                               self.DenominatorZcoefs)
        self.frequency = self.FreqResponse[0]*self.fs/(2*np.pi)
        self.period = self.frequency**(-1)
        self.dbpowergain = 20*np.log10(np.abs(np.array(self.FreqResponse[1])))
        self.phase = np.angle(np.array(self.FreqResponse[1]))
    
    def __plotFig(self, x, y, xlabel, ylabel, title, plottype = "plot", 
                  xticks=None) -> None:
        plt.figure(figsize = [8,6])
        plt.title(f"{self.name} {title}")
        plt.grid()
        
        if plottype == "semilog":
            plt.semilogx(x, y)
        else:
            plt.plot(x, y)
        
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        
        if xticks:
            plt.xticks(xticks,tuple(map(lambda num: str(num),xticks)))
        
    def plotNormFreqResponse(self) -> None:
        ### rad/bar (Frequency) ###
        self.__plotFig(x = self.FreqResponse[0]/np.pi, y = self.dbpowergain, 
                       xlabel = 'Normalized frequency', ylabel = 'Gain (dB)',
                       title = 'Normalized Frequency Response')
    
    def plotFreqResponse(self) -> None:
        ### cycles/bar (Frequency), Log plot ###
        self.__plotFig(x = self.frequency, y = self.dbpowergain, 
                       xlabel = 'Frequency (cycles/bar)', 
                       ylabel = 'Gain (dB)', 
                       title = 'Frequency Response' , plottype = "semilog")
        
    def plotPeriodResponse(self) -> None:
        ### bars/cycle (Period), Log plot ###
        self.__plotFig(x = self.period, y = self.dbpowergain, 
                       xlabel = 'Period (bars/cycle)', ylabel = 'Gain (dB)', 
                       title = 'Period Response', plottype = "semilog", 
                       xticks = [10,20,30,40,50])
    
    def plotPhaseResponse(self) -> None:
        ### Phase response ###
        self.__plotFig(x = self.FreqResponse[0]/np.pi, y = self.phase,
                       xlabel = 'Normalized frequency',
                       ylabel = 'Angle (radians)',
                       title = 'Phase Response')
        
    def plotGroupDelay(self) -> None:
        ### Group delay ###
        w, gd = scipy.signal.group_delay((self.NumeratorZcoefs, self.DenominatorZcoefs))
        self.__plotFig(x = w/np.pi, y = gd,
                       xlabel = 'Normalized frequency',
                       ylabel = 'Group delay (samples)',
                       title = 'Group delay')
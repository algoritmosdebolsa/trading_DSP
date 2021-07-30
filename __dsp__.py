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

        self.w, self.complex = scipy.signal.freqz(self.NumeratorZcoefs, 
                                               self.DenominatorZcoefs)
        
        self.w, self.complex = self.w[1:], self.complex[1:]
        self.frequency = self.w * self.fs / (2*np.pi)
        self.period = self.frequency**(-1)
        self.dbpowergain = 20*np.log10(np.abs(self.complex))
        self.phase = np.angle(self.complex)
    
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
        self.__plotFig(x = self.frequency, y = self.dbpowergain, 
                       xlabel = 'Frequency (cycles/sample)', ylabel = 'Gain (dB)',
                       title = 'Normalized Frequency Response')
    
    def plotFreqResponse(self) -> None:
        ### cycles/bar (Frequency), Log plot ###
        self.__plotFig(x = self.frequency, y = self.dbpowergain, 
                       xlabel = 'Frequency (cycles/sample)', 
                       ylabel = 'Gain (dB)', 
                       title = 'Frequency Response' , plottype = "semilog")
    
    def plotPeriodResponse(self) -> None:
        ### bars/cycle (Period), Log plot ###
        self.__plotFig(x = self.period, y = self.dbpowergain, 
                       xlabel = 'Period (samples/cycle)', ylabel = 'Gain (dB)', 
                       title = 'Period Response', plottype = "semilog", 
                       xticks = [10,20,30,40,50])
    
    def plotPhaseResponse(self) -> None:
        ### Phase response ###
        self.__plotFig(x = self.frequency, y = self.phase,
                       xlabel = 'Frequency (cycles/sample)',
                       ylabel = 'Angle (radians)',
                       title = 'Phase Response')
        
    def plotGroupDelay(self) -> None:
        ### Group delay ###
        _w, gd = scipy.signal.group_delay((self.NumeratorZcoefs, self.DenominatorZcoefs))
        self.__plotFig(x = self.frequency, y = gd[1:],
                       xlabel = 'Frequency (cycles/sample)',
                       ylabel = 'Group delay (samples)',
                       title = 'Group delay')
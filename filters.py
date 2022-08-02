import numpy as np
import matplotlib.pyplot as plt
import scipy.signal
from dataclasses import dataclass, field
from nptyping import NDArray, Shape, Float, Complex

@dataclass
class Filter:
    name: str
    NumeratorZcoefs: list[float]
    DenominatorZcoefs: list[float]
    fs: int = 1
    comments: str = field(default_factory=str)
    
    complex_amplitude: NDArray[Shape["512"], Complex] = field(init=False, repr=False)
    w: NDArray[Shape["512"], Float] = field(init=False, repr=False)
    gd: NDArray[Shape["512"], Float] = field(init=False, repr=False)
    frequency: NDArray[Shape["512"], Float] = field(init=False, repr=False)
    period: NDArray[Shape["512"], Float] = field(init=False, repr=False)
    dbpowergain: NDArray[Shape["512"], Float] = field(init=False, repr=False)
    phase: NDArray[Shape["512"], Float] = field(init=False, repr=False)
    
    def __post_init__(self) -> None:
        self.w, self.complex_amplitude = scipy.signal.freqz(self.NumeratorZcoefs, self.DenominatorZcoefs)
        _, self.gd = scipy.signal.group_delay((self.NumeratorZcoefs, self.DenominatorZcoefs))
        self.dbpowergain = 20*np.log10(np.abs(self.complex_amplitude))
        self.phase = np.unwrap(np.angle(self.complex_amplitude))
        self.frequency = self.w * self.fs / (2*np.pi)
        with np.errstate(divide='ignore'):
            self.period = self.frequency**(-1)
    
    def __plotFig(self, x: NDArray[Shape["512"], Float], y: NDArray[Shape["512"], Float], 
                  xlabel: str, ylabel: str, title: str, plot_type: str = "plot", 
                  xticks: list = [], yticks: list = []) -> None:
        plt.figure(figsize = [8,6])
        plt.title(f"{self.name} {title}")
        plt.grid()
        
        if plot_type == "semilog":
            plt.semilogx(x, y)
        else:
            plt.plot(x, y)
        
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        
        if xticks != []:
            plt.xticks(xticks,tuple(map(lambda num: str(num),xticks)))
        
        if yticks != []:
            plt.yticks(yticks,tuple(map(lambda num: str(num),yticks)))
        
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
                       title = 'Frequency Response' , plot_type = "semilog")
    
    def plotPeriodResponse(self) -> None:
        ### bars/cycle (Period), Log plot ###
        self.__plotFig(x = self.period, y = self.dbpowergain, 
                       xlabel = 'Period (samples/cycle)', ylabel = 'Gain (dB)', 
                       title = 'Period Response', plot_type = "semilog", 
                       xticks = [10,20,30,40,50],
                       yticks = [-40,-20,-10,-3,0])
    
    def plotPhaseResponse(self) -> None:
        ### Phase response ###
        self.__plotFig(x = self.frequency, y = self.phase,
                       xlabel = 'Frequency (cycles/sample)',
                       ylabel = 'Angle (radians)',
                       title = 'Phase Response')
        
    def plotGroupDelay(self) -> None:
        ### Group delay ###
        self.__plotFig(x = self.frequency, y = self.gd,
                       xlabel = 'Frequency (cycles/sample)',
                       ylabel = 'Group delay (samples)',
                       title = 'Group delay')

"""
Scipy uses z**(-n) coefficients to generate both numerator and denominator:
[a,b,c,d,...] = a*z**(0) + b*z**(-1) + c*z**(-2) + d*z**(-3) ...
"""

def TwoBarEMA(alpha: float = 0.8) -> Filter:   
    filt = Filter(name = "2-bar window EMA", 
                  NumeratorZcoefs = [alpha], 
                  DenominatorZcoefs = [1, -(1-alpha)], 
                  comments = "1 pole, no zeros")    
    return filt

def TenBarSMA() -> Filter:
    filt = Filter(name = "10-bar window SMA", 
                  NumeratorZcoefs = [1,1,1,1,1,1,1,1,1,1], 
                  DenominatorZcoefs = [10], 
                  comments = "no poles, 1 zero")
    return filt

def SimpleHighPassFIR() -> Filter:
    filt = Filter(name = "Very simple High-Pass FIR filter", 
                  NumeratorZcoefs = [1,-1],
                  DenominatorZcoefs = [2])
    return filt

def SimpleLowPassFIR() -> Filter:
    filt = Filter(name = "Very simple Low-Pass FIR filter", 
                  NumeratorZcoefs = [1,1], 
                  DenominatorZcoefs = [2])
    return filt


def LowPassSecondOrderFIR() -> Filter:
    filt = Filter(name = "2nd order Low-Pass FIR filter", 
                  NumeratorZcoefs = [1,2,1],
                  DenominatorZcoefs = [4],
                  comments = "")
    return filt

def EhlersBandPass(center_period: int = 20) -> Filter:
    pi = np.pi
    beta = np.cos(2*pi/center_period)
    gamma = 1/np.cos(2*pi/center_period)
    alpha = gamma - np.sqrt(gamma**2 - 1)
    
    filt = Filter(name = "Ehlers Band-Pass filter", 
                  NumeratorZcoefs = [0.5*(1-alpha),0,-0.5*(1-alpha)], 
                  DenominatorZcoefs = [1,-beta*(1+alpha),alpha], 
                  comments = "Pass Band is 30 percent of the center period")     
    return filt

def EhlersHighPass(pc: int = 48, fs: int = 1) -> Filter:
    pi = np.pi
    period = fs*pc
    alpha1 = (np.cos(2*pi/period) + np.sin(2*pi/period) - 1) / np.cos(2*pi/period)
    
    c2 = 2*(1-alpha1)
    c3 = -(1-alpha1)**2
    c1 = (1-alpha1/2)**2
    
    filt = Filter(name = "Ehlers High-pass filter", 
                  NumeratorZcoefs = [1*c1,-2*c1,1*c1], 
                  DenominatorZcoefs = [1,-c2,-c3], 
                  fs = fs,
                  comments = "Second Order IIR")
    return filt

def EhlersButterworth(pc: int = 10, fs: int = 1) -> Filter:
    pi = np.pi
    period = fs*pc
    a1 = np.exp(-np.sqrt(2)*pi/period)
    b1 = 2*a1*np.cos(np.sqrt(2)*pi/period)
    c2 = b1
    c3 = -a1*a1
    c1 = 1 - c2 - c3
        
    filt = Filter(name = "Ehlers 2nd order Butterworth filter", 
                  NumeratorZcoefs = [c1], 
                  DenominatorZcoefs = [1,-c2,-c3],
                  fs = fs,
                  comments = "")   
    return filt

def Supersmoother(pc: int = 10, fs: int = 1) -> Filter:
    pi = np.pi
    period = fs*pc
    a1 = np.exp(-np.sqrt(2)*pi/period)
    b1 = 2*a1*np.cos(np.sqrt(2)*pi/period)
    c2 = b1
    c3 = -a1*a1
    c1 = 1 - c2 - c3
        
    filt = Filter(name = "Supersmoother", 
                  NumeratorZcoefs = [c1,c1], 
                  DenominatorZcoefs = [2,-2*c2,-2*c3], 
                  fs = fs,
                  comments = "")
    return filt

# More filters will be added in the future!
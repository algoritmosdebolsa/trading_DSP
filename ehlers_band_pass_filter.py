from __dsp__ import Filter
import numpy as np

def main() -> None:
    
    period = 20 # Center period
    beta = np.cos(2*np.pi/period)
    gamma = 1/np.cos(2*np.pi/period)
    alpha = gamma - np.sqrt(gamma**2 - 1)
    
    filt = Filter(name = "Ehlers Band-Pass filter", 
                  NumeratorZcoefs = [0.5*(1-alpha),0,-0.5*(1-alpha)], 
                  DenominatorZcoefs = [1,-beta*(1+alpha),alpha], 
                  comments = "Pass Band is 30 percent of the center \
                  frequency")
    
    filt.plotNormFreqResponse()
    filt.plotFreqResponse()
    filt.plotPeriodResponse()
    filt.plotPhaseResponse()
    filt.plotGroupDelay()

if __name__ == '__main__':
    main()
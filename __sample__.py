from __dsp__ import Filter

"""Easy to copy script to generate your own filters"""

def main() -> None:
    filt = Filter(name = "", 
                  NumeratorZcoefs = [], 
                  DenominatorZcoefs = [], 
                  comments = "")
    
    filt.plotNormFreqResponse()
    filt.plotFreqResponse()
    filt.plotPeriodResponse()
    filt.plotPhaseResponse()
    filt.plotGroupDelay()

if __name__ == '__main__':
    main()
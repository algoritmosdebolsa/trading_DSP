from __dsp__ import Filter

def main() -> None:
    filt = Filter(name = "2nd order Low-Pass FIR filter", 
                  NumeratorZcoefs = [1,2,1], 
                  DenominatorZcoefs = [4], 
                  comments = "")
    
    filt.plotNormFreqResponse()
    filt.plotFreqResponse()
    filt.plotPeriodResponse()
    filt.plotPhaseResponse()
    filt.plotGroupDelay()

if __name__ == '__main__':
    main()
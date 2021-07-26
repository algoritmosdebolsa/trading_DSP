from __dsp__ import Filter

def main() -> None:
    filt = Filter(name = "Very simple High-Pass FIR filter", 
                  NumeratorZcoefs = [1,-1],
                  DenominatorZcoefs = [2])
    
    filt.plotNormFreqResponse()
    filt.plotFreqResponse()
    filt.plotPeriodResponse()
    filt.plotPhaseResponse()
    filt.plotGroupDelay()

if __name__ == '__main__':
    main()
from __dsp__ import Filter

def main() -> None:
    filt = Filter(name = "10-bar window SMA", 
                  NumeratorZcoefs = [1,1,1,1,1,1,1,1,1,1], 
                  DenominatorZcoefs = [10], 
                  comments = "0 poles, 1 zero")
    
    filt.plotNormFreqResponse()
    filt.plotFreqResponse()
    filt.plotPeriodResponse()
    filt.plotPhaseResponse()
    filt.plotGroupDelay()

if __name__ == '__main__':
    main()
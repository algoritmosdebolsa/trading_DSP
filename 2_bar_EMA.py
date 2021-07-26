from __dsp__ import Filter

def main() -> None:
    alpha = 0.8
    filt = Filter(name = "2-bar window EMA", 
                  NumeratorZcoefs = [alpha], 
                  DenominatorZcoefs = [1, -(1-alpha)], 
                  comments = "1 pole, 0 zeros")
    
    # filt.plotNormFreqResponse()
    # filt.plotFreqResponse()
    filt.plotPeriodResponse()
    # filt.plotPhaseResponse()
    filt.plotGroupDelay()

if __name__ == '__main__':
    main()
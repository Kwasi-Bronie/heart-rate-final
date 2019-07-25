
import time
import Adafruit_ADS1x15


def heartrate():

    adc = Adafruit_ADS1x15.ADS1015()
    
    GAIN = 2/3
    curState = 0
    thresh = 600
    P = 400
    T = 400
    stateChanged = 0
    sampleCounter = 0
    lastBeatTime = 0
    firstBeat = True
    secondBeat = False
    Pulse = False
    IBI = 600
    rate = [0]*10
    amp = 100

    lastTime = int(time.time()*700)

    
    while True:
        
        Signal = adc.read_adc(0, gain=GAIN)   
        curTime = int(time.time()*700)

        sampleCounter += curTime - lastTime  
        lastTime = curTime
        N = sampleCounter - lastBeatTime;     
        

        if Signal < thresh and N > (IBI/5.0)*3.0 :  
            if Signal < T :                        
              T = Signal;                         

        if Signal > thresh and  Signal > P:   
            P = Signal;                        
                                                
          
        if N > 250 :                               
            if  (Signal > thresh) and  (Pulse == False) and  (N > (IBI/5.0)*3.0)  :       
              Pulse = True;                               
              IBI = sampleCounter - lastBeatTime; 
              lastBeatTime = sampleCounter;             

              if secondBeat :                        
                secondBeat = False;             
                for i in range(0,10):             
                  rate[i] = IBI;                      

              if firstBeat :                        
                firstBeat = False;                   
                secondBeat = True;                   
                continue                             
            
              runningTotal = 0;                  
              for i in range(0,9):
                rate[i] = rate[i+1];                  
                runningTotal += rate[i];              

              rate[9] = IBI;                        
              runningTotal += rate[9];   
              runningTotal /= 10;                 
              BPM = 60000/runningTotal;               
              return BPM

        if Signal < thresh and Pulse == True :   
            Pulse = False;                         
            amp = P - T;                           
            thresh = amp/2 + T;                   
            P = thresh;                            
            T = thresh;

        if N > 2500:                          
            thresh = 512;                         
            P = 400;                               
            T = 4000;                               
            lastBeatTime = sampleCounter;               
            firstBeat = True;                      
            secondBeat = False;                  

        time.sleep(0.005)
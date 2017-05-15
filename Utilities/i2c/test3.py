import time
import Adafruit_ADS1x15

adc=Adafruit_ADS1x15.ADS1115(address=0x48,busnum=1)
GAIN = 1

for i in range(4):
   print(adc.read_adc(i,gain=GAIN))

import smbus
import time
bus = smbus.SMBus(1)
address = 0x48


#while True:
#	print(bus.read_byte_data(address,1))
#	time.sleep(0.5)

for device in range(128):

      try:
         bus.read_byte(device)
         print(hex(device))
      except: # exception if read_byte fails
         pass



# https://gpiozero.readthedocs.io/en/stable/remote_gpio.html
# raspberrypi.org/documentation/configuration/wireless/access-point.md
from gpiozero import LED
from gpiozero.pins.pigpio import PiGPIOFactory
import time
from time import sleep

partnum = input("partnum: ")
factory = PiGPIOFactory(host='192.168.4.5') # host='129.128.174.163'
led = LED(17,pin_factory=factory)
local_pi_trigs = []
start_time = time.time()

for i in range(100):
    local_pi_trigs.append(start_time - time.time())
    led.on()
    sleep(1)
    led.off()
    sleep(1)

###save trial information###
filename = "test"
filename_part = ("/home/pi/Documents/GoPro_Grid_Pi/data/test/" + partnum + "_" + filename + ".csv")


np.savetxt(filename_part, (local_pi_trigs), delimiter=',',fmt="%s")
# https://gpiozero.readthedocs.io/en/stable/remote_gpio.html
# raspberrypi.org/documentation/configuration/wireless/access-point.md
from gpiozero import LED
from gpiozero.pins.pigpio import PiGPIOFactory
import time
from time import sleep
import numpy as np
import subprocess


def ping_response(host):
    p1 = subprocess.Popen(['ping','-c2', host], stdout=subprocess.PIPE)
    output = p1.communicate()[0]
    return(output)

# to run "GPIOZERO_PIN_FACTORY=pigpio python3 Remote_Pin_Control.py"

partnum = input("partnum: ")
factory = PiGPIOFactory(host='192.168.4.2') # host='129.128.174.163'
led = LED(17,pin_factory=factory)
length = 200
local_pi_trigs = np.zeros((length))
ping_pi_trigs = np.zeros((length))

start_time = time.time()

for i in range(length):
    local_pi_trigs[i] = time.time() - start_time
    ping_pi_trigs[i] = ping_response('192.168.4.2')
    print(time.time() - start_time)
    led.on()
    sleep(1)
    led.off()
    sleep(1)

###save trial information###
filename = "test"
filename_part = ("/home/pi/Documents/GitHub/GoPro_Grid_Pi/Pi3_Amp_Latencies/Pi_Times/" + partnum + "_" + filename + ".csv")


np.savetxt(filename_part, (local_pi_trigs,ping_pi_trigs), delimiter=',',fmt="%s")

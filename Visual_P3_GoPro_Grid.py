#tasks use pwmled instead of led
#make sure button is using SPI pin to send information to the server



#importing modules
import board
import time
from random import randint, shuffle
import numpy as np
from gpiozero.pins.pigpio import PiGPIOPin
from gpiozero.pins.pigpio import PiGPIOFactory
from neopixel import *
from gpiozero import MCP2008, PWMLED

class experiment:
    def __init__(self, partnum, trial_num):
        # I approach pin organization by setting the remote pins to be native of the local machine and redefining the lcoal pins under a different 'factory'
        local_factory = PiGPIOFactory(host='192.168.1.3') # Server Pi - needs to be specified - since most is happening with the other Pi's pins
        #remote_factory = PiGPIOFactory(host='192.168.1.4') # Client Pi - don't specify here as long as you run the script, preceded by the following environmental variables: GPIOZERO_PIN_FACTORY=pigpio PIGPIO_ADDR=192.168.1.3

        ##pins we will be using ##
        self.trig_pins = [4,17,27,22,5,6,13,19]

        #button connected to sever pi (should allow the lights to wait for button trigger on server pi)
        self.button = Button(PiGPIOPIn(19)
        self.led = PWMLED(17, pin_factory = local_factory)  #using thet MOSI pin (master out slave in) alows the client pi to send information to the server pi

        #controls Pi's SPI pins
        pot = MCP3008(0)
        self.led.source = pot
        ##setup some constant variables##
        self.partnum = partnum
        self.filename = 'visual_p3_gopro_visor'

        ##number of trials##
        self.trial_num = trial_num


        ##standard and target rate##
        standard_rate = 0.8
        target_rate = 0.2

        ##distribution of targets and standards##
        self.trials = np.zeros(int(self.trial_num*self.standard_rate)).tolist() + np.ones(int(self.trial_num*self.target_rate)).tolist()
        shuffle(self.trials) # randomize order of standards and targets

        ##several colours for the pixels##
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)
        self.blank = (0, 0, 0)
        self.brightness = 0.2

        ##number of pixels we will be controlling##
        self.pin_num = 6

        ##specify which pin we will be controlling the LEDs with##
        pin_out = board.D18

        ##amount of time needed to reset triggers##
        self.trig_gap = 0.005

        ##setup our neopixels##
        self.pixels = neopixel.NeoPixel(self.pin_out, self.pin_num, brightness = self.brightness, auto_write = True)


    def resp_trig(self, trig): # maps response trigger to standard (3) or target (4)
        if trig == 0.5:
            resp_trig = 0.3
        if trig == 1:
            resp_trig = 0.4
        self.led.value = resp_trig
        time.sleep(self.trig_gap)
        self.led.value = 0
        time.sleep(self.trig_gap)


    def get_resp_led_off(led_on_time,trig): # get response (if occured in first 1 second) + turn off the LEDs regardless
        start_resp = time.time()
        #waits a certain amount of time for button press
        self.button.wait_for_press(timeout = int(led_on_time * 1000))
        button_down = time.time() - start_resp # this is response time from the start of the 1 second response window


    def get_resp_led_off(led_on_time,trig): # get response (if occured in first 1 second) + turn off the LEDs regardless
        start_resp = time.time()
        #waits a certain amount of time for button press
        self.button.wait_for_press(timeout = int(led_on_time * 1000))
        button_down = time.time() - start_resp # this is response time from the start of the 1 second response window

        if button_down < led_on_time: ## right now this isn't making any sense to me
            resp_trig(trig)
            resp_time = button_down
            if button_down <= 0.990:
                time.sleep(led_on_time - (button_down + self.trig_gap*2)) # wait until the end of the 1 second of the light being on
        else:
            resp_time = 0

        # before_second_light = time.time() - start_exp
        self.pixels.fill(self.blank)
        # after_second_light = time.time() - start_resp
        if trig == 1: ## Maps out offset trigger to standard and target flashes
            self.led.value = 0.5
        else:
            self.led.value = 0.6
        time.sleep(self.trig_gap)
        self.led.value = 0

        return resp_time # before_second_light, after_second_light


    def get_resp(self, wait_time, prev_delay, resp, trig): # get response (if not in the first second) + wait for wait time (delay)
        start_resp = time.time()

        #waits a certain amount of time for button press
        self.button.wait_for_press( timeout = int(wait_time * 1000))
        delay_end_time = time.time() - start_resp

        if resp == 0:
            resp_time = delay_end_time + prev_delay
            if resp_time <= 2.0:
                resp_trig(trig)
        else:
            resp_time = resp

        if delay_end_time < wait_time:
            time.sleep(wait_time - delay_end_time)

        return resp_time


    def wheel(self, pos):
        # Input a value 0 to 255 to get a color value.
        # The colours are a transition r - g - b - back to r.
        if pos < 0 or pos > 255:
            r = g = b = 0
        elif pos < 85:
            r = int(pos * 3)
            g = int(255 - pos*3)
            b = 0
        elif pos < 170:
            pos -= 85
            r = int(255 - pos*3)
            g = 0
            b = int(pos*3)
        else:
            pos -= 170
            r = 0
            g = int(pos*3)
            b = int(255 - pos*3)
        return (r, g, b)


    def rainbow_cycle(self, wait, rainbow_time):
        start = time.time()
        while time.time() - start < rainbow_time:
            for j in range(255):
                for i in range(self.pin_num):
                    pixel_index = (i * 256 // self.pin_num) + j
                    pixels[i] = wheel(pixel_index & 255)
                self.pixels.show()
                time.sleep(wait)


    def refresh_trig_visor(self, x): # structure output of CSV
        trig_type.append(x)
        trig_time.append(time.time() - start_exp)
        delay_length.append(2)
        trial_resp.append(0)
        resp_latency.append(0)
        time.sleep(2) ## leave red on for 2 seconds
        self.pixels.fill(self.blank)
        self.led.value = 0


    def run_blocks(self,block_num):
        #dictionary of information for easy storage
        trial_dict = {}

        #trail infromation to be saved
        trial_dict[trig_time]  = []
        trial_dict[trig_type] = []
        trial_dict[delay_length]  = []
        trial_dict[trial_resp] = []
        trial_dict[resp_latency] = []
        trial_dict[block_start_stop] = []
        trial_dict[exp_start_stop] = []

        index = 0
        while index <= block_num:
            #waits for button input to start block
            self.button.wait_for_press()
            self.pixels.fill(self.red)
            self.led.value = 0.10

            if block == 0:
                start_exp = time.time()
                trial_dict[exp_start_stop].append(0)
                trial_dict[block_start_stop].append(time.time() - start_exp) # start of each block from start_exp
                refresh_trig_visor(3)
                time.sleep(2)

            self.run_trials(self,self.trials,trials_dict)

            ##end of block##
            self.pixels.fill(self.red)
            self.led.value = 0.11 # send unique trigger for the end of a block
            trial_dict[trig_time].append(time.time() - start_exp)
            trial_dict[block_start_stop].append(time.time() - start_exp) # end of each block from start_exp
            refresh_trig_visor(4)
            time.sleep(2)
            index += 1

        return trial_dict


    def run_trials(self,trials,trial_dict):

        for i_trial in range(len(trials)):
            start_trial = time.time() + self.trig_gap # define start time of a given trial
            delay = ((randint(0,500)*0.001)+1.0) # define delay, to be used later
            trial_dict[delay_length].append(delay)

            ##determine the type of stimuli we will show on this trial##
            if trials[i_trial] == 0: #standards
                trig = 0.5
                self.pixels.fill(self.green)

            elif trials[i_trial] == 1: #targets
                trig = 1.0
                self.pixels.fill(self.blue)

            ## Specify which trigger to send Standard vs Target
            self.led.value = trig
            trial_dict[trig_type].append(trig)
            trial_dict[trig_time].append(time.time() - start_exp)
            time.sleep(self.trig_gap)

            self.led.value = 0
            resp_time = get_resp_led_off(1.0,trig) # before_second_light, after_second_light
            resp_time = get_resp(delay, 1.0, resp_time,trig)
            trial_dict[resp_latency].append(time.time() - start_exp)
            trial_dict[trial_resp].append(resp_time)

            self.led.value = 0 ## doesn't give us a trigger
            time.sleep(self.trig_gap)
            end_trial = time.time()

        return trail_dict


    def end(self,trial_dict):
        self.rainbow_cycle(0.001, 5) ## After all blocks finished flash a rainbow at a refresh of (1st arguement) ms for (2nd arguement) seconds
        self.pixels.fill(self.blank)

        ###save trial information###
        filename_part = ("/home/pi/GitHub/GoPro_Visor_Eye_Pi/Pilot_Data/Experiment_1/" + self.partnum + "_" + self.filename + ".csv")

        np.savetxt(filename_part, (trial_dict[trig_type],trial_dict[trig_time], trial_dict[delay_length], trial_dict[trial_resp], trial_dict[resp_latency], trial_dict[block_start_stop]), delimiter=',',fmt="%s")


def main():
    partnum = input("partnum: ")
    trial_num = int(input("How many trials per block?: "))
    block_num = int(input("How many blocks?: "))

    exp = experiment(partnum, trial_num)
    trial_dict = exp.run_blocks(block_num)
    exp.end(trial_dict)

    return

if __name__ == "__main__":
    main()

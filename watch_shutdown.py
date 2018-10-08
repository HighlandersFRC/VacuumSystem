#! /usr/bin/python

import RPi.GPIO as GPIO ## Import GPIO Library
import time             ## Allows us to use : sleep, time fucntions
import datetime         ## Allows us to use : sleep, time fucntions
import os               ## for invoking shell commands

GPIO_SHUTDOWN = 12 



# My callback for GPIO button press
def my_shutdown (channel) :
    global time_stamp
    time_now = time.time()
    if ((time_now - time_stamp) >= 1) :
        print ("Hit shutdown button: ${0}", channel)
        set_gpio_defaults_and_exit
        os.system("sudo shutdown -h now")
        #os.system("ls -l")
    time_stamp = time_now

# Set up gpio for button
def enableButton () :
    print ("Enable shutdown button. GPIO = ${0}", GPIO_SHUTDOWN)
    GPIO.add_event_detect( GPIO_SHUTDOWN, GPIO.FALLING, callback=my_shutdown)


#
def set_gpio_defaults () :
    GPIO.setwarnings ( False )
    GPIO.setmode ( GPIO.BOARD )  ## Use BOARD pin numbering
    GPIO.setup ( GPIO_SHUTDOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP )
# END set_gpio_defaults ()


############################################################################
#
# Clean shutdown GPIOs
#
def set_gpio_defaults_and_exit () :

    set_gpio_defaults ()
    GPIO.cleanup ()

# END set_gpio_defaults_and_exit ()



#
# Invoke main program        
#
time_stamp = time.time()
set_gpio_defaults ()

enableButton()

while True :
    time.sleep (10)

set_gpio_defaults_and_exit ()



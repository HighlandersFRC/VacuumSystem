#! /usr/bin/python

import RPi.GPIO as GPIO ## Import GPIO Library
import time             ## Allows us to use : sleep, time fucntions
import datetime         ## Allows us to use : sleep, time fucntions
import smtplib          ## for sending email
import os               ## for invoking shell commands
from subprocess import Popen,PIPE       ## to get stdout from cmd
import subprocess       ## to get stdout from cmd

valve_delay_open_sec  = 1.0
valve_delay_close_sec = 1.0

# GPIO pin assignments for the two valves
vacuum_valve   = 7  # GREEN
pressure_valve = 11 # GREY 



############################################################################
#
# Initialize GPIO pins
#
def set_gpio_defaults () :


    GPIO.setwarnings ( False )

    GPIO.setmode ( GPIO.BOARD )  ## Use BOARD pin numbering

    GPIO.setup ( vacuum_valve,   GPIO.OUT ) ## Setup GPIO pin vac valve to OUT
    GPIO.setup ( pressure_valve, GPIO.OUT ) ## Setup GPIO pin pressure valve to OUT

# END set_gpio_defaults ()


############################################################################
#
# Clean shutdown GPIOs
#
def set_gpio_defaults_and_exit () :

    set_gpio_defaults ()

    GPIO.cleanup ()

# END set_gpio_defaults_and_exit ()


############################################################################
#
# Turn on vacuum system. All valves open.
#
def turn_on_vacuum ():

    print "DEBUG: turn vacuum on"

    # open pressure valve which turns on venturi.
    GPIO.output ( pressure_valve, True ) 

    # pause one for vacuum to build before opening path to vacuum bag.
    time.sleep ( valve_delay_open_sec )

    # Open valve to vacuum bag.
    GPIO.output ( vacuum_valve, True ) 
	
# END turn_on_vacuum ()



############################################################################
#
# Turn on vacuum system.
#
def on ():

    set_gpio_defaults ()

    turn_on_vacuum ()

# END on ()



#
# Invoke main program        
#
on ()

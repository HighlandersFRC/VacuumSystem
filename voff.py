#! /usr/bin/python

import RPi.GPIO as GPIO ## Import GPIO Library
import time             ## Allows us to use : sleep, time fucntions
import datetime         ## Allows us to use : sleep, time fucntions
import smtplib          ## for sending email
import os               ## for invoking shell commands
from subprocess import Popen,PIPE       ## to get stdout from cmd
import subprocess       ## to get stdout from cmd

valve_delay_open_sec  = 1.0
valve_delay_close_sec = 2.0

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
# Turn off vacuum system and close all valves.
#
def turn_off_vacuum ():

    print "DEBUG: turn vacuum off"

    # Close valve to isolate vacuum in vacuum bag.
    GPIO.output ( vacuum_valve,  False )

    # pause to allow valve to vacuum bag to completely close before turning
    # off venturi.
    time.sleep ( valve_delay_close_sec )

    # Close pressure valve which turns off venturi to save air.
    GPIO.output ( pressure_valve, False ) 
	
# END turn_off_vacuum ()



############################################################################
#
# Turn off vacuum system and close all valves.
#
def off ():

    set_gpio_defaults ()

    turn_off_vacuum ()

# END off ()



#
# Invoke main program        
#
off ()

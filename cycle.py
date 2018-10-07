#! /usr/bin/python

import RPi.GPIO as GPIO ## Import GPIO Library
import time             ## Allows us to use : sleep, time fucntions
import datetime         ## Allows us to use : sleep, time fucntions
import smtplib          ## for sending email
import os               ## for invoking shell commands
from subprocess import Popen,PIPE       ## to get stdout from cmd
import subprocess       ## to get stdout from cmd
from Adafruit_LED_Backpack import SevenSegment 

# File name to read for new vacuum off time
voff_file = '/home/pi/gpio/voff_time.txt'
von_file  = '/home/pi/gpio/von_time.txt'
vac_on    = 0
vacuum_on_time_sec    = 30
vacuum_off_time_sec   = 5 
valve_delay_open_sec  = 1  #0.50
valve_delay_close_sec = 0.1
VAC_SENSE_POLL_FREQ_SEC = 2    # Polling frequency when sensing vacuum
vac_volts             = 0.69    # Voltage from vac sensor, default for no vacuum
VAC_V_MIN             = 0.00    # Voltage from vac sensor: vacuum is too low so turn on vacuum
VAC_V_MAX             = 0.05    # Voltage from vac sensor: vacuum max setting so turn off vacuum
VAC_V_PER_PSI         = 0.05    # Voltage from vac sensor: volts per PSI
VAC_V_0               = 0.70    # Voltage from vac sensor: volts at atmospheric

# Sides and back for robot cart: 12/11/2016
VAC_V_MAX             = 0.1    # Voltage from vac sensor: vacuum max setting so turn off vacuum
VAC_V_MIN             = 0.2    # Voltage from vac sensor: vacuum is too low so turn on vacuum

#READ_VAC_VOLTS_CMD = "/home/pi/adafruit/Adafruit-Raspberry-Pi-Python-Code/Adafruit_ADS1x15/ads1x15_ex_singleended.py"
READ_VAC_VOLTS_CMD = "/home/pi/vac/original/gpio/Adafruit-Raspberry-Pi-Python-Code/Adafruit_ADS1x15/ads1x15_ex_singleended.py"

MY_SMTP_SERVER = 'smtp.mine.com:587'
MY_SMTP_USER = 'me'
MY_SMTP_PASS = 'em'

# GPIO pin assignments for the two valves
GPIO_VAC_SOLENOID   = 11  # GREEN
GPIO_PRESSURE_VALVE = 7 # GREY 
GPIO_QUIT = 18 
GPIO_SHUTDOWN = 16 

keep_vacuum = True

fon = False


# My callback for GPIO button press
def my_quit (channel) :
    global keep_vacuum
    global time_stamp

    time_now = time.time()
    if ((time_now - time_stamp) >= 1) :
        print ("Hit shutdown button: ${0}", channel)
        turn_off_vacuum ()
        keep_vacuum = False
    time_stamp = time_now

# My callback for GPIO button press
def my_shutdown (channel) :
    global time_stamp
    time_now = time.time()
    if ((time_now - time_stamp) >= 1) :
        print ("Hit shutdown button: ${0}", channel)
        os.system("sudo shutdown -h now")
        #os.system("ls -l")
    time_stamp = time_now

# Set up gpio for button
def enableButton () :
    print ("Enable shutdown button. GPIO = ${0}", GPIO_SHUTDOWN)
    #print ("Enable quit button. GPIO = ${0}", GPIO_QUIT)

    GPIO.setwarnings ( False )
    GPIO.setmode ( GPIO.BOARD )
    GPIO.setup ( GPIO_QUIT, GPIO.IN, pull_up_down=GPIO.PUD_UP )
    GPIO.setup ( GPIO_SHUTDOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP )

    #GPIO.add_event_detect( gpio_shutdown, GPIO.FALLING, callback=turn_off_vacuum)

    GPIO.add_event_detect( GPIO_SHUTDOWN, GPIO.FALLING, callback=my_shutdown)
    GPIO.add_event_detect( GPIO_QUIT, GPIO.FALLING, callback=my_quit)

def showPSI(psi):
    global segment
    global fon
    segment.clear()

    # Set hours
    #segment.set_digit(0, int(psi / 10))
    #segment.set_digit(0, 2)     # Tens
    #segment.set_digit(0, psi%10)     # Tens

    segment.set_digit(0, int(psi/10)) 
    segment.set_digit(1, int(psi % 10))

    # Toggle colon
    if (fon):
        fon = False
        #segment.set_colon(0)              # Toggle colon at 1Hz
    else:
        fon = True
        #segment.set_colon(1)              # Toggle colon at 1Hz

    # Write the display buffer to the hardware.  This must be called to
    # update the actual display LEDs.
    segment.write_display()
    


############################################################################
#
# Read vac_volts
#
def get_vac_volts () :

    global vac_volts
	
    p1 = Popen([READ_VAC_VOLTS_CMD], stdout=subprocess.PIPE)
	
    # Read standard out from process [0]. Stderr is [1].
    vac_volts = float(p1.communicate()[0])
    psi = round( vac_volts_to_psi(vac_volts), 2)
    psi = abs(psi)
    print "Vacuum PSI: ", psi, "Volts: ", round( vac_volts, 2)
    showPSI(psi)

# END get_vac_volts ()


############################################################################
#
# Initialize GPIO pins
#
def set_gpio_defaults () :


    GPIO.setwarnings ( False )

    GPIO.setmode ( GPIO.BOARD )  ## Use BOARD pin numbering

    GPIO.setup ( GPIO_VAC_SOLENOID,   GPIO.OUT ) ## Setup GPIO pin vac valve to OUT
    GPIO.setup ( GPIO_PRESSURE_VALVE, GPIO.OUT ) ## Setup GPIO pin pressure valve to OUT

    vac_on = 1 

    turn_off_vacuum ()

# END set_gpio_defaults ()


############################################################################
#
# Clean shutdown GPIOs
#
def set_gpio_defaults_and_exit () :

    set_gpio_defaults ()

    turn_off_vacuum ()

    GPIO.cleanup ()

# END set_gpio_defaults_and_exit ()


############################################################################
#
# Open both valves which turns on venturi vacuum.
# Open vacuum valve one second after pressure valve to insure venturi
# vacuum has time to build up.
#
def turn_on_vacuum ():

    global vac_on

    vac_on = 1

    print "DEBUG: turn vacuum on"

    # open pressure valve which turns on venturi.
    GPIO.output ( GPIO_PRESSURE_VALVE, True ) 

    # pause one second for vacuum to build before opening path to
    # vacuum bag.
    time.sleep ( valve_delay_open_sec )

    # Open valve to vacuum bag.
    GPIO.output ( GPIO_VAC_SOLENOID, True ) 
	
# END turn_on_vacuum ()



############################################################################
#
# Close both valves which turns off venturi vacuum and holds vacuum.
# Close pressure valve one second after closing vacuum valve to prevent
# vacuum leak.
#
def turn_off_vacuum ():

    global vac_on

    vac_on = 0

    print "DEBUG: turn vacuum off"

    # Close valve to isolate vacuum in vacuum bag.
    GPIO.output ( GPIO_VAC_SOLENOID,  False )

    # pause to allow valve to vacuum bag to completely close before turning
    # off venturi.
    time.sleep ( valve_delay_close_sec )

    # Close pressure valve which turns off venturi to save air.
    GPIO.output ( GPIO_PRESSURE_VALVE, False ) 
	
# END turn_off_vacuum ()


############################################################################
#
# Log state of system to text file and send periodic email.
# Periodic emails every 15 iterations.
#
def email_state ():

    s = smtplib.SMTP ( MY_SMTP_SERVER )
    s.starttls ()
    s.login    ( MY_SMTP_USER, MY_SMTP_PASS )
    s.sendmail ( MY_SMTP_USER, MY_SMTP_USER, 'still running' )
    s.quit ()

# END email_state ()


############################################################################
#
# Read vacuum on time from a file.
# This allows duynamic changing of the build vacuum time
# without restarting the script.
#
def get_vacuum_on_time_sec ():

    fp = open ( von_file )

    on_time_sec = float ( fp.read () )

    fp.close ()

    return on_time_sec

# END get_vacuum_on_time_sec ()


############################################################################
#
# Read vacuum hold time from a file.
# This allows duynamic changing of the hold time
# without restarting the script.
#
def get_vacuum_off_time_sec ():

    fp = open ( voff_file )

    off_time_sec = float ( fp.read () )

    fp.close ()

    return off_time_sec

# END get_vacuum_off_time_sec ()


############################################################################
#
# Convert volts from vacuum sensor to PSI
#
def vac_volts_to_psi ( volts ):

   return (float(volts) - VAC_V_0) / VAC_V_PER_PSI

# END vac_volts_to_psi ()


############################################################################
#
# Run an infinite loop cycling vacuum and pressure valves to accumulate and
# then hold a vacuum in the system indefinitely.
#
# Note: Send an email to tfrye@frenchryes once every 15 mins for remote 
# monitoring.
#
def regulate_vacuum_sense ():

    global vac_volts
    global vac_on
    global keep_vacuum

    set_gpio_defaults ()

    get_vac_volts ()
	
    print "Regulating vacuum: psi = ", vac_volts_to_psi (vac_volts), ", volts = ", vac_volts

    while keep_vacuum :
	
        get_vac_volts ()

        if ( vac_volts < VAC_V_MIN ) :
            if ( vac_on == 1 ) :
                print "turn off vacuum: psi = ", vac_volts_to_psi (vac_volts), ", volts = ", vac_volts
                turn_off_vacuum ()
        elif ( vac_volts > VAC_V_MAX ) :
            if ( vac_on == 0 ) :
                print "turn on vacuum: psi = ", vac_volts_to_psi (vac_volts), ", volts = ", vac_volts
                turn_on_vacuum ()
    	
        # Sleep one second then loop
        time.sleep ( VAC_SENSE_POLL_FREQ_SEC ) 
		
    set_gpio_defaults_and_exit ()

# END regulate_vacuum_sense ()


############################################################################
#
# Run an infinite loop cycling vacuum and pressure valves to accumulate and
# then hold a vacuum in the system indefinitely.
#
# Note: Send an email to tfrye@frenchryes once every 15 mins for remote 
# monitoring.
#
def regulate_vacuum_time ():

    global vacuum_on_time_sec
    global vacuum_off_time_sec
    global keep_vacuum

    set_gpio_defaults ()

    # Keep a cycle count for logging progress
    cycle_count = 0

    print "Regulating vacuum by time: vacuum on time = ", vacuum_on_time_sec, \
        ", vacuum off time = ", vacuum_off_time_sec

    while keep_vacuum :

        # Print cycle count every 10 iterations
        if ( ( cycle_count % 10 ) == 0 ) :
            print "\tcycle count: ", cycle_count

        # Read vacuum on time from a file every iteration
        tmp = get_vacuum_on_time_sec ()
        if ( tmp != vacuum_on_time_sec ) :
            print "CHANGE vacuum on time: old = ", vacuum_on_time_sec, \
                ", new = ", tmp 
            vacuum_on_time_sec = tmp

        # Read vacuum off time from a file every iteration
        tmp = get_vacuum_off_time_sec ()
        if ( tmp != vacuum_off_time_sec ) :
            print "CHANGE vacuum off time: old = ", vacuum_off_time_sec, \
                ", new = ", tmp 
            vacuum_off_time_sec = tmp

        # email program state every 15 iterations
        #if ( ( cycle_count % 95 ) == 0 ) :
            #email_state ()

        # turn on both valves to begin vacuum
        turn_on_vacuum ()

        # Leave valves open to accumulate vacuum
        time.sleep ( vacuum_on_time_sec ) 

        # turn off both valves to hold vacuum
        turn_off_vacuum ()

        # Pause with valves closed to hold vacuum 
        time.sleep ( vacuum_off_time_sec )

        cycle_count += 1

    set_gpio_defaults_and_exit ()

# END regulate_vacuum_time ()



#
# Invoke main program        
#
time_stamp = time.time()
enableButton()
segment = SevenSegment.SevenSegment(address=0x70)

# Initialize the display. Must be called once before using the display.
segment.begin()

regulate_vacuum_sense ()
#regulate_vacuum_time ()
#set_gpio_defaults_and_exit ()

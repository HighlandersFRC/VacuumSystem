# VacuumSystem
This repository contains python scripts designed to run on a RaspberryPi to control a custom venturi vacuum system.

## Usage Instructions
1. Automatic behavoir once installation and configuration are complete

1. Manually start and stop vacuum
   1. /home/pi/
   1. /home/pi/


## Compatibility
1. These instructions were verified with the following configurations:
   1. Raspberry PI 2 Model B, Raspian OS Version: **9.4 (stretch)**
      - Linux raspberrypi 4.14.62-v7+ #1134 SMP Tue Aug 14 17:10:10 BST 2018 armv7l GNU/Linux


## Configuration Instructions
1. Raspberry PI Configuration
   1. Update PI OS
      Note: [Upgrade Options](https://askubuntu.com/questions/81585/what-is-dist-upgrade-and-why-does-it-upgrade-more-than-upgrade)
      1. sudo apt-get update
      1. sudo apt-get dist-upgrade
      1. sudo apt-get autoremove
      1. sudo reboot

   1. Install Development Packages
      1. sudo apt-get install -y git build-essential python-dev
      1. sudo apt-get install -y python-smbus python-imaging
      1. sudo apt-get install -y git python-pip python-pil
      1. sudo apt-get install -y i2c-tools python-smbus

   1. Install Adafruit packages on the Raspberry PI
      Note: Older Adafruit github repo conatined all packages in one repo. There are now separate repos for each product.

      1. Suggested directory for Adafruit tools:
         1. **cd**
         1. **mkdir adafruit**
         1. **cd adafruit**

     1. [Adafruit LED Backpack](https://learn.adafruit.com/adafruit-led-backpack/0-dot-56-seven-segment-backpack)
         1. **git clone https://github.com/adafruit/Adafruit_Python_ADS1x15.git**
         1. **cd Adafruit_Python_LED_ADS1x15/**
            1. **sudo python setup.py install** Run again if errors. Reboot and re-run if that doesn't work.

     1. [Adafruit LED Backpack](https://learn.adafruit.com/adafruit-led-backpack/0-dot-56-seven-segment-backpack)
        [Adafruit Python LED](https://learn.adafruit.com/matrix-7-segment-led-backpack-with-the-raspberry-pi?view=all)
        [Adafruit Tutorial](https://learn.adafruit.com/adafruit-led-backpack)
         1. **git clone https://github.com/adafruit/Adafruit_Python_LED_Backpack.git**
         1. **cd Adafruit_Python_LED_Backpack/**
            1. **sudo python setup.py install** Run again if errors. Reboot and re-run if that doesn't work.

   1. Configure Crontab to start automatic vacuum control upon reboot
      1. See file: **/var/spool/cron/crontabs/pi**
      1. The main configuration line to be added is:
         **@reboot nohup /home/pi/start.sh > /home/pi/start.log 2>&1 &**

   1. Scripts from this repo used to manage streaming should be copied to **/home/pi/**
      1. **/home/pi/mjpg-streamer.sh** helper script to invoke mjpg-streamer binary
      1. **/home/pi/start.sh** Simple wrapper to invoke mjpg-streamer for multiple cameras.
      1. **/home/pi/stop.sh** Optional wrapper to kill all running instances of mjpg-streamer.
      1. **/home/pi/status.sh** Optional wrapper to report status of any running instances of mjpg-streamer.
      1. **/home/pi/down.sh** Optional wrapper to shutdown PI.

## Basic Raspberry PI How-To:
1. [Check Hardware version](https://elinux.org/RPi_HardwareHistory)
   - cat /proc/cpuinfo
1. [Check Raspian OS version](https://www.meccanismocomplesso.org/en/how-to-raspberry-checking-raspbian-version-update-upgrade/)
   - cat /etc/os-release
   - lsb_release -a
   - uname -a
1. [Configure static IP on the PI for wired, eth0](https://www.raspberrypi.org/forums/viewtopic.php?t=191140)


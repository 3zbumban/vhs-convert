#!/usr/bin/python3

import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import socket

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)

def listen_on_button():
    while True: # Run forever
        if GPIO.input(10) == GPIO.HIGH:
            print("Button was pushed!")

def main():
    listen_on_button()

if __name__ == "__main__":
    main()
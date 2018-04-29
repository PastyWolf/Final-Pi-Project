#######################################################################
# Name: Prasil Mainali
# Date: 4-14-18
# Description: Using RPI we will implement the idea of paper piano
######################################################################

import RPi.GPIO as GPIO
from array import array
from random import randint
from time import sleep, time
import pygame

DEBUG = True
pygame.init()

switches = [25, 24, 23, 22]
sounds = [ pygame.mixer.Sound("one.wav"),\
           pygame.mixer.Sound("two.wav"),\
           pygame.mixer.Sound("three.wav"),\
           pygame.mixer.Sound("four.wav"),]

GPIO.setmode(GPIO.BCM)
GPIO.setup(switches, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(leds, GPIO.OUT)

# this function turns the LEDs on
def all_on():
    for i in leds:
        GPIO.output(leds, True)

def all_off():
    for i in leds:
        GPIO.output(leds, False)

#This function flashes the LEDS a few times when the player loses the game
def lose():
    # prints the users score
    if (len(seq) == 3):
        print "You didn't even make it a sequence!"
    else:
        print ("You made it to a sequence of {}!").format(len(seq) - 3)
    for i in range(0, 4):
        all_on()
        sleep(0.5)
        all_off()
        sleep(0.5)
# The main part of the program
# initialize the simon sequence
# each item in the sequence represents an LED (or switch), indexed at zero through three
seq = []
# randomly add the first two items to the sequence
seq.append(randint(0, 3))
seq.append(randint(0, 3))

print "Welcome to Simon!"
print "Try to play the sequence back by pressing the switches."
print "Press Cntrl+C to exit..."

# we'll discuss this later, but this allows us to detect when ctrl+c is pressed so that we can reset the GPIO pn
# detext when cntrl+c is pressed so we can reset GPIO pins
# everything within this try-except construct will run forever until cntr+c
# will talk about more in 132
try:
    # keep going until the user presses cntrl+c
    # while runs as long as the statement in the () is true. True is always true so it goes forever
    while (True):
        # randomly add one more item to sequence
        seq.append(randint(0, 3))
        if (DEBUG):
            # display the sequence to the console
            if (len(seq) > 3):
                print
            print "seq={}".format(seq)
        #display the sequence  using the LEDS
        for s in seq:
            # turn the appropiate LED on
            GPIO.output(leds[s], True)
            #play the corresponding sound
            sounds[s].play()
            # wait and turn the LED off again
            if (len(seq) < 5):
                sleep(1)
                GPIO.output(leds[s], False)
                sleep(0.5)
            elif (len(seq) < 7):
                sleep(0.9)
                GPIO.output(leds[s], False)
                sleep(0.4)
            elif (len(seq) < 10):
                sleep(0.8)
                GPIO.output(leds[s], False)
                sleep(0.3)
            elif (len(seq) < 13):
                sleep(0.7)
                GPIO.output(leds[s], False)
                sleep(0.25)
            elif (len(seq) < 15):
                sleep(0.6)
                GPIO.output(leds[s], False)
                sleep(.15)
            elif (len(seq) >= 15):
                # keeps LEDs off (mostly) but sound on for .6
                GPIO.output(leds[s], False)
                sleep(.6)
                # keeps LEDs off (mostly) but delay between sounds for .15
                GPIO.output(leds[s], False)
                sleep(.15)
                
        # wait for player input (via the switches)
        # initialize the count of switches pressed ot zero
        switch_count = 0
        # keep accepting player input until the number of items in dsquence is reached
        while (switch_count < len(seq)):
            # initially note that no switch is pressed
            # this will help with switch debouncing
            pressed = False
            # so long as no switch is currently pressed
            while (not pressed):
                #...we can check the status of each switch
                for i in range (len(switches)):
                    # if one switch is pressed
                    while (GPIO.input(switches[i]) == True):
                        # note its index
                        val = i
                        # note that a switch has now been pressed
                        # so that we don't detect any more switch presses
                        pressed = True
            if (DEBUG):
                # display the index of the switch pressed
                print val,

            # light the matching LED
            GPIO.output(leds[val], True)
            # play the corresponding sound
            sounds[val].play()
            # wait and turn the led off again
#############DONT MESS WITH THESE FOR SPEED. THIS IS USER INPUT###############################
            sleep(1)
            GPIO.output(leds[val], False)
            sleep(0.25)

            # Check to see if this led is correct in the sequence
            if (val != seq[switch_count]):
                # player is incorrect; invoke the lose function
                lose()
                #reset the GPIO pins
                GPIO.cleanup()
                # exit the game
                exit(0)

            # if the player has this item in the sequence correct, increment the count
            switch_count += 1
            
except KeyboardInterrupt:
    # reset the GPIO pins
    GPIO.cleanup()
    

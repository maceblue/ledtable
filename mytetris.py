#!/usr/bin/env python3
# Tetris Game with Neopixel Library
# Author: Marcus Mende
# 2018

import time, pygame
from neopixel import *

# LED strip configuration:
LED_COUNT      = 16      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53



# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def initSound():
    #https://bitbucket.org/royassas/rgb-led-table/src/94c420332135e8c4517c17e8c33510e1bac0ffea/TetrisClass.py?at=master&fileviewer=file-view-default
    print("Initialize sound system..."),
    pygame.mixer.pre_init(44100, -16, 2, 2048)    
    pygame.init()
    print("done")
    print("Loading music..."),
    pygame.mixer.music.load('/home/pi/rgbtable/sounds/tetrisaccapella.ogg')
    pygame.mixer.music.set_volume(0.2)
    print("done")
    print("Loading SFX..."),
    snd_click = pygame.mixer.Sound('/home/pi/rgbtable/sounds/click.ogg')
    snd_linekill = pygame.mixer.Sound('/home/pi/rgbtable/sounds/linekill.ogg')
    snd_tilefix = pygame.mixer.Sound('/home/pi/rgbtable/sounds/tilefix.ogg')
    snd_pause = pygame.mixer.Sound('/home/pi/rgbtable/sounds/pause.ogg')
    snd_gameover = pygame.mixer.Sound('/home/pi/rgbtable/sounds/gameover.ogg')
    snd_level = pygame.mixer.Sound('/home/pi/rgbtable/sounds/level.ogg')
    print("done")
    pygame.mixer.music.play(-1)

def initGamepad():
    joystick_count = pygame.joystick.get_count()
    if joystick_count == 0:
        print ("How do you want to play Tetris without a joystick?")
        sys.exit()
    else:
        j = pygame.joystick.Joystick(0)
        j.init()
        print('Initialized Joystick : %s' % j.get_name())

def gameOver():
        print("Game over. "+str(self.Tetris_Points)+" points.")
        pygame.mixer.music.stop()
        self.snd_gameover.play()
        time.sleep(3)
        self.fadeInOut([255,0,0])
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
        sock.sendto(str(self.Tetris_Points), ("192.168.1.19", 56565))
        entry = (self.playerName, self.Tetris_Points)
        self.hiScores.append(entry)
        self.hiScores.sort(key=self.getKey,reverse=True)
        pickle.dump(self.hiScores,open("/home/pi/rgbtable/hiscores.zfl","wb"))

        
# Main program logic follows:
if __name__ == '__main__':
   
    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    try:

        while True:
            print ('Color wipe animations.')
            colorWipe(strip, Color(255, 0, 0))  # Red wipe
            colorWipe(strip, Color(0, 255, 0))  # Blue wipe
            colorWipe(strip, Color(0, 0, 255))  # Green wipe
            
    except KeyboardInterrupt:
        colorWipe(strip, Color(0,0,0), 10)
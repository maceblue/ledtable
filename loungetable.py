import math, sys, time, random, colorsys, pygame, socket
from pygame.locals import *
from colorsys import hsv_to_rgb, rgb_to_hsv
from neopixel import *


# LED strip configuration:
LED_COUNT      = 150      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 55     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

class LoungeTable:
    REFRESHSCREEN = USEREVENT+1
    spidev = file("/dev/spidev0.0", "wb")
    width = 10
    height = 15
    
    def __init__(self,fromColor="000",toColor="000",brightness="1000",waittime="50"):
        self.fromcolor = float(float(fromColor)/360)
        self.tocolor = float(float(toColor)/360)
        self.pixels = [[[0 for x in range(3)] for x in range(self.width)] for x in range(self.height)]
        self.brightness = float(brightness)/1000
        self.waittime = int(waittime)
        self.waitbright = 200
        self.waitint = 100
        self.running = True
        #self.s = s
        self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        # Intialize the library (must be called once before other functions).
        self.strip.begin()
    def hsv2rgb(self,h,s,v):
        return tuple(int(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))
    def rgb2hsv(self,r,g,b):
        return tuple(i  for i in colorsys.rgb_to_hsv(r/ 255.0, g/ 255.0, b/ 255.0))
    # Map a matrix to snake-sequenced LED-Strip
    def matrix2snake(self,x,y):
        if x%2==0:
            pos = (x+1)*self.height - y -1
        else:
            pos = (x*self.height) + y

        return pos
    def send2strip(self):
        for y in range(self.height):
            for x in range(self.width):
                a = int(self.pixels[y][x][0]*self.brightness)
                b = int(self.pixels[y][x][1]*self.brightness)
                c = int(self.pixels[y][x][2]*self.brightness)
                color = Color(a, b, c)
                pos = self.matrix2snake(x,y)
                self.strip.setPixelColor(pos, color)
        self.strip.show()
        time.sleep(0.001)

    def draw(self):
            for row in self.pixels:
                    for pixel in row:
                            for color in pixel:
                                    c = int(color*self.brightness)
                                    self.spidev.write(chr(c & 0xFF))
            self.spidev.flush()
            time.sleep(0.001)
    def initScreen(self):
        for row in range(0,self.height):
            for pixel in range(0,self.width):
                r, g, b = self.hsv2rgb(random.uniform(self.fromcolor,self.tocolor),1,1)
                self.pixels[row][pixel]=[r,g,b]
        self.send2strip()
    def changePixels(self):
        for i in range(0,5):
            row = random.randint(0,self.height-1)
            col = random.randint(0,self.width-1)
            r, g, b = self.hsv2rgb(random.uniform(self.fromcolor,self.tocolor),1,1)
            self.pixels[row][col] = [r,g,b]
        self.send2strip()
    def startTable(self): 
        pygame.quit()
        print("LoungeTable started")
        pygame.init()
        joystick_count = pygame.joystick.get_count()
        if joystick_count == 0:
            print ("Error, I did not find any joysticks")
        else:
            j = pygame.joystick.Joystick(0)
            j.quit()
            j.init()
            print 'Initialized Joystick : %s' % j.get_name()
        self.initScreen()
        pygame.time.set_timer(self.REFRESHSCREEN, self.waittime)
        cl = pygame.time.Clock()
        start = pygame.time.get_ticks()
        startbright = start
        startint = start
        while self.running:
            try:
                #data = self.s.recv(1024)

                #if data.startswith("LOU"):
                    self.fromcolor = float(float(data[3:6])/360)
                    self.tocolor = float(float(data[6:9])/360)
                    self.brightness = float(data[9:13])/1000
                    self.waittime = int(data[13:])
                    print("Parameters updated")
                #elif data=="AbOrTTrObA":
                #    self.running=False
            except: 
                pass
            pygame.event.pump()
            #Check if waitbright-Intervall has passed since last change of brightness and update if buttons pressed
            if (pygame.time.get_ticks()>=startbright+self.waitbright):
                if j.get_axis(1) <= -0.5:
                    if self.brightness <= 0.95:
                        self.brightness +=0.05
                        
                if j.get_axis(1) >= +0.5:
                    if self.brightness >= 0.05:
                        self.brightness -=0.05
                self.send2strip()
                startbright = pygame.time.get_ticks()
                            
            if (pygame.time.get_ticks()>=startint+self.waitint):
                if j.get_axis(0) >= +0.5:
                    if self.waittime <= 9980:
                        self.waittime +=20
                       
                if j.get_axis(0) <= -0.5:
                    if self.waittime >= 20:
                        self.waittime -=20
                startint = pygame.time.get_ticks() 
    
            if j.get_button(1):
                self.waittime = 1
                self.brightness = 1.0
                startint = pygame.time.get_ticks()
                self.changePixels()        
            
            if (pygame.time.get_ticks()>=start+self.waittime):
                self.changePixels()
                start = pygame.time.get_ticks()
        pygame.quit()
        print("LoungeTable closed")
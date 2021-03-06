import pygame, pickle
import math, sys, os, random, socket, time, colorsys
import pyttsx
from pygame.locals import *
from colorsys import hsv_to_rgb, rgb_to_hsv
from copy import deepcopy
from neopixel import *

# LED strip configuration:
LED_COUNT      = 150      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 25     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

class bcolors:
    ANSI_RED = '\033[91m'
    ANSI_GREEN = '\033[92m'
    ANSI_BLUE = '\033[94m'
    ANSI_CYAN= '\033[96m'
    ANSI_WHITE = '\033[97m'
    ANSI_YELLOW = '\033[93m'
    ANSI_MAGENTA = '\033[95m'
    ANSI_GREY = '\033[90m'
    ANSI_BLACK = '\033[90m'
    ENDC = '\033[0m'
    #os.system('cls' if os.name=='nt' else 'clear')
class gamecolors:
    CYAN = [0,255,255]
    BLUE = [0,0,255]
    ORANGE = [255,80,0]
    YELLOW = [255,255,0]
    GREEN = [0,255,0]
    PINK = [255,0,255]
    RED = [255,0,0]
    BLACK = [0,0,0]
    GREY = [40,40,40]
    WHITE = [255,255,255]
    SNAKE_GREEN_1 = [0,255,204] #00ffcc
    SNAKE_GREEN_2 = [0,153,153] #009999
    SNAKE_YELLOW_1 = [255,204,0]
    SNAKE_YELLOW_2 = [102,0,204] # lila
    SNAKE_RED_1 = [204,0,0]
    SNAKE_RED_2 = YELLOW
    SNAKE_BLUE_1 = [0,102,255]
    SNAKE_BLUE_2 = ORANGE
class tiles:
    I_TILE = [[[1,1,1,1]],
              [[1],
               [1],
               [1],
               [1]],
              [[1,1,1,1]],
              [[1],
               [1],
               [1],
               [1]],
              gamecolors.CYAN]
    J_TILE = [[[1,0,0],
               [1,1,1]],
              [[1,1],
               [1,0],
               [1,0]],
              [[1,1,1],
               [0,0,1]],
              [[0,1],
               [0,1],
               [1,1]],
              gamecolors.BLUE]
    L_TILE = [[[0,0,1],
               [1,1,1]],
              [[1,0],
               [1,0],
               [1,1]],
              [[1,1,1],
               [1,0,0]],
              [[1,1],
               [0,1],
               [0,1]],
              gamecolors.YELLOW]
    O_TILE = [[[1,1],
               [1,1]],
              [[1,1],
               [1,1]],
              [[1,1],
               [1,1]],
              [[1,1],
               [1,1]],
              gamecolors.ORANGE]
    S_TILE = [[[0,1,1],
               [1,1,0]],
              [[1,0],
               [1,1],
               [0,1]],
              [[0,1,1],
               [1,1,0]],
              [[1,0],
               [1,1],
               [0,1]],
              gamecolors.GREEN]
    T_TILE = [[[0,1,0],
               [1,1,1]],
              [[1,0],
               [1,1],
               [1,0]],
              [[1,1,1],
               [0,1,0]],
              [[0,1],
               [1,1],
               [0,1]],
              gamecolors.PINK]
    Z_TILE = [[[1,1,0],
               [0,1,1]],
              [[0,1],
               [1,1],
               [1,0]],
              [[1,1,0],
               [0,1,1]],
              [[0,1],
               [1,1],
               [1,0]],
              gamecolors.RED]    
class RGB_Tetris:
    #Variables for all instances of TetrisClass
    width = 10
    height = 15
    hiScores = []
    hiScores_Snake = []
    hiScores_RainbowDrive = []
    snd_click = None
    snd_linekil = None
    snd_tilefix = None
    snd_pause = None
    snd_gameover = None
    snd_level = None
    snd_appluse = None
    snd_rocket = None
    snd_bite = None
    snd_snake_gameover = None
    snd_car_crash = None
    snd_engine = None
    strip = None
    REFRESHSCREEN = USEREVENT+1
    gamepad = None
    
    #Variables per instance of TetrisClass
    def __init__(self,playerName="Anon"):
        self.playerName=playerName
        self.rndSeq = []
        self.activeTet = ""
        self.activeTetCoords=[0,0]
        self.activeTetRotation=0
        self.level=1
        self.linescleared=0
        self.dropPoints=0
        self.fixedPixels = [[gamecolors.BLACK for x in range(self.width)] for x in range(self.height+2)]
        self.movingPixels = [[gamecolors.BLACK for x in range(self.width)] for x in range(self.height+2)]
        self.displayPixels = [[gamecolors.BLACK for x in range(self.width)] for x in range(self.height)]
        self.keyPressTimeout = 125
        self.keyPressTime = 0
        self.keyTimeout = 150
        self.keyTime = 0
        self.moveTimeout = 500
        self.moveTime = 0
        self.brightness = 0.9
        self.Tetris_Points = 0
        self.running = False
        self.paused = False
        self.lastPressed = "NONE"
        self.speakEngine = None
        #lounge modus
        self.fromcolor = float(float("1")/360)
        self.tocolor = float(float("360")/360)
        self.pixels = [[[0 for x in range(3)] for x in range(self.width)] for x in range(self.height)]
        self.waittime = int("250")
        self.waitbright = 200
        self.waitint = 100
        self.loungeTableRunning = False
        #snake game
        self.snakeGameRunning = False
        self.snake = None
        self.snakeDirection = None
        self.cherrySpawned = False
        self.snakeColor = 'green'
        #strip
        self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        # Intialize the library (must be called once before other functions).
        self.strip.begin()
        
    def printMatrix(self,matrix):
        for row in range (0,len(matrix)):
            if row <=9:
                print(" " + str(row) + " ["),
            else:
                print(str(row) + " ["),
            
            for col in range(10):
                if str(matrix[row][col]) =="0" or  str(matrix[row][col]) =="[0, 0, 0]":
                    print(bcolors.ANSI_RED + "X" + bcolors.ENDC),
                else:
                    print (bcolors.ANSI_BLUE + "O" + bcolors.ENDC),
            print("]")

    # Map a matrix to snake-sequenced LED-Strip
    def matrix2snake(self,x,y):
        if x%2==0:
            pos = (x+1)*self.height - y -1
        else:
            pos = (x*self.height) + y

        return pos

    def send2strip(self,matrix):
        for y in range(self.height):
            for x in range(self.width):
                a = int(matrix[y][x][0]*self.brightness)
                b = int(matrix[y][x][1]*self.brightness)
                c = int(matrix[y][x][2]*self.brightness)
                color = Color(a, b, c)
                pos = self.matrix2snake(x,y)
                self.strip.setPixelColor(pos, color)
        self.strip.show()
        time.sleep(0.001)

    def fadeInOut(self,c):
            self.brightness=0
            self.displayPixels = [[c for x in range(self.width)] for x in range(self.height)]
            while self.brightness <1.0:
                    self.send2strip(self.displayPixels)
                    self.brightness+=0.05
            while self.brightness >0.0:
                    self.send2strip(self.displayPixels)
                    self.brightness-=0.05
            self.displayPixels = [[gamecolors.BLACK for x in range(self.width)] for x in range(self.height)]
            self.brightness = 1.0
            self.send2strip(self.displayPixels)

    def countdown(self):
        # number 3
        self.displayPixels = [[gamecolors.BLACK for x in range(self.width)] for x in range(self.height)]
        self.displayPixels[3][3] = gamecolors.RED
        self.displayPixels[3][4] = gamecolors.RED
        self.displayPixels[3][5] = gamecolors.RED
        self.displayPixels[3][6] = gamecolors.RED
        self.displayPixels[4][2] = gamecolors.RED
        self.displayPixels[4][7] = gamecolors.RED
        self.displayPixels[5][7] = gamecolors.RED
        self.displayPixels[6][7] = gamecolors.RED
        self.displayPixels[7][6] = gamecolors.RED
        self.displayPixels[8][7] = gamecolors.RED
        self.displayPixels[9][7] = gamecolors.RED
        self.displayPixels[10][7] = gamecolors.RED
        self.displayPixels[10][2] = gamecolors.RED
        self.displayPixels[11][6] = gamecolors.RED
        self.displayPixels[11][5] = gamecolors.RED
        self.displayPixels[11][4] = gamecolors.RED
        self.displayPixels[11][3] = gamecolors.RED
        self.send2strip(self.displayPixels)
        time.sleep(1)

        # number 2
        self.displayPixels = [[gamecolors.BLACK for x in range(self.width)] for x in range(self.height)]
        self.displayPixels[3][3] = gamecolors.YELLOW
        self.displayPixels[3][4] = gamecolors.YELLOW
        self.displayPixels[3][5] = gamecolors.YELLOW
        self.displayPixels[3][6] = gamecolors.YELLOW
        self.displayPixels[4][2] = gamecolors.YELLOW
        self.displayPixels[4][7] = gamecolors.YELLOW
        self.displayPixels[5][7] = gamecolors.YELLOW
        self.displayPixels[6][7] = gamecolors.YELLOW
        self.displayPixels[7][6] = gamecolors.YELLOW
        self.displayPixels[8][5] = gamecolors.YELLOW
        self.displayPixels[9][4] = gamecolors.YELLOW
        self.displayPixels[10][3] = gamecolors.YELLOW
        self.displayPixels[11][2] = gamecolors.YELLOW
        self.displayPixels[11][3] = gamecolors.YELLOW
        self.displayPixels[11][4] = gamecolors.YELLOW
        self.displayPixels[11][5] = gamecolors.YELLOW
        self.displayPixels[11][6] = gamecolors.YELLOW
        self.displayPixels[11][7] = gamecolors.YELLOW
        self.send2strip(self.displayPixels)
        time.sleep(1)

        # number 1
        self.displayPixels = [[gamecolors.BLACK for x in range(self.width)] for x in range(self.height)]
        self.displayPixels[3][4] = gamecolors.GREEN
        self.displayPixels[3][5] = gamecolors.GREEN
        self.displayPixels[4][3] = gamecolors.GREEN
        self.displayPixels[4][5] = gamecolors.GREEN
        self.displayPixels[5][2] = gamecolors.GREEN
        self.displayPixels[5][5] = gamecolors.GREEN
        self.displayPixels[6][5] = gamecolors.GREEN
        self.displayPixels[7][5] = gamecolors.GREEN
        self.displayPixels[8][5] = gamecolors.GREEN
        self.displayPixels[9][5] = gamecolors.GREEN
        self.displayPixels[10][5] = gamecolors.GREEN
        self.displayPixels[11][5] = gamecolors.GREEN
        self.send2strip(self.displayPixels)
        time.sleep(1)

        self.displayPixels = [[gamecolors.BLACK for x in range(self.width)] for x in range(self.height)]
    
    #Shuffle the next bag of Tetronimos        
    def shuffleSeq(self):
        str_list = [tiles.I_TILE,tiles.O_TILE,tiles.T_TILE,tiles.S_TILE,tiles.Z_TILE,tiles.J_TILE,tiles.L_TILE]
        random.shuffle(str_list)
        return str_list
    #Check if new spawned Tetromino overlaps the current fixedPixels
    def checkSpawn(self):
        tempPixels = [[0 for x in range(self.width)] for x in range(self.height+2)]
        for row in range(len(self.activeTet[self.activeTetRotation])):
            for col in range(len(self.activeTet[self.activeTetRotation][0])):
                if self.activeTet[self.activeTetRotation][row][col]:
                    tempPixels[self.activeTetCoords[0]+row][self.activeTetCoords[1]+col]=1
        for row in range (self.height+2):
            for col in range(self.width):
                if tempPixels[row][col]==1:
                    if self.fixedPixels[row][col]!=gamecolors.BLACK:
                        return True
        return False
    #Spawn a new Tetromino
    def resetGame(self):
        self.rndSeq = []
        self.activeTet = ""
        self.activeTetCoords=[0,0]
        self.activeTetRotation=0
        self.linescleared=0
        self.dropPoints=0
        self.level=1
        self.fixedPixels = [[gamecolors.BLACK for x in range(self.width)] for x in range(self.height+2)]
        self.movingPixels = [[gamecolors.BLACK for x in range(self.width)] for x in range(self.height+2)]
        self.displayPixels = [[gamecolors.BLACK for x in range(self.width)] for x in range(self.height)]
        self.keyPressTimeout = 150
        self.keyPressTime = 0    
        self.keyTimeout = 100
        self.keyTime = 0
        self.moveTimeout = 200
        self.moveTime = 0
        self.brightness = 1.0
        self.Tetris_Points = 0
        self.running = False
        self.paused = False
        self.lastPressed = "NONE"
    def spawn(self):
        if len(self.rndSeq) == 0:
            self.rndSeq = self.shuffleSeq()
        self.activeTet=self.rndSeq[0]
        del self.rndSeq[0]        
        self.activeTetRotation=0
        self.dropPoints=0
        if self.activeTet == tiles.I_TILE:
            self.activeTetCoords=[2,3]
        elif self.activeTet == tiles.J_TILE:
            self.activeTetCoords=[2,3]    
        elif self.activeTet == tiles.L_TILE:
            self.activeTetCoords=[2,3]        
        elif self.activeTet == tiles.O_TILE:
            self.activeTetCoords=[2,4]    
        elif self.activeTet == tiles.S_TILE:
            self.activeTetCoords=[2,3]
        elif self.activeTet == tiles.Z_TILE:
            self.activeTetCoords=[2,3]            
        elif self.activeTet == tiles.T_TILE:
            self.activeTetCoords=[2,3]
        if self.checkSpawn():
            self.gameOver()
            self.resetGame()        
    def checkMoveLeftCollision(self):
        tempPixels = [[0 for x in range(self.width)] for x in range(self.height+2)]
        for row in range(len(self.activeTet[self.activeTetRotation])):
            for col in range(len(self.activeTet[self.activeTetRotation][0])):
                if self.activeTet[self.activeTetRotation][row][col]:
                    tempPixels[self.activeTetCoords[0]+row][self.activeTetCoords[1]+col]=1
        for row in range(self.height+2):
            if tempPixels[row][0]==1:
                return True
        for row in range (self.height+2):
            for col in range(self.width):
                if tempPixels[row][col]==1:
                    if self.fixedPixels[row][col-1]!=gamecolors.BLACK:
                        return True
        return False    
    def checkMoveRightCollision(self):
        tempPixels = [[0 for x in range(self.width)] for x in range(self.height+2)]
        for row in range(len(self.activeTet[self.activeTetRotation])):
            for col in range(len(self.activeTet[self.activeTetRotation][0])):
                if self.activeTet[self.activeTetRotation][row][col]:
                    tempPixels[self.activeTetCoords[0]+row][self.activeTetCoords[1]+col]=1
        for row in range(self.height+2):
            if tempPixels[row][9]==1:
                return True
        for row in range (self.height+2):
            for col in range(self.width):
                if tempPixels[row][col]==1:
                    if self.fixedPixels[row][col+1]!=gamecolors.BLACK:
                        return True
        return False
    def moveRight(self):
        self.activeTetCoords[1]+=1
        self.snd_click.play()    
    def moveLeft(self):
        self.activeTetCoords[1]-=1
        self.snd_click.play()    
    #Player is gameover
    def gameOver(self):
        print("Game over. "+str(self.Tetris_Points)+" points.")
        pygame.mixer.music.stop()
        self.snd_gameover.play()
        time.sleep(1)
        self.speakEngine = None
        self.speakEngine = pyttsx.init()
        rate = self.speakEngine.getProperty('rate')
        #self.speakEngine.setProperty('rate', rate-10)
        self.speakEngine.setProperty('voice', 'german')
        self.speakEngine.say("Du hast "+str(self.Tetris_Points)+" Punkte.")
        if self.hiScores[0][1] < self.Tetris_Points:
            entry = (self.playerName, self.Tetris_Points)
            self.hiScores.append(entry)
            self.hiScores.sort(key=self.getKey,reverse=True)
            pickle.dump(self.hiScores,open("/home/pi/ledtable/hiscores.zfl","wb"))
            self.speakEngine.say("Du hast einen neuen Rekord aufgestellt.")
            self.speakEngine.runAndWait()
            self.snd_appluse.play()
            time.sleep(6)
            self.snd_rocket.play()
            time.sleep(10)
        else:
            self.speakEngine.say("Der Rekord liegt bei "+str(self.hiScores[0][1])+" Punkten.")
            self.speakEngine.runAndWait()
        self.fadeInOut([255,0,0])
            
    #Teil nach links drehen
    def rotateLeft(self):
        if self.activeTet == tiles.I_TILE:
            validMove = True
            if self.activeTetRotation == 0:
                tempPixels = [[0 for x in range(self.width)] for x in range(self.height+2)]
                if self.activeTetCoords[0]>19:
                    validMove=False    
                else:
                    for row in range(len(self.activeTet[3])):
                        for col in range(len(self.activeTet[3][0])):
                            if self.activeTet[3][row][col]:
                                tempPixels[self.activeTetCoords[0]-1+row][self.activeTetCoords[1]+1+col]=1
                    for row in range (self.height+2):
                        for col in range(self.width):
                            if tempPixels[row][col]==1:
                                if self.fixedPixels[row][col]!=gamecolors.BLACK:
                                    validMove = False                        
                if validMove:
                    self.activeTetRotation =3
                    self.activeTetCoords[1]+=1    
                    self.activeTetCoords[0]-=1        
            elif self.activeTetRotation == 3:
                tempPixels = [[0 for x in range(self.width)] for x in range(self.height+2)]
                if self.activeTetCoords[1]<1 or self.activeTetCoords[1]>7:
                    validMove=False        
                else:
                    for row in range(len(self.activeTet[2])):
                        for col in range(len(self.activeTet[2][0])):
                            if self.activeTet[2][row][col]:
                                tempPixels[self.activeTetCoords[0]+2+row][self.activeTetCoords[1]-1+col]=1
                    for row in range (self.height+2):
                        for col in range(self.width):
                            if tempPixels[row][col]==1:
                                if self.fixedPixels[row][col]!=gamecolors.BLACK:
                                    validMove = False                        
                if validMove:
                    self.activeTetRotation =2
                    self.activeTetCoords[1]-=1    
                    self.activeTetCoords[0]+=2            
            elif self.activeTetRotation == 2:
                tempPixels = [[0 for x in range(self.width)] for x in range(self.height+2)]
                if self.activeTetCoords[0]>self.height+2:
                    validMove=False    
                else:
                    for row in range(len(self.activeTet[1])):
                        for col in range(len(self.activeTet[1][0])):
                            if self.activeTet[1][row][col]:
                                tempPixels[self.activeTetCoords[0]-2+row][self.activeTetCoords[1]+2+col]=1
                    for row in range (self.height+2):
                        for col in range(self.width):
                            if tempPixels[row][col]==1:
                                if self.fixedPixels[row][col]!=gamecolors.BLACK:
                                    validMove = False                
                if validMove:
                    self.activeTetRotation =1
                    self.activeTetCoords[1]+=2    
                    self.activeTetCoords[0]-=2        
            elif self.activeTetRotation == 1:
                tempPixels = [[0 for x in range(self.width)] for x in range(self.height+2)]
                if self.activeTetCoords[1]<2 or self.activeTetCoords[1]>8:
                    validMove=False    
                else:
                    for row in range(len(self.activeTet[0])):
                        for col in range(len(self.activeTet[0][0])):
                            if self.activeTet[0][row][col]:
                                tempPixels[self.activeTetCoords[0]+1+row][self.activeTetCoords[1]-2+col]=1
                    for row in range (self.height+2):
                        for col in range(self.width):
                            if tempPixels[row][col]==1:
                                if self.fixedPixels[row][col]!=gamecolors.BLACK:
                                    validMove = False
                if validMove:
                    self.activeTetRotation =0
                    self.activeTetCoords[1]-=2    
                    self.activeTetCoords[0]+=1            
        elif self.activeTet == tiles.J_TILE or self.activeTet == tiles.L_TILE or self.activeTet == tiles.S_TILE or self.activeTet == tiles.T_TILE or self.activeTet == tiles.Z_TILE:
            validMove = True
            if self.activeTetRotation == 0:
                tempPixels = [[0 for x in range(self.width)] for x in range(self.height+2)]
                if self.activeTetCoords[0]>self.height-1:
                    validMove=False    
                else:
                    for row in range(len(self.activeTet[3])):
                        for col in range(len(self.activeTet[3][0])):
                            if self.activeTet[3][row][col]:
                                tempPixels[self.activeTetCoords[0]+row][self.activeTetCoords[1]+col]=1
                    for row in range (self.height+2):
                        for col in range(self.width):
                            if tempPixels[row][col]==1:
                                if self.fixedPixels[row][col]!=gamecolors.BLACK:
                                    validMove = False                        
                if validMove:
                    self.activeTetRotation =3
                    self.activeTetCoords[1]+=0    
                    self.activeTetCoords[0]-=0        
            elif self.activeTetRotation == 3:
                tempPixels = [[0 for x in range(self.width)] for x in range(self.height+2)]
                if self.activeTetCoords[1]>7:
                    validMove=False        
                else:
                    for row in range(len(self.activeTet[2])):
                        for col in range(len(self.activeTet[2][0])):
                            if self.activeTet[2][row][col]:
                                tempPixels[self.activeTetCoords[0]+1+row][self.activeTetCoords[1]+col]=1
                    for row in range (self.height+2):
                        for col in range(self.width):
                            if tempPixels[row][col]==1:
                                if self.fixedPixels[row][col]!=gamecolors.BLACK:
                                    validMove = False                        
                if validMove:
                    self.activeTetRotation =2
                    self.activeTetCoords[1]-=0    
                    self.activeTetCoords[0]+=1            
            elif self.activeTetRotation == 2:
                tempPixels = [[0 for x in range(self.width)] for x in range(self.height+2)]
                if self.activeTetCoords[0]>self.height:
                    validMove=False    
                else:
                    for row in range(len(self.activeTet[1])):
                        for col in range(len(self.activeTet[1][0])):
                            if self.activeTet[1][row][col]:
                                tempPixels[self.activeTetCoords[0]-1+row][self.activeTetCoords[1]+1+col]=1
                    for row in range (self.height+2):
                        for col in range(self.width):
                            if tempPixels[row][col]==1:
                                if self.fixedPixels[row][col]!=gamecolors.BLACK:
                                    validMove = False                
                if validMove:
                    self.activeTetRotation =1
                    self.activeTetCoords[1]+=1    
                    self.activeTetCoords[0]-=1        
            elif self.activeTetRotation == 1:
                tempPixels = [[0 for x in range(self.width)] for x in range(self.height+2)]
                if self.activeTetCoords[1]<1:
                    validMove=False    
                else:
                    for row in range(len(self.activeTet[0])):
                        for col in range(len(self.activeTet[0][0])):
                            if self.activeTet[0][row][col]:
                                tempPixels[self.activeTetCoords[0]+0+row][self.activeTetCoords[1]-1+col]=1
                    for row in range (self.height+2):
                        for col in range(self.width):
                            if tempPixels[row][col]==1:
                                if self.fixedPixels[row][col]!=gamecolors.BLACK:
                                    validMove = False
                if validMove:
                    self.activeTetRotation =0
                    self.activeTetCoords[1]-=1    
                    self.activeTetCoords[0]+=0            
        elif self.activeTet == tiles.O_TILE:
            return False
        self.snd_click.play()    
    #Teil nach rechts drehen
    def rotateRight(self):
        global fixedPixels,activeTet,activeTetCoords,activeTetRotation
        if self.activeTet == tiles.I_TILE:
            validMove = True
            if self.activeTetRotation == 0:
                tempPixels = [[0 for x in range(self.width)] for x in range(self.height+2)]
                if self.activeTetCoords[0]>self.height-1:
                    validMove=False    
                else:
                    for row in range(len(self.activeTet[1])):
                        for col in range(len(self.activeTet[1][0])):
                            if self.activeTet[1][row][col]:
                                tempPixels[self.activeTetCoords[0]-1+row][self.activeTetCoords[1]+2+col]=1
                    for row in range (self.height+2):
                        for col in range(self.width):
                            if tempPixels[row][col]==1:
                                if self.fixedPixels[row][col]!=gamecolors.BLACK:
                                    validMove = False                        
                if validMove:
                    self.activeTetRotation =1
                    self.activeTetCoords[1]+=2    
                    self.activeTetCoords[0]-=1        
            elif self.activeTetRotation == 1:
                tempPixels = [[0 for x in range(self.width)] for x in range(self.height+2)]
                if self.activeTetCoords[1]<2 or self.activeTetCoords[1]>8:
                    validMove=False        
                else:
                    for row in range(len(self.activeTet[2])):
                        for col in range(len(self.activeTet[2][0])):
                            if self.activeTet[2][row][col]:
                                tempPixels[self.activeTetCoords[0]+2+row][self.activeTetCoords[1]-2+col]=1
                    for row in range (self.height+2):
                        for col in range(self.width):
                            if tempPixels[row][col]==1:
                                if self.fixedPixels[row][col]!=gamecolors.BLACK:
                                    validMove = False                        
                if validMove:
                    self.activeTetRotation =2
                    self.activeTetCoords[1]-=2    
                    self.activeTetCoords[0]+=2            
            elif self.activeTetRotation == 2:
                tempPixels = [[0 for x in range(self.width)] for x in range(self.height+2)]
                if self.activeTetCoords[0]>self.height:
                    validMove=False    
                else:
                    for row in range(len(self.activeTet[3])):
                        for col in range(len(self.activeTet[3][0])):
                            if self.activeTet[3][row][col]:
                                tempPixels[self.activeTetCoords[0]-2+row][self.activeTetCoords[1]+1+col]=1
                    for row in range (self.height+2):
                        for col in range(self.width):
                            if tempPixels[row][col]==1:
                                if self.fixedPixels[row][col]!=gamecolors.BLACK:
                                    validMove = False                
                if validMove:
                    self.activeTetRotation =3
                    self.activeTetCoords[1]+=1    
                    self.activeTetCoords[0]-=2        
            elif self.activeTetRotation == 3:
                tempPixels = [[0 for x in range(self.width)] for x in range(self.height+2)]
                if self.activeTetCoords[1]<1 or self.activeTetCoords[1]>7:
                    validMove=False    
                else:
                    for row in range(len(self.activeTet[0])):
                        for col in range(len(self.activeTet[0][0])):
                            if self.activeTet[0][row][col]:
                                tempPixels[self.activeTetCoords[0]+1+row][self.activeTetCoords[1]-1+col]=1
                    for row in range (self.height+2):
                        for col in range(self.width):
                            if tempPixels[row][col]==1:
                                if self.fixedPixels[row][col]!=gamecolors.BLACK:
                                    validMove = False
                if validMove:
                    self.activeTetRotation =0
                    self.activeTetCoords[1]-=1    
                    self.activeTetCoords[0]+=1            
        elif self.activeTet == tiles.J_TILE or self.activeTet == tiles.L_TILE or self.activeTet == tiles.S_TILE or self.activeTet == tiles.T_TILE or self.activeTet == tiles.Z_TILE:
            validMove = True
            if self.activeTetRotation == 0:
                tempPixels = [[0 for x in range(self.width)] for x in range(self.height+2)]
                if self.activeTetCoords[0]>self.height-1:
                    validMove=False    
                else:
                    for row in range(len(self.activeTet[1])):
                        for col in range(len(self.activeTet[1][0])):
                            if self.activeTet[1][row][col]:
                                tempPixels[self.activeTetCoords[0]+row][self.activeTetCoords[1]+1+col]=1
                    for row in range (self.height+2):
                        for col in range(self.width):
                            if tempPixels[row][col]==1:
                                if self.fixedPixels[row][col]!=gamecolors.BLACK:
                                    validMove = False                        
                if validMove:
                    self.activeTetRotation =1
                    self.activeTetCoords[1]+=1    
                    self.activeTetCoords[0]-=0        
            elif self.activeTetRotation == 1:
                tempPixels = [[0 for x in range(self.width)] for x in range(self.height+2)]
                if self.activeTetCoords[1]<1:
                    validMove=False        
                else:
                    for row in range(len(self.activeTet[2])):
                        for col in range(len(self.activeTet[2][0])):
                            if self.activeTet[2][row][col]:
                                tempPixels[self.activeTetCoords[0]+1+row][self.activeTetCoords[1]-1+col]=1
                    for row in range (self.height+2):
                        for col in range(self.width):
                            if tempPixels[row][col]==1:
                                if self.fixedPixels[row][col]!=gamecolors.BLACK:
                                    validMove = False                        
                if validMove:
                    self.activeTetRotation =2
                    self.activeTetCoords[1]-=1    
                    self.activeTetCoords[0]+=1            
            elif self.activeTetRotation == 2:
                tempPixels = [[0 for x in range(self.width)] for x in range(self.height+2)]
                if self.activeTetCoords[0]>self.height:
                    validMove=False    
                else:
                    for row in range(len(self.activeTet[3])):
                        for col in range(len(self.activeTet[3][0])):
                            if self.activeTet[3][row][col]:
                                tempPixels[self.activeTetCoords[0]-1+row][self.activeTetCoords[1]+col]=1
                    for row in range (self.height+2):
                        for col in range(self.width):
                            if tempPixels[row][col]==1:
                                if self.fixedPixels[row][col]!=gamecolors.BLACK:
                                    validMove = False                
                if validMove:
                    self.activeTetRotation =3
                    self.activeTetCoords[1]+=0    
                    self.activeTetCoords[0]-=1        
            elif self.activeTetRotation == 3:
                tempPixels = [[0 for x in range(self.width)] for x in range(self.height+2)]
                if self.activeTetCoords[1]>7:
                    validMove=False    
                else:
                    for row in range(len(self.activeTet[0])):
                        for col in range(len(self.activeTet[0][0])):
                            if self.activeTet[0][row][col]:
                                tempPixels[self.activeTetCoords[0]+row][self.activeTetCoords[1]+col]=1
                    for row in range (self.height+2):
                        for col in range(self.width):
                            if tempPixels[row][col]==1:
                                if self.fixedPixels[row][col]!=gamecolors.BLACK:
                                    validMove = False
                if validMove:
                    self.activeTetRotation =0
                    self.activeTetCoords[1]-=0    
                    self.activeTetCoords[0]+=0
        elif self.activeTet == tiles.O_TILE:
            return False
        self.snd_click.play()
    #Process inputs
    def keyAction(self): 
        if self.lastPressed == "UP":
            self.dropDown()
        if self.lastPressed == "DOWN":
            self.moveDown()
            self.keyPressTime = pygame.time.get_ticks()
        if self.lastPressed == "RIGHT":
            if not self.checkMoveRightCollision():
                self.moveRight()
                self.keyPressTime = pygame.time.get_ticks()
        if self.lastPressed == "LEFT":
            if not self.checkMoveLeftCollision():
                self.moveLeft()
                self.keyPressTime = pygame.time.get_ticks()
        if self.lastPressed == "A":
            self.rotateRight()
            self.keyPressTime = pygame.time.get_ticks()
        if self.lastPressed == "B":
            self.rotateLeft()
            self.keyPressTime = pygame.time.get_ticks()
        if self.lastPressed == "SELECT":
            print("Button 8 - Select button")
        if self.lastPressed == "START":
            print ("Game paused")
            self.paused = True
            pygame.mixer.music.pause()
            self.snd_pause.play()
        self.buildScreen()
        self.lastPressed ="NONE"
    def checkMoveDownCollision(self):
        tempPixels = [[0 for x in range(self.width)] for x in range(self.height+3)]
        for row in range(len(self.activeTet[self.activeTetRotation])):
            for col in range(len(self.activeTet[self.activeTetRotation][0])):
                if self.activeTet[self.activeTetRotation][row][col]:
                    tempPixels[self.activeTetCoords[0]+1+row][self.activeTetCoords[1]+col]=1
        for col in range(0,self.width):
            if tempPixels[self.height+2][col]==1:
                return True    
        for row in range (self.height+2):
            for col in range(self.width):
                if tempPixels[row][col]==1:
                    if self.fixedPixels[row][col]!=gamecolors.BLACK:
                        return True
        return False
    def setLevelAndSpeed(self):
        prelevel = self.level
        if self.linescleared<=0:
            self.level=1
        elif self.linescleared>=1 and self.linescleared <=90:
            self.level = 1 + ((self.linescleared - 1) / 10)
        elif self.linescleared>=91:
            self.level = 10
            
        if self.level > prelevel:
            self.snd_level.play()
        self.moveTimeout = (((11 - self.level) * 50))
        #print("Abgeraeumte Linien: "+str(self.linescleared)+" - Level: "+str(self.level)+" - moveTime: "+str(self.moveTimeout)+" - Tetris Points: "+str(self.Tetris_Points))
    def checkFinishedLines(self):
        linesFinished = 0
        for row in range(self.height+2):
            counter = 0
            for col in range(self.width):
                if self.fixedPixels[row][col]!=gamecolors.BLACK:
                    counter+=1
            if counter == 10:
                linesFinished +=1
                for col in range(self.width):
                    self.fixedPixels[row][col]=gamecolors.BLACK
                self.buildScreen()
                for mrow in range(row,0,-1):
                    for mcol in range(self.width):
                        self.fixedPixels[mrow][mcol]=self.fixedPixels[mrow-1][mcol]
                self.snd_linekill.play()
                self.buildScreen()
                
        if linesFinished==1:
            self.Tetris_Points += 40*self.level
        elif linesFinished==2:
            self.Tetris_Points+= 100*self.level
        elif linesFinished==3:
            self.Tetris_Points+= 300*self.level
        elif linesFinished==4:
            self.Tetris_Points+=1200*self.level
            
        self.linescleared+=linesFinished
        self.setLevelAndSpeed()
    def fixTile(self):
        for row in range(len(self.activeTet[self.activeTetRotation])):
            for col in range(len(self.activeTet[self.activeTetRotation][0])):
                if self.activeTet[self.activeTetRotation][row][col]:
                    self.fixedPixels[self.activeTetCoords[0]+row][self.activeTetCoords[1]+col]=self.activeTet[4]
        self.activeTet=None
        self.checkFinishedLines()
        self.snd_tilefix.play()
        time.sleep(self.moveTimeout/1000.0)
        self.Tetris_Points += ( (21 + (3 * self.level)) - self.dropPoints )
        self.spawn()
        if self.running:
            self.buildScreen()
        self.moveTime = pygame.time.get_ticks()
    def dropDown(self):
        while not self.checkMoveDownCollision():
            self.activeTetCoords[0]+=1
            self.keyTime = pygame.time.get_ticks()
            self.moveTime = pygame.time.get_ticks()
            self.buildScreen()
        self.fixTile()
    #Let gravity pull the mobile pixels down
    def timeAction(self):
        if self.checkMoveDownCollision():
            self.fixTile()
        else:
            self.activeTetCoords[0]+=1
            self.dropPoints+=1
    def moveDown(self):
        if self.checkMoveDownCollision():
            self.fixTile()
        else:
            self.activeTetCoords[0]+=1
            self.dropPoints+=1
    def getKeypress(self,u):
        pygame.event.pump()
        # if u.get_button(0):
        #     print("0")
        # if u.get_button(1):
        #     print("1")
        # if u.get_button(2):
        #     print("2")
        # if u.get_button(3):
        #     print("3")
        # if u.get_button(4):
        #     print("4")
        # if u.get_button(5):
        #     print("5")
        # if u.get_button(6):
        #     print("6")
        # if u.get_button(7):
        #     print("7")
        # if u.get_button(8):
        #     print("8")
        # if u.get_button(9):
        #     print("9")
        if u.get_axis(1) <= -0.5: #D-Pad nach oben
            self.lastPressed = "UP"    
        if u.get_axis(1) >= +0.5: #D-Pad nach unten
            self.lastPressed = "DOWN"    
        if u.get_axis(0) >= +0.5: #D-Pad rechts
            self.lastPressed = "RIGHT"
        if u.get_axis(0) <= -0.5: #D-Pad nach links
            self.lastPressed = "LEFT"
        if u.get_button(1): #Button A - right red button 
            self.lastPressed = "A"
        if u.get_button(2): #Button B - left yellow button 
            self.lastPressed = "B"
        if u.get_button(0): #Button X - right blue button 
            self.lastPressed = "X"
        if u.get_button(3): #Button Y - left green button 
            self.lastPressed = "Y"
        if u.get_button(8):
            self.lastPressed = "SELECT"
        if u.get_button(9):
            self.lastPressed = "START"    
        if u.get_button(5): # right top button
            self.lastPressed = "TOPRIGHT"
            musicVol = pygame.mixer.music.get_volume()
            pygame.mixer.music.set_volume(musicVol+0.1)
            clickVol = self.snd_click.get_volume()
            self.snd_click.set_volume(clickVol+0.1)
            linekillVol = self.snd_linekill.get_volume()
            self.snd_linekill.set_volume(linekillVol+0.1)
            tilefixVol = self.snd_tilefix.get_volume()
            self.snd_tilefix.set_volume(tilefixVol+0.1)
            pauseVol = self.snd_pause.get_volume()
            self.snd_pause.set_volume(pauseVol+0.1)
            gameoverVol = self.snd_gameover.get_volume()
            self.snd_gameover.set_volume(gameoverVol+0.1)
            levelVol = self.snd_level.get_volume()
            self.snd_level.set_volume(levelVol+0.1)
            levelBite = self.snd_bite.get_volume()
            self.snd_bite.set_volume(levelBite+0.1)
            levelSnakeGameOver = self.snd_snake_gameover.get_volume()
            self.snd_snake_gameover.set_volume(levelSnakeGameOver+0.1)
            volume = self.speakEngine.getProperty('volume')
            self.speakEngine.setProperty('volume',volume+0.1)
            levelApplause = self.snd_appluse.get_volume()
            self.snd_appluse.set_volume(levelApplause+0.1)
            levelRocket = self.snd_rocket.get_volume()
            self.snd_rocket.set_volume(levelRocket+0.1)
            levelEngine = self.snd_engine.get_volume()
            self.snd_engine.set_volume(levelEngine+0.1)
            levelCarCrash = self.snd_car_crash.get_volume()
            self.snd_car_crash.set_volume(levelCarCrash+0.1)
        if u.get_button(4): # left top button
            self.lastPressed = "TOPLEFT"
            musicVol = pygame.mixer.music.get_volume()
            pygame.mixer.music.set_volume(musicVol-0.05)
            clickVol = self.snd_click.get_volume()
            self.snd_click.set_volume(clickVol-0.1)
            linekillVol = self.snd_linekill.get_volume()
            self.snd_linekill.set_volume(linekillVol-0.1)
            tilefixVol = self.snd_tilefix.get_volume()
            self.snd_tilefix.set_volume(tilefixVol-0.1)
            pauseVol = self.snd_pause.get_volume()
            self.snd_pause.set_volume(pauseVol-0.1)
            gameoverVol = self.snd_gameover.get_volume()
            self.snd_gameover.set_volume(gameoverVol-0.1)
            levelVol = self.snd_level.get_volume()
            self.snd_level.set_volume(levelVol-0.1)
            levelBite = self.snd_bite.get_volume()
            self.snd_bite.set_volume(levelBite-0.1)
            levelSnakeGameOver = self.snd_snake_gameover.get_volume()
            self.snd_snake_gameover.set_volume(levelSnakeGameOver-0.1)
            volume = self.speakEngine.getProperty('volume')
            self.speakEngine.setProperty('volume',volume-0.1)
            levelApplause = self.snd_appluse.get_volume()
            self.snd_appluse.set_volume(levelApplause-0.1)
            levelRocket = self.snd_rocket.get_volume()
            self.snd_rocket.set_volume(levelRocket-0.1)
            levelEngine = self.snd_engine.get_volume()
            self.snd_engine.set_volume(levelEngine-0.1)
            levelCarCrash = self.snd_car_crash.get_volume()
            self.snd_car_crash.set_volume(levelCarCrash-0.1)
    #Overlay fixed and mobile Pixels
    def buildScreen(self):
        if self.running:
            for row in range(self.height):
                for pixel in range(self.width):
                    self.displayPixels[row][pixel]=self.fixedPixels[row+2][pixel]
            if self.activeTet != None:
                for row in range(len(self.activeTet[self.activeTetRotation])):
                    for col in range(len(self.activeTet[self.activeTetRotation][0])):
                        if self.activeTet[self.activeTetRotation][row][col]:
                            self.displayPixels[self.activeTetCoords[0]-2+row][self.activeTetCoords[1]+col]=self.activeTet[4]
            self.send2strip(self.displayPixels)
    def getKey(self,item):
        return item[1]  
    def startTable(self):
        print("Initialize sound system..."),
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        self.lastPressed = None
        self.paused = False
        pygame.init()
        print("done")
        print("Loading music..."),
        pygame.mixer.music.load('/home/pi/ledtable/sounds/tetrisaccapella.ogg')
        pygame.mixer.music.set_volume(0.2)
        print("done")
        print("Loading SFX..."),
        self.snd_click = pygame.mixer.Sound('/home/pi/ledtable/sounds/click.ogg')
        self.snd_linekill = pygame.mixer.Sound('/home/pi/ledtable/sounds/linekill.ogg')
        self.snd_tilefix = pygame.mixer.Sound('/home/pi/ledtable/sounds/tilefix.ogg')
        self.snd_pause = pygame.mixer.Sound('/home/pi/ledtable/sounds/pause.ogg')
        self.snd_gameover = pygame.mixer.Sound('/home/pi/ledtable/sounds/gameover.ogg')
        self.snd_level = pygame.mixer.Sound('/home/pi/ledtable/sounds/level.ogg')
        self.snd_appluse = pygame.mixer.Sound('/home/pi/ledtable/sounds/applause.ogg')
        self.snd_rocket = pygame.mixer.Sound('/home/pi/ledtable/sounds/rocket-start.ogg')
        self.snd_bite = pygame.mixer.Sound('/home/pi/ledtable/sounds/bite.ogg')
        self.snd_snake_gameover = pygame.mixer.Sound('/home/pi/ledtable/sounds/snake_gameover.ogg')
        self.snd_car_crash = pygame.mixer.Sound('/home/pi/ledtable/sounds/car-crash.ogg')
        self.snd_engine = pygame.mixer.Sound('/home/pi/ledtable/sounds/diesel-engine.ogg')
        print("done")
        print("Loading self.speakEngine...")
        self.speakEngine = pyttsx.init()
        rate = self.speakEngine.getProperty('rate')
        #self.speakEngine.setProperty('rate', rate-10)
        self.speakEngine.setProperty('voice', 'german')
        print("done")
        print("Loading Gamepad...")
        joystick_count = pygame.joystick.get_count()
        if joystick_count == 0:
            print ("How do you want to play Tetris without a joystick?")
            sys.exit()
        else:
            self.gamepad = pygame.joystick.Joystick(0)
            self.gamepad.init()
            print('Initialized Joystick : %s' % self.gamepad.get_name())
        print("done")
        self.startLoungeTable()
    def startTetris(self):
        pygame.mixer.music.play(-1)
        print("Loading Hiscores..."),
        self.hiScores = pickle.load(open("/home/pi/ledtable/hiscores.zfl","rb"))
        self.hiScores.sort(key=self.getKey,reverse=True)
        print("done")
        print("Aktueller Hiscore: "+str(self.hiScores[0][1])+" Punkte von "+str(self.hiScores[0][0]))
        print("Hi "+self.playerName+", good luck!")
        print("Game of Tetris started!")
        self.countdown()
        self.running = True
        self.spawn()
        self.moveTime = pygame.time.get_ticks()
        self.keyTime = self.moveTime
        self.keyPressTime = self.moveTime
        while self.running:
            if self.paused:
                time.sleep(1)
                while self.paused:
                    pygame.event.pump()
                    if self.gamepad.get_button(9):
                        print ("Game unpaused")
                        self.snd_pause.play()
                        pygame.mixer.music.unpause()
                        time.sleep(1)
                        self.paused = False
                        self.lastPressed="NONE"
            
            if self.running:
                if pygame.time.get_ticks() > self.keyPressTime + self.keyPressTimeout:
                     self.getKeypress(self.gamepad)
                if pygame.time.get_ticks() > self.keyTime + self.keyTimeout:
                     self.keyAction()
                     self.keyTime = pygame.time.get_ticks()
                if pygame.time.get_ticks() > self.moveTime + self.moveTimeout:
                    self.timeAction()
                    self.moveTime = pygame.time.get_ticks()
            if self.running:
                self.buildScreen()
        
        print("Tetris ended.")
        self.startLoungeTable()

    # lounge modus functions
    def hsv2rgb(self,h,s,v):
        return tuple(int(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))
    def rgb2hsv(self,r,g,b):
        return tuple(i  for i in colorsys.rgb_to_hsv(r/ 255.0, g/ 255.0, b/ 255.0))
    def initLoungeScreen(self):
        for row in range(0,self.height):
            for pixel in range(0,self.width):
                r, g, b = self.hsv2rgb(random.uniform(self.fromcolor,self.tocolor),1,1)
                self.pixels[row][pixel]=[r,g,b]
        self.send2strip(self.pixels)
    def changePixels(self):
        for i in range(0,5):
            row = random.randint(0,self.height-1)
            col = random.randint(0,self.width-1)
            r, g, b = self.hsv2rgb(random.uniform(self.fromcolor,self.tocolor),1,1)
            self.pixels[row][col] = [r,g,b]
        self.send2strip(self.pixels)
    def startLoungeTable(self): 
        self.loungeTableRunning = True
        print("LoungeTable started")
        self.brightness = 0.5
        self.initLoungeScreen()
        pygame.time.set_timer(self.REFRESHSCREEN, self.waittime)
        cl = pygame.time.Clock()
        start = pygame.time.get_ticks()
        startbright = start
        startint = start
        countdown_shutdown = 0
        while self.loungeTableRunning:
            pygame.event.pump()
            #Check if waitbright-Intervall has passed since last change of brightness and update if buttons pressed
            if (pygame.time.get_ticks()>=startbright+self.waitbright):
                if self.gamepad.get_axis(1) <= -0.5:
                    if self.brightness <= 0.95:
                        self.brightness +=0.05
                        
                if self.gamepad.get_axis(1) >= +0.5:
                    if self.brightness >= 0.05:
                        self.brightness -=0.05
                self.send2strip(self.pixels)
                startbright = pygame.time.get_ticks()

                            
            if (pygame.time.get_ticks()>=startint+self.waitint):
                if self.gamepad.get_axis(0) >= +0.5:
                    if self.waittime <= 9980:
                        self.waittime +=20
                       
                if self.gamepad.get_axis(0) <= -0.5:
                    if self.waittime >= 20:
                        self.waittime -=20
                startint = pygame.time.get_ticks() 
    
            #if self.gamepad.get_button(1):
                #self.waittime = 1
                #self.brightness = 1.0
                #startint = pygame.time.get_ticks()
                #self.changePixels()        
            
            if (pygame.time.get_ticks()>=start+self.waittime):
                self.changePixels()
                store_pressed = self.lastPressed
                self.getKeypress(self.gamepad)
                if store_pressed == 'X' and self.lastPressed == 'X':
                    countdown_shutdown += 1
                    self.lastPressed = 'None'
                else:
                    countdown_shutdown = 0

                start = pygame.time.get_ticks()
           
            self.getKeypress(self.gamepad)
            
            if countdown_shutdown == 5:
                print('')
                print('!!!!!!!! S.H.U.T.D.O.W.N !!!!!!!!!')
                self.fadeInOut([0,0,0])
                time.sleep(5)
                self.brightness = 0
                os.system("shutdown -h now")
            

            if self.lastPressed == 'START':
                self.loungeTableRunning = False
                self.lastPressed = None
                self.paused = False
                self.brightness = 0.5
                self.startTetris()
            if self.lastPressed == 'SELECT':
                self.loungeTableRunning = False
                self.lastPressed = None
                self.paused = False
                self.brightness = 0.5
                self.startSnakeGame()
            if self.lastPressed == 'B':
                self.loungeTableRunning = False
                self.lastPressed = None
                self.paused = False
                self.brightness = 0.5
                self.startRainbowDrive()

####################################################################################
################################### Snake-Game #####################################
####################################################################################

    def startSnakeGame(self):
        print("startSnakeGame")
        self.snakeGameRunning = True
        self.snakePoints = 0
        #coords are [y,x] NOT [x,y] !!!
        self.snake = [[5,0],[4,0],[3,0],[2,0],[1,0]]
        self.snakeDirection = "DOWN"
        self.waittime = 250

        print("Loading Hiscores..."),
        self.hiScores_Snake = pickle.load(open("/home/pi/ledtable/hiscores_snake.zfl","rb"))
        self.hiScores_Snake.sort(key=self.getKey,reverse=True)
        print("done")

        joystick_count = pygame.joystick.get_count()
        if joystick_count == 0:
            print ("How do you want to play Snake without a joystick?")
            sys.exit()
        else:
            self.gamepad = pygame.joystick.Joystick(0)
            self.gamepad.init()
            
        self.moveTime = pygame.time.get_ticks()
        self.keyTime = self.moveTime
        self.keyPressTime = self.moveTime

        start = 0

        while self.snakeGameRunning:
            pygame.event.pump()
            if pygame.time.get_ticks() > self.keyPressTime + self.keyPressTimeout:
                self.getKeypress(self.gamepad)
            #self.getKeypress(self.gamepad)
            if self.lastPressed == "UP" and self.snakeDirection != "DOWN":
                self.snakeDirection = "UP"
            if self.lastPressed == "DOWN" and self.snakeDirection != "UP":
                self.snakeDirection = "DOWN"
            if self.lastPressed == "LEFT" and self.snakeDirection != "RIGHT":
                self.snakeDirection = "LEFT"
            if self.lastPressed == "RIGHT" and self.snakeDirection != "LEFT":
                self.snakeDirection = "RIGHT"

            if self.lastPressed == "A":
                self.snakeColor = "red"
            if self.lastPressed == "B":
                self.snakeColor = "yellow"
            if self.lastPressed == "X":
                self.snakeColor = "blue"
            if self.lastPressed == "Y":
                self.snakeColor = "green"

            if self.cherrySpawned == False:
                self.spawnCherry()

            if (pygame.time.get_ticks()>=start+self.waittime):
                self.moveSnake()
                self.buildSnakeScreen()
                start = pygame.time.get_ticks()
            

    def moveSnake(self):
        #print("moveSnake")
        new_snake = deepcopy(self.snake)
        for index in range(0,len(self.snake)):
            if index == 0:
                if self.snakeDirection == "UP":
                    if self.snake[index][0] == 0:
                        new_snake[index][0] = self.height-1
                    else:
                        new_snake[index][0] -= 1
                if self.snakeDirection == "DOWN":
                    if self.snake[index][0] == self.height-1:
                        new_snake[index][0] = 0
                    else:
                        new_snake[index][0] += 1
                if self.snakeDirection == "LEFT":
                    if self.snake[index][1] == 0:
                        new_snake[index][1] = self.width-1
                    else:
                        new_snake[index][1] -= 1
                if self.snakeDirection == "RIGHT":
                    if self.snake[index][1] == self.width-1:
                        new_snake[index][1] = 0
                    else:
                        new_snake[index][1] += 1
            else:
                new_snake[index] = self.snake[index-1]
                lastindexpos = new_snake[index]

        self.snake = deepcopy(new_snake)
        
        self.checkSnakeCollision()
        self.checkSnakeBite(lastindexpos)
        #self.snakePoints += 1


    def buildSnakeScreen(self):
        #print("buildSnakeScreen")
        #set every pixel black
        for row in range(0,self.height):
            for pixel in range(0,self.width):
                self.pixels[row][pixel] = gamecolors.BLACK
        #set snake pixels light and dark cyan
        for index in range(len(self.snake)):
            if self.snakeColor == 'green':
                if index%3:
                    self.pixels[self.snake[index][0]][self.snake[index][1]] = gamecolors.SNAKE_GREEN_1
                else:
                    self.pixels[self.snake[index][0]][self.snake[index][1]] = gamecolors.SNAKE_GREEN_2
            elif self.snakeColor == 'yellow':
                if index%3:
                    self.pixels[self.snake[index][0]][self.snake[index][1]] = gamecolors.SNAKE_YELLOW_1
                else:
                    self.pixels[self.snake[index][0]][self.snake[index][1]] = gamecolors.SNAKE_YELLOW_2
            elif self.snakeColor == 'red':
                if index%3:
                    self.pixels[self.snake[index][0]][self.snake[index][1]] = gamecolors.SNAKE_RED_1
                else:
                    self.pixels[self.snake[index][0]][self.snake[index][1]] = gamecolors.SNAKE_RED_2
            elif self.snakeColor == 'blue':
                if index%3:
                    self.pixels[self.snake[index][0]][self.snake[index][1]] = gamecolors.SNAKE_BLUE_1
                else:
                    self.pixels[self.snake[index][0]][self.snake[index][1]] = gamecolors.SNAKE_BLUE_2
        #set cherry pixel
        if self.cherrySpawned == True:
            if self.snakeColor == 'red':
                self.pixels[self.cherryPosition[0]][self.cherryPosition[1]] = gamecolors.GREEN
            else:
                self.pixels[self.cherryPosition[0]][self.cherryPosition[1]] = gamecolors.RED
        #draw the matrix
        self.send2strip(self.pixels)

    def spawnCherry(self):
        #print("spawnCherry")
        x = random.randrange(0,self.width-1)
        y = random.randrange(0,self.height-1)
        onsnake = False
        for index in range(len(self.snake)):
            if self.snake[index][0] == y and self.snake[index][1] == x:
                onsnake = True
        if onsnake == False:
            self.cherryPosition = [int(y),int(x)]
            self.cherrySpawned = True
        else:
            self.spawnCherry()

    def checkSnakeCollision(self):
        for index in range(1,len(self.snake)):
            if self.snake[index][0] == self.snake[0][0] and self.snake[index][1] == self.snake[0][1]:
                print("SnakeCollision")
                self.snakeGameOver()

    def snakeGameOver(self):
        #print("snakeGameOver")
        self.snakeGameRunning = False
        self.snd_snake_gameover.play()
        time.sleep(1)
        print("Du hast")
        print(self.snakePoints)
        print("Punkte.")
        self.speakEngine = None
        self.speakEngine = pyttsx.init()
        rate = self.speakEngine.getProperty('rate')
        #self.speakEngine.setProperty('rate', rate-10)
        self.speakEngine.setProperty('voice', 'german')
        self.speakEngine.say("Du hast "+str(self.snakePoints)+" Punkte.")
        if self.hiScores_Snake[0][1] < self.snakePoints:
            entry = (self.playerName, self.snakePoints)
            self.hiScores_Snake.append(entry)
            self.hiScores_Snake.sort(key=self.getKey,reverse=True)
            pickle.dump(self.hiScores_Snake,open("/home/pi/ledtable/hiscores_snake.zfl","wb"))
            self.speakEngine.say("Du hast einen neuen Rekord aufgestellt.")
            self.speakEngine.runAndWait()
            self.snd_appluse.play()
            time.sleep(6)
            self.snd_rocket.play()
            time.sleep(10)
        else:
            self.speakEngine.say("Der Rekord liegt bei "+str(self.hiScores_Snake[0][1])+" Punkten.")
            self.speakEngine.runAndWait()
        self.fadeInOut([0,255,0])
        self.startLoungeTable()

    def checkSnakeBite(self,lastindexpos):
        #print("checkSnakeBite")
        if self.snake[0][0] == self.cherryPosition[0] and self.snake[0][1] == self.cherryPosition[1]:
            #snake bites the cherry - longer snake
            self.snakePoints += 10
            self.snake.append(lastindexpos)
            #paint cherry green
            self.pixels[self.cherryPosition[0]][self.cherryPosition[1]] = gamecolors.GREEN
            self.send2strip(self.pixels)
            self.cherrySpawned = False
            self.snd_bite.play()


####################################################################################
################################ Rainbow-Drive #####################################
####################################################################################


    # Rainbow-Drive
    def startRainbowDrive(self):
        print("Starting Rainbow Drive...")
        self.rainbowDriveRunning = True
        self.waittime = 200
        self.rainbowCompression = 10 #full rainbow-length would be 255 pixel - compression needed
        self.keyPressTimeout = 100
        self.acceleration = 0.3
        self.rainbow_points = 0
        self.car = [[13,4],[12,4]] #coords are [y,x] NOT [x,y] !!!
        self.road = [
                        [[0,3],[0,4],[0,5],[0,6]],
                        [[0,3],[0,4],[0,5],[0,6]],
                        [[0,3],[0,4],[0,5],[0,6]],
                        [[0,3],[0,4],[0,5],[0,6]],
                        [[0,3],[0,4],[0,5],[0,6]],
                        [[0,3],[0,4],[0,5],[0,6]],
                        [[0,3],[0,4],[0,5],[0,6]],
                        [[0,3],[0,4],[0,5],[0,6]],
                        [[0,3],[0,4],[0,5],[0,6]],
                        [[0,3],[0,4],[0,5],[0,6]],
                        [[0,3],[0,4],[0,5],[0,6]],
                        [[0,3],[0,4],[0,5],[0,6]],
                        [[0,3],[0,4],[0,5],[0,6]],
                        [[0,3],[0,4],[0,5],[0,6]],
                        [[0,3],[0,4],[0,5],[0,6]]
                    ]
        self.road_tick = 1
        self.road_turn_interval = 5

        print("Loading Hiscores..."),
        self.hiScores_RainbowDrive = pickle.load(open("/home/pi/ledtable/hiscores_rainbowdrive.zfl","rb"))
        self.hiScores_RainbowDrive.sort(key=self.getKey,reverse=True)
        print("done")

        joystick_count = pygame.joystick.get_count()
        if joystick_count == 0:
            print ("How do you want to drive without a joystick?")
            sys.exit()
        else:
            self.gamepad = pygame.joystick.Joystick(0)
            self.gamepad.init()
            
        self.moveTime = pygame.time.get_ticks()
        self.keyTime = self.moveTime
        self.keyPressTime = self.moveTime
        self.snd_engine.play(-1)

        start = 0

        while self.rainbowDriveRunning:
            pygame.event.pump()
            if pygame.time.get_ticks() > self.keyPressTime + self.keyPressTimeout:
                self.getKeypress(self.gamepad)
                

            if (pygame.time.get_ticks()>=start+self.waittime):
                self.rainbow_points += 1
                if self.waittime > 0:
                    self.waittime -= self.acceleration
                self.moveRoad()
                self.moveCar()
                self.buildRainbowDriveScreen()
                self.checkCarCollision()
                start = pygame.time.get_ticks()
                self.lastPressed = None
                
    def buildRainbowDriveScreen(self):
        # all black
        for row in range(0,self.height):
            for pixel in range(0,self.width):
                self.pixels[row][pixel] = gamecolors.BLACK

        # draw full matrix as rainbow
        for row in range(0,self.height):
            color = self.getRainbowColor((row*self.rainbowCompression + self.road_tick) & 255)
            for pixel in range(0,self.width):
                self.pixels[row][pixel] = color

        # draw road grey
        for row in range(0,len(self.road)):
            for pixel in range(0,len(self.road[row])):
                self.pixels[row][self.road[row][pixel][1]] = gamecolors.GREY

        # draw car blue
        for i in range(0,len(self.car)):
            self.pixels[self.car[i][0]][self.car[i][1]] = gamecolors.BLUE

        self.send2strip(self.pixels)

    def moveRoad(self):
        new_road_elem = deepcopy(self.road[0])
        
        if self.road_tick%self.road_turn_interval == 0: # turn every [interval] ticks
            # road direction
            r = random.randint(0,1)
            if r == 0:
                # road turns left
                for i in range(0,len(new_road_elem)):
                    new_road_elem[i][1] -= 1 
            else:
                # road turns left
                for i in range(0,len(new_road_elem)):
                    new_road_elem[i][1] += 1

        # check road wall collision
        if new_road_elem[0][1] < 0 or new_road_elem[len(new_road_elem)-1][1] > self.width-1:
            self.moveRoad()
        else:
            # move down road
            self.road.insert(0,new_road_elem)
            if len(self.road) > self.height:
                del self.road[-1]
                
            if self.road_tick == 255:
                self.road_tick = 1;
            else:
                self.road_tick += 1
        #print(self.road)
        #print("----------------------")

    def moveCar(self):
        if self.lastPressed == "LEFT" and self.car[0][1] > 0:
            self.car[0][1] -= 1
            self.car[1][1] -= 1
        if self.lastPressed == "RIGHT" and self.car[0][1] < self.width-1:
            self.car[0][1] += 1
            self.car[1][1] += 1

    def checkCarCollision(self):
        matches = 0
        for car_pos in range(0,len(self.car)):
            for road_row in range(0,len(self.road)):
                for road_pos in range(0,len(self.road[road_row])):
                    if self.car[car_pos] == [road_row, self.road[road_row][road_pos][1]]:
                        matches += 1
        if matches < 2:
            print("car collision!")
            self.snd_engine.stop()
            self.snd_car_crash.play()
            self.rainbowDriveGameOver()

    def getRainbowColor(self,pos):
        fac = 3
        """Generate rainbow colors across 0-255 positions."""
        if pos < 85:
            col = [pos * fac, 255 - pos * fac, 0] #Color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            col = [255 - pos * fac, 0, pos * fac] #Color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            col = [0, pos * fac, 255 - pos * fac] #Color(0, pos * 3, 255 - pos * 3)
        
        return col

    def rainbowDriveGameOver(self):
        self.rainbowDriveRunning = False
        print("Du hast "+str(self.rainbow_points)+" Punkte")
        self.speakEngine = None
        self.speakEngine = pyttsx.init()
        rate = self.speakEngine.getProperty('rate')
        #self.speakEngine.setProperty('rate', rate-10)
        self.speakEngine.setProperty('voice', 'german')
        self.speakEngine.say("Du hast "+str(self.rainbow_points)+" Punkte.")
        if self.hiScores_RainbowDrive[0][1] < self.rainbow_points:
            entry = (self.playerName, self.rainbow_points)
            self.hiScores_RainbowDrive.append(entry)
            self.hiScores_RainbowDrive.sort(key=self.getKey,reverse=True)
            pickle.dump(self.hiScores_RainbowDrive,open("/home/pi/ledtable/hiscores_rainbowdrive.zfl","wb"))
            self.speakEngine.say("Du hast einen neuen Rekord aufgestellt.")
            self.speakEngine.runAndWait()
            self.snd_appluse.play()
            time.sleep(6)
            self.snd_rocket.play()
            time.sleep(10)
        else:
            self.speakEngine.say("Der Rekord liegt bei "+str(self.hiScores_RainbowDrive[0][1])+" Punkten.")
            self.speakEngine.runAndWait()
        self.waittime = 250
        time.sleep(3)
        self.fadeInOut([0,0,255])
        self.startLoungeTable()



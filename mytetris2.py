import pygame, pickle
import math, sys, os, random, socket, time, colorsys
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
    I_COLOR = [0,255,255]
    J_COLOR = [0,0,255]
    L_COLOR = [255,80,0]
    O_COLOR = [255,255,0]
    S_COLOR = [0,255,0]
    T_COLOR = [255,0,255]
    Z_COLOR = [255,0,0]
    BACKGROUNDCOLOR = [0,0,0]
    TEXTCOLOR = [255,255,255]    
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
              gamecolors.I_COLOR]
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
              gamecolors.J_COLOR]
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
              gamecolors.L_COLOR]
    O_TILE = [[[1,1],
               [1,1]],
              [[1,1],
               [1,1]],
              [[1,1],
               [1,1]],
              [[1,1],
               [1,1]],
              gamecolors.O_COLOR]
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
              gamecolors.S_COLOR]
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
              gamecolors.T_COLOR]
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
              gamecolors.Z_COLOR]    
class RGB_Tetris:
    #Variables for all instances of TetrisClass
    width = 10
    height = 15
    hiScores = []
    spidev = file("/dev/spidev0.0", "wb")
    snd_click = None
    snd_linekil = None
    snd_tilefix = None
    snd_pause = None
    snd_gameover = None
    snd_level = None
    
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
        self.fixedPixels = [[gamecolors.BACKGROUNDCOLOR for x in range(width)] for x in range(height+2)]
        self.movingPixels = [[gamecolors.BACKGROUNDCOLOR for x in range(width)] for x in range(height+2)]
        self.displayPixels = [[gamecolors.BACKGROUNDCOLOR for x in range(width)] for x in range(height)]
        self.keyPressTimeout = 125
        self.keyPressTime = 0
        self.keyTimeout = 150
        self.keyTime = 0
        self.moveTimeout = 500
        self.moveTime = 0
        self.brightness = 1.0
        self.Tetris_Points = 0
        self.running = False
        self.paused = False
        self.lastPressed = "NONE"
        self.s=s
        
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
    def matrix2snake(x,y):
                #   _   _   _
        ######     | | | | | |
        ######  -> | | | | | |
        ######     | | | | | |
                #     -   -
        mapping = {'0,0': 15,
                    '0,1': 14,
                    '0,2': 13,
                    '0,3': 12,
                    '0,4': 11,
                    '0,5': 10,
                    '0,6': 9,
                    '0,7': 8,
                    '0,8': 7,
                    '0,9': 6,
                    '0,10': 5,
                    '0,11': 4,
                    '0,12': 3,
                    '0,13': 2,
                    '0,14': 1,
                    '1,0': 16,
                    '1,1': 17,
                    '1,2': 18,
                    '1,3': 19,
                    '1,4': 20,
                    '1,5': 21,
                    '1,6': 22,
                    '1,7': 23,
                    '1,8': 24,
                    '1,9': 25,
                    '1,10': 26,
                    '1,11': 27,
                    '1,12': 28,
                    '1,13': 29,
                    '1,14': 30,
                    '2,0': 45,
                    '2,1': 44,
                    '3,0': 46
                    }
        s = x + ',' + y
        #return mapping[s]


        if x%2==0:
            pos = (x+1)*height - y
        else:
            pos = (x*height) + 1 + y

        return pos

    def send2strip(self,matrix):
        for y in range(height):
            for x in range(width):
                a = int(matrix[row][pixel][0]*self.brightness)
                b = int(matrix[row][pixel][1]*self.brightness)
                c = int(matrix[row][pixel][2]*self.brightness)
                color = Color(a, b, c)
                pos = self.matrix2snake(x,y)
                strip.setPixelColor(pos, color)
        strip.show()
        time.sleep(0.001)

    def draw(self,matrix):
        sendstring = ""
        for row in range(height):
            if row%2==0:
                for pixel in range(0,width):
                    for color in range(0,3):
                        c=int(matrix[row][pixel][color]*self.brightness)
                        sendstring += chr(c & 0xFF)
            else:
                for pixel in range(9,-1,-1):
                    for color in range(0,3):
                        c=int(matrix[row][pixel][color]*self.brightness)
                        sendstring += chr(c & 0xFF)            
        self.spidev.write(sendstring)        
        self.spidev.flush()
        time.sleep(0.001)

    def fadeInOut(self,c):
            self.brightness=0
            self.displayPixels = [[c for x in range(width)] for x in range(height)]
            while self.brightness <1.0:
                    self.send2strip(self.displayPixels)
                    self.brightness+=0.05
            while self.brightness >0.0:
                    self.send2strip(self.displayPixels)
                    self.brightness-=0.05
            self.displayPixels = [[gamecolors.BACKGROUNDCOLOR for x in range(width)] for x in range(height)]
            self.brightness = 1.0
            self.send2strip(self.displayPixels)
    
    #Shuffle the next bag of Tetronimos        
    def shuffleSeq(self):
        str_list = [tiles.I_TILE,tiles.O_TILE,tiles.T_TILE,tiles.S_TILE,tiles.Z_TILE,tiles.J_TILE,tiles.L_TILE]
        random.shuffle(str_list)
        return str_list
    #Check if new spawned Tetromino overlaps the current fixedPixels
    def checkSpawn(self):
        tempPixels = [[0 for x in range(width)] for x in range(height+2)]
        for row in range(len(self.activeTet[self.activeTetRotation])):
            for col in range(len(self.activeTet[self.activeTetRotation][0])):
                if self.activeTet[self.activeTetRotation][row][col]:
                    tempPixels[self.activeTetCoords[0]+row][self.activeTetCoords[1]+col]=1
        for row in range (height+2):
            for col in range(width):
                if tempPixels[row][col]==1:
                    if self.fixedPixels[row][col]!=gamecolors.BACKGROUNDCOLOR:
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
        self.fixedPixels = [[gamecolors.BACKGROUNDCOLOR for x in range(width)] for x in range(height+2)]
        self.movingPixels = [[gamecolors.BACKGROUNDCOLOR for x in range(width)] for x in range(height+2)]
        self.displayPixels = [[gamecolors.BACKGROUNDCOLOR for x in range(width)] for x in range(height)]
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
        tempPixels = [[0 for x in range(width)] for x in range(height+2)]
        for row in range(len(self.activeTet[self.activeTetRotation])):
            for col in range(len(self.activeTet[self.activeTetRotation][0])):
                if self.activeTet[self.activeTetRotation][row][col]:
                    tempPixels[self.activeTetCoords[0]+row][self.activeTetCoords[1]+col]=1
        for row in range(height+2):
            if tempPixels[row][0]==1:
                return True
        for row in range (height+2):
            for col in range(width):
                if tempPixels[row][col]==1:
                    if self.fixedPixels[row][col-1]!=gamecolors.BACKGROUNDCOLOR:
                        return True
        return False    
    def checkMoveRightCollision(self):
        tempPixels = [[0 for x in range(width)] for x in range(height+2)]
        for row in range(len(self.activeTet[self.activeTetRotation])):
            for col in range(len(self.activeTet[self.activeTetRotation][0])):
                if self.activeTet[self.activeTetRotation][row][col]:
                    tempPixels[self.activeTetCoords[0]+row][self.activeTetCoords[1]+col]=1
        for row in range(height+2):
            if tempPixels[row][9]==1:
                return True
        for row in range (height+2):
            for col in range(width):
                if tempPixels[row][col]==1:
                    if self.fixedPixels[row][col+1]!=gamecolors.BACKGROUNDCOLOR:
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
        time.sleep(3)
        self.fadeInOut([255,0,0])
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
        sock.sendto(str(self.Tetris_Points), ("192.168.1.19", 56565))
        entry = (self.playerName, self.Tetris_Points)
        self.hiScores.append(entry)
        self.hiScores.sort(key=self.getKey,reverse=True)
        pickle.dump(self.hiScores,open("/home/pi/ledtable/hiscores.zfl","wb"))
    #Teil nach links drehen
    def rotateLeft(self):
        if self.activeTet == tiles.I_TILE:
            validMove = True
            if self.activeTetRotation == 0:
                tempPixels = [[0 for x in range(width)] for x in range(height+2)]
                if self.activeTetCoords[0]>19:
                    validMove=False    
                else:
                    for row in range(len(self.activeTet[3])):
                        for col in range(len(self.activeTet[3][0])):
                            if self.activeTet[3][row][col]:
                                tempPixels[self.activeTetCoords[0]-1+row][self.activeTetCoords[1]+1+col]=1
                    for row in range (height+2):
                        for col in range(width):
                            if tempPixels[row][col]==1:
                                if self.fixedPixels[row][col]!=gamecolors.BACKGROUNDCOLOR:
                                    validMove = False                        
                if validMove:
                    self.activeTetRotation =3
                    self.activeTetCoords[1]+=1    
                    self.activeTetCoords[0]-=1        
            elif self.activeTetRotation == 3:
                tempPixels = [[0 for x in range(width)] for x in range(height+2)]
                if self.activeTetCoords[1]<1 or self.activeTetCoords[1]>7:
                    validMove=False        
                else:
                    for row in range(len(self.activeTet[2])):
                        for col in range(len(self.activeTet[2][0])):
                            if self.activeTet[2][row][col]:
                                tempPixels[self.activeTetCoords[0]+2+row][self.activeTetCoords[1]-1+col]=1
                    for row in range (height+2):
                        for col in range(width):
                            if tempPixels[row][col]==1:
                                if self.fixedPixels[row][col]!=gamecolors.BACKGROUNDCOLOR:
                                    validMove = False                        
                if validMove:
                    self.activeTetRotation =2
                    self.activeTetCoords[1]-=1    
                    self.activeTetCoords[0]+=2            
            elif self.activeTetRotation == 2:
                tempPixels = [[0 for x in range(width)] for x in range(height+2)]
                if self.activeTetCoords[0]>height+2:
                    validMove=False    
                else:
                    for row in range(len(self.activeTet[1])):
                        for col in range(len(self.activeTet[1][0])):
                            if self.activeTet[1][row][col]:
                                tempPixels[self.activeTetCoords[0]-2+row][self.activeTetCoords[1]+2+col]=1
                    for row in range (height+2):
                        for col in range(width):
                            if tempPixels[row][col]==1:
                                if self.fixedPixels[row][col]!=gamecolors.BACKGROUNDCOLOR:
                                    validMove = False                
                if validMove:
                    self.activeTetRotation =1
                    self.activeTetCoords[1]+=2    
                    self.activeTetCoords[0]-=2        
            elif self.activeTetRotation == 1:
                tempPixels = [[0 for x in range(width)] for x in range(height+2)]
                if self.activeTetCoords[1]<2 or self.activeTetCoords[1]>8:
                    validMove=False    
                else:
                    for row in range(len(self.activeTet[0])):
                        for col in range(len(self.activeTet[0][0])):
                            if self.activeTet[0][row][col]:
                                tempPixels[self.activeTetCoords[0]+1+row][self.activeTetCoords[1]-2+col]=1
                    for row in range (height+2):
                        for col in range(width):
                            if tempPixels[row][col]==1:
                                if self.fixedPixels[row][col]!=gamecolors.BACKGROUNDCOLOR:
                                    validMove = False
                if validMove:
                    self.activeTetRotation =0
                    self.activeTetCoords[1]-=2    
                    self.activeTetCoords[0]+=1            
        elif self.activeTet == tiles.J_TILE or self.activeTet == tiles.L_TILE or self.activeTet == tiles.S_TILE or self.activeTet == tiles.T_TILE or self.activeTet == tiles.Z_TILE:
            validMove = True
            if self.activeTetRotation == 0:
                tempPixels = [[0 for x in range(width)] for x in range(height+2)]
                if self.activeTetCoords[0]>height-1:
                    validMove=False    
                else:
                    for row in range(len(self.activeTet[3])):
                        for col in range(len(self.activeTet[3][0])):
                            if self.activeTet[3][row][col]:
                                tempPixels[self.activeTetCoords[0]+row][self.activeTetCoords[1]+col]=1
                    for row in range (height+2):
                        for col in range(width):
                            if tempPixels[row][col]==1:
                                if self.fixedPixels[row][col]!=gamecolors.BACKGROUNDCOLOR:
                                    validMove = False                        
                if validMove:
                    self.activeTetRotation =3
                    self.activeTetCoords[1]+=0    
                    self.activeTetCoords[0]-=0        
            elif self.activeTetRotation == 3:
                tempPixels = [[0 for x in range(width)] for x in range(height+2)]
                if self.activeTetCoords[1]>7:
                    validMove=False        
                else:
                    for row in range(len(self.activeTet[2])):
                        for col in range(len(self.activeTet[2][0])):
                            if self.activeTet[2][row][col]:
                                tempPixels[self.activeTetCoords[0]+1+row][self.activeTetCoords[1]+col]=1
                    for row in range (height+2):
                        for col in range(width):
                            if tempPixels[row][col]==1:
                                if self.fixedPixels[row][col]!=gamecolors.BACKGROUNDCOLOR:
                                    validMove = False                        
                if validMove:
                    self.activeTetRotation =2
                    self.activeTetCoords[1]-=0    
                    self.activeTetCoords[0]+=1            
            elif self.activeTetRotation == 2:
                tempPixels = [[0 for x in range(width)] for x in range(height+2)]
                if self.activeTetCoords[0]>height:
                    validMove=False    
                else:
                    for row in range(len(self.activeTet[1])):
                        for col in range(len(self.activeTet[1][0])):
                            if self.activeTet[1][row][col]:
                                tempPixels[self.activeTetCoords[0]-1+row][self.activeTetCoords[1]+1+col]=1
                    for row in range (height+2):
                        for col in range(width):
                            if tempPixels[row][col]==1:
                                if self.fixedPixels[row][col]!=gamecolors.BACKGROUNDCOLOR:
                                    validMove = False                
                if validMove:
                    self.activeTetRotation =1
                    self.activeTetCoords[1]+=1    
                    self.activeTetCoords[0]-=1        
            elif self.activeTetRotation == 1:
                tempPixels = [[0 for x in range(width)] for x in range(height+2)]
                if self.activeTetCoords[1]<1:
                    validMove=False    
                else:
                    for row in range(len(self.activeTet[0])):
                        for col in range(len(self.activeTet[0][0])):
                            if self.activeTet[0][row][col]:
                                tempPixels[self.activeTetCoords[0]+0+row][self.activeTetCoords[1]-1+col]=1
                    for row in range (height+2):
                        for col in range(width):
                            if tempPixels[row][col]==1:
                                if self.fixedPixels[row][col]!=gamecolors.BACKGROUNDCOLOR:
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
                tempPixels = [[0 for x in range(width)] for x in range(height+2)]
                if self.activeTetCoords[0]>height-1:
                    validMove=False    
                else:
                    for row in range(len(self.activeTet[1])):
                        for col in range(len(self.activeTet[1][0])):
                            if self.activeTet[1][row][col]:
                                tempPixels[self.activeTetCoords[0]-1+row][self.activeTetCoords[1]+2+col]=1
                    for row in range (height+2):
                        for col in range(width):
                            if tempPixels[row][col]==1:
                                if self.fixedPixels[row][col]!=gamecolors.BACKGROUNDCOLOR:
                                    validMove = False                        
                if validMove:
                    self.activeTetRotation =1
                    self.activeTetCoords[1]+=2    
                    self.activeTetCoords[0]-=1        
            elif self.activeTetRotation == 1:
                tempPixels = [[0 for x in range(width)] for x in range(height+2)]
                if self.activeTetCoords[1]<2 or self.activeTetCoords[1]>8:
                    validMove=False        
                else:
                    for row in range(len(self.activeTet[2])):
                        for col in range(len(self.activeTet[2][0])):
                            if self.activeTet[2][row][col]:
                                tempPixels[self.activeTetCoords[0]+2+row][self.activeTetCoords[1]-2+col]=1
                    for row in range (height+2):
                        for col in range(width):
                            if tempPixels[row][col]==1:
                                if self.fixedPixels[row][col]!=gamecolors.BACKGROUNDCOLOR:
                                    validMove = False                        
                if validMove:
                    self.activeTetRotation =2
                    self.activeTetCoords[1]-=2    
                    self.activeTetCoords[0]+=2            
            elif self.activeTetRotation == 2:
                tempPixels = [[0 for x in range(width)] for x in range(height+2)]
                if self.activeTetCoords[0]>height:
                    validMove=False    
                else:
                    for row in range(len(self.activeTet[3])):
                        for col in range(len(self.activeTet[3][0])):
                            if self.activeTet[3][row][col]:
                                tempPixels[self.activeTetCoords[0]-2+row][self.activeTetCoords[1]+1+col]=1
                    for row in range (height+2):
                        for col in range(width):
                            if tempPixels[row][col]==1:
                                if self.fixedPixels[row][col]!=gamecolors.BACKGROUNDCOLOR:
                                    validMove = False                
                if validMove:
                    self.activeTetRotation =3
                    self.activeTetCoords[1]+=1    
                    self.activeTetCoords[0]-=2        
            elif self.activeTetRotation == 3:
                tempPixels = [[0 for x in range(width)] for x in range(height+2)]
                if self.activeTetCoords[1]<1 or self.activeTetCoords[1]>7:
                    validMove=False    
                else:
                    for row in range(len(self.activeTet[0])):
                        for col in range(len(self.activeTet[0][0])):
                            if self.activeTet[0][row][col]:
                                tempPixels[self.activeTetCoords[0]+1+row][self.activeTetCoords[1]-1+col]=1
                    for row in range (height+2):
                        for col in range(width):
                            if tempPixels[row][col]==1:
                                if self.fixedPixels[row][col]!=gamecolors.BACKGROUNDCOLOR:
                                    validMove = False
                if validMove:
                    self.activeTetRotation =0
                    self.activeTetCoords[1]-=1    
                    self.activeTetCoords[0]+=1            
        elif self.activeTet == tiles.J_TILE or self.activeTet == tiles.L_TILE or self.activeTet == tiles.S_TILE or self.activeTet == tiles.T_TILE or self.activeTet == tiles.Z_TILE:
            validMove = True
            if self.activeTetRotation == 0:
                tempPixels = [[0 for x in range(width)] for x in range(height+2)]
                if self.activeTetCoords[0]>height-1:
                    validMove=False    
                else:
                    for row in range(len(self.activeTet[1])):
                        for col in range(len(self.activeTet[1][0])):
                            if self.activeTet[1][row][col]:
                                tempPixels[self.activeTetCoords[0]+row][self.activeTetCoords[1]+1+col]=1
                    for row in range (height+2):
                        for col in range(width):
                            if tempPixels[row][col]==1:
                                if self.fixedPixels[row][col]!=gamecolors.BACKGROUNDCOLOR:
                                    validMove = False                        
                if validMove:
                    self.activeTetRotation =1
                    self.activeTetCoords[1]+=1    
                    self.activeTetCoords[0]-=0        
            elif self.activeTetRotation == 1:
                tempPixels = [[0 for x in range(width)] for x in range(height+2)]
                if self.activeTetCoords[1]<1:
                    validMove=False        
                else:
                    for row in range(len(self.activeTet[2])):
                        for col in range(len(self.activeTet[2][0])):
                            if self.activeTet[2][row][col]:
                                tempPixels[self.activeTetCoords[0]+1+row][self.activeTetCoords[1]-1+col]=1
                    for row in range (height+2):
                        for col in range(width):
                            if tempPixels[row][col]==1:
                                if self.fixedPixels[row][col]!=gamecolors.BACKGROUNDCOLOR:
                                    validMove = False                        
                if validMove:
                    self.activeTetRotation =2
                    self.activeTetCoords[1]-=1    
                    self.activeTetCoords[0]+=1            
            elif self.activeTetRotation == 2:
                tempPixels = [[0 for x in range(width)] for x in range(height+2)]
                if self.activeTetCoords[0]>height:
                    validMove=False    
                else:
                    for row in range(len(self.activeTet[3])):
                        for col in range(len(self.activeTet[3][0])):
                            if self.activeTet[3][row][col]:
                                tempPixels[self.activeTetCoords[0]-1+row][self.activeTetCoords[1]+col]=1
                    for row in range (height+2):
                        for col in range(width):
                            if tempPixels[row][col]==1:
                                if self.fixedPixels[row][col]!=gamecolors.BACKGROUNDCOLOR:
                                    validMove = False                
                if validMove:
                    self.activeTetRotation =3
                    self.activeTetCoords[1]+=0    
                    self.activeTetCoords[0]-=1        
            elif self.activeTetRotation == 3:
                tempPixels = [[0 for x in range(width)] for x in range(height+2)]
                if self.activeTetCoords[1]>7:
                    validMove=False    
                else:
                    for row in range(len(self.activeTet[0])):
                        for col in range(len(self.activeTet[0][0])):
                            if self.activeTet[0][row][col]:
                                tempPixels[self.activeTetCoords[0]+row][self.activeTetCoords[1]+col]=1
                    for row in range (height+2):
                        for col in range(width):
                            if tempPixels[row][col]==1:
                                if self.fixedPixels[row][col]!=gamecolors.BACKGROUNDCOLOR:
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
        tempPixels = [[0 for x in range(width)] for x in range(height+3)]
        for row in range(len(self.activeTet[self.activeTetRotation])):
            for col in range(len(self.activeTet[self.activeTetRotation][0])):
                if self.activeTet[self.activeTetRotation][row][col]:
                    tempPixels[self.activeTetCoords[0]+1+row][self.activeTetCoords[1]+col]=1
        for col in range(0,width):
            if tempPixels[height+2][col]==1:
                return True    
        for row in range (height+2):
            for col in range(width):
                if tempPixels[row][col]==1:
                    if self.fixedPixels[row][col]!=gamecolors.BACKGROUNDCOLOR:
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
        for row in range(height+2):
            counter = 0
            for col in range(width):
                if self.fixedPixels[row][col]!=gamecolors.BACKGROUNDCOLOR:
                    counter+=1
            if counter == 10:
                linesFinished +=1
                for col in range(width):
                    self.fixedPixels[row][col]=gamecolors.BACKGROUNDCOLOR
                self.buildScreen()
                for mrow in range(row,0,-1):
                    for mcol in range(width):
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
        if u.get_axis(1) <= -0.5: #D-Pad nach oben
            self.lastPressed = "UP"    
        if u.get_axis(1) >= +0.5: #D-Pad nach unten
            self.lastPressed = "DOWN"    
        if u.get_axis(0) >= +0.5: #D-Pad rechts
            self.lastPressed = "RIGHT"
        if u.get_axis(0) <= -0.5: #D-Pad nach links
            self.lastPressed = "LEFT"
        if u.get_button(1): #Button A - right red button - Rotate right
            self.lastPressed = "A"
        if u.get_button(2): #Button B - left red button - Rotate left
            self.lastPressed = "B"
        if u.get_button(8):
            self.lastPressed = "SELECT"
        if u.get_button(9):
            self.lastPressed = "START"    
    #Overlay fixed and mobile Pixels
    def buildScreen(self):
        if self.running:
            for row in range(height):
                for pixel in range(width):
                    self.displayPixels[row][pixel]=self.fixedPixels[row+2][pixel]
            if self.activeTet != None:
                for row in range(len(self.activeTet[self.activeTetRotation])):
                    for col in range(len(self.activeTet[self.activeTetRotation][0])):
                        if self.activeTet[self.activeTetRotation][row][col]:
                            self.displayPixels[self.activeTetCoords[0]-2+row][self.activeTetCoords[1]+col]=self.activeTet[4]
            self.send2strip(self.displayPixels)
    def getKey(self,item):
        return item[1]  
    def startGame(self):
        print("Initialize sound system..."),
        pygame.mixer.pre_init(44100, -16, 2, 2048)    
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
        print("done")
        pygame.mixer.music.play(-1)
        joystick_count = pygame.joystick.get_count()
        if joystick_count == 0:
            print ("How do you want to play Tetris without a joystick?")
            sys.exit()
        else:
            j = pygame.joystick.Joystick(0)
            j.init()
            print('Initialized Joystick : %s' % j.get_name())
        print("Loading Hiscores..."),
        self.hiScores = pickle.load(open("/home/pi/ledtable/hiscores.zfl","rb"))
        self.hiScores.sort(key=self.getKey,reverse=True)
        print("done")
        print("Aktueller Hiscore: "+str(self.hiScores[0][1])+" Punkte von "+str(self.hiScores[0][0]))
        print("Hi "+self.playerName+", good luck!")
        print("Game of Tetris started!")
        self.fadeInOut([255,255,255])
        self.running = True
        self.spawn()
        self.moveTime = pygame.time.get_ticks()
        self.keyTime = self.moveTime
        self.keyPressTime = self.moveTime
        while self.running:
            try:
                data = self.s.recv(1024)
                if data=="AbOrTTrObA":
                    self.running=False
            except: 
                pass
            
            if self.paused:
                time.sleep(1)
                while self.paused:
                    pygame.event.pump()
                    if j.get_button(9):
                        print ("Game unpaused")
                        self.snd_pause.play()
                        pygame.mixer.music.unpause()
                        time.sleep(1)
                        self.paused = False
                        self.lastPressed="NONE"
            
            if self.running:
                if pygame.time.get_ticks() > self.keyPressTime + self.keyPressTimeout:
                     self.getKeypress(j)
                if pygame.time.get_ticks() > self.keyTime + self.keyTimeout:
                     self.keyAction()
                     self.keyTime = pygame.time.get_ticks()
                if pygame.time.get_ticks() > self.moveTime + self.moveTimeout:
                    self.timeAction()
                    self.moveTime = pygame.time.get_ticks()
            if self.running:
                self.buildScreen()
        pygame.quit()
        print("Tetris ended.")
from machine import Pin,SPI,PWM
import framebuf
import time
import random

BL = 13
DC = 8
RST = 12
MOSI = 11
SCK = 10
CS = 9


class LCD_1inch14(framebuf.FrameBuffer):
    def __init__(self):
        self.width = 240
        self.height = 135
        
        self.cs = Pin(CS,Pin.OUT)
        self.rst = Pin(RST,Pin.OUT)
        
        self.cs(1)
        self.spi = SPI(1)
        self.spi = SPI(1,1000_000)
        self.spi = SPI(1,10000_000,polarity=0, phase=0,sck=Pin(SCK),mosi=Pin(MOSI),miso=None)
        self.dc = Pin(DC,Pin.OUT)
        self.dc(1)
        self.buffer = bytearray(self.height * self.width * 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.init_display()
        
        self.red   =   0x07E0
        self.green =   0x001f
        self.blue  =   0xf800
        self.white =   0xffff
        
    def write_cmd(self, cmd):
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)

    def init_display(self):
        """Initialize dispaly"""  
        self.rst(1)
        self.rst(0)
        self.rst(1)
        
        self.write_cmd(0x36)
        self.write_data(0x70)

        self.write_cmd(0x3A) 
        self.write_data(0x05)

        self.write_cmd(0xB2)
        self.write_data(0x0C)
        self.write_data(0x0C)
        self.write_data(0x00)
        self.write_data(0x33)
        self.write_data(0x33)

        self.write_cmd(0xB7)
        self.write_data(0x35) 

        self.write_cmd(0xBB)
        self.write_data(0x19)

        self.write_cmd(0xC0)
        self.write_data(0x2C)

        self.write_cmd(0xC2)
        self.write_data(0x01)

        self.write_cmd(0xC3)
        self.write_data(0x12)   

        self.write_cmd(0xC4)
        self.write_data(0x20)

        self.write_cmd(0xC6)
        self.write_data(0x0F) 

        self.write_cmd(0xD0)
        self.write_data(0xA4)
        self.write_data(0xA1)

        self.write_cmd(0xE0)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0D)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2B)
        self.write_data(0x3F)
        self.write_data(0x54)
        self.write_data(0x4C)
        self.write_data(0x18)
        self.write_data(0x0D)
        self.write_data(0x0B)
        self.write_data(0x1F)
        self.write_data(0x23)

        self.write_cmd(0xE1)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0C)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2C)
        self.write_data(0x3F)
        self.write_data(0x44)
        self.write_data(0x51)
        self.write_data(0x2F)
        self.write_data(0x1F)
        self.write_data(0x1F)
        self.write_data(0x20)
        self.write_data(0x23)
        
        self.write_cmd(0x21)

        self.write_cmd(0x11)

        self.write_cmd(0x29)

    def show(self):
        self.write_cmd(0x2A)
        self.write_data(0x00)
        self.write_data(0x28)
        self.write_data(0x01)
        self.write_data(0x17)
        
        self.write_cmd(0x2B)
        self.write_data(0x00)
        self.write_data(0x35)
        self.write_data(0x00)
        self.write_data(0xBB)
        
        self.write_cmd(0x2C)
        
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(self.buffer)
        self.cs(1)
      
#settings
xfood=0
yfood=0
xob=[50,150,20]
yob=[90,50,30]
def foodrespawn():
    global xfood,yfood
    xfood=random.randint(20,200)
    yfood=random.randint(20,95)

def drawsnake(snakelist):
    for i in snakelist:
        LCD.rect(i[0],i[1],width,height,LCD.green)
        
    
xpos=100
ypos=50
width=10
height=10
direction = "ABC"
olddirection = "ABC"
score = 0
gameover = False
restart=False
lengthsnake = 1
snakelist = []


foodrespawn()

if __name__=='__main__':
    pwm = PWM(Pin(BL))
    pwm.freq(1000)
    pwm.duty_u16(32768)#max 65535

    LCD = LCD_1inch14()
    #color BRG
    LCD.fill(LCD.white)
 
    LCD.show()
    LCD.text("Snake Game",90,3,LCD.red)
    #border 
    LCD.hline(10,10,220,LCD.blue)
    LCD.hline(10,125,220,LCD.blue)
    LCD.vline(10,10,115,LCD.blue)
    LCD.vline(230,10,115,LCD.blue)

    #key presses
    LCD.show()
    keyA = Pin(15,Pin.IN,Pin.PULL_UP) #top button
    keyB = Pin(17,Pin.IN,Pin.PULL_UP) #bottom button
    
    key2 = Pin(2 ,Pin.IN,Pin.PULL_UP) #up
    key3 = Pin(3 ,Pin.IN,Pin.PULL_UP)#press
    key4 = Pin(16 ,Pin.IN,Pin.PULL_UP)#left
    key5 = Pin(18 ,Pin.IN,Pin.PULL_UP)#down
    key6 = Pin(20 ,Pin.IN,Pin.PULL_UP)#right
    
   
                     
    while(1):
        restart=False
        #move with direction
        if direction == "RIGHT" and xpos<205:
            olddirection = "RIGHT"
            xpos+=5
            LCD.fill_rect(xpos-5,ypos,width,height,LCD.white)
            
        elif direction == "LEFT" and xpos>15:
            olddirection = "LEFT"
            xpos-=5
            LCD.fill_rect(xpos+5,ypos,width,height,LCD.white)
            
        elif direction == "UP" and ypos>15:
            olddirection = "UP"
            ypos-=5
            LCD.fill_rect(xpos,ypos+5,width,height,LCD.white)
            
        elif direction == "DOWN" and ypos<110:
            olddirection = "DOWN"
            ypos+=5
            LCD.fill_rect(xpos,ypos-5,width,height,LCD.white)
            
        if(keyB.value() == 0):
            print("B")
    
        if(key2.value() == 0 and ypos>15):#上
            direction = "UP"
            print(xpos)
            print(ypos)
            
        if(key3.value() == 0):#中
            print("CTRL")

        if(key4.value() == 0 and xpos>15):#左
            direction="LEFT"
            print(xpos)
            print(ypos)
            
        if(key5.value() == 0 and ypos<107):#下
            direction="DOWN"
            print(xpos)
            print(ypos)
            
        if(key6.value() == 0 and xpos<205):#右
            direction="RIGHT"
            print("RIGHT")
            print(xpos)
            print(ypos)
        
        #direction changing
        if direction != olddirection:
            if direction== "UP":
                LCD.fill_rect(xpos,ypos-10,width*2,height*2,LCD.white)
            if direction== "DOWN":
                LCD.fill_rect(xpos,ypos+10,width*2,height*2,LCD.white)
            if direction== "LEFT":
                LCD.fill_rect(xpos+10,ypos,width*2,height*2,LCD.white)
            if direction== "RIGHT":
                LCD.fill_rect(xpos-10,ypos,width*2,height*2,LCD.white)
        
        while gameover==True:
            if(keyA.value() == 0):
                print("A")
                lengthsnake=0
                LCD.fill(LCD.white)
                LCD.show()
                LCD.text("Snake Game",90,3,LCD.red)
                #border 
                LCD.hline(10,10,220,LCD.blue)
                LCD.hline(10,125,220,LCD.blue)
                LCD.vline(10,10,115,LCD.blue)
                LCD.vline(230,10,115,LCD.blue)
                xpos=100
                ypos=50
                restart=True
                gameover=False
                score=0
                
        LCD.rect(xpos,ypos,width,height,LCD.green)
        LCD.fill_rect(xfood,yfood,10,10,LCD.blue)
        for i in range(len(xob)):
            LCD.text("X",xob[i],yob[i],LCD.red)
        
        
        #detect collision
        if xfood+7 <= xpos+20 and xfood-7 >= xpos-20 and yfood+7<=ypos+20 and yfood-7>=ypos-20:
            LCD.fill_rect(xfood,yfood,10,10,LCD.white)
            foodrespawn()
            score+=1
            lengthsnake+=1
            #width+=1
            #height+=1
            LCD.fill_rect(90,126,70,10,LCD.white)
            LCD.text("Score:"+str(score), 90,126,LCD.red)
            
        #object collision
        for i in range(len(xob)):
            if xob[i]<= xpos+12 and xob[i]>= xpos-12 and yob[i]<=ypos+9 and yob[i]>=ypos-9:
                gameover=True
                LCD.fill(LCD.red)
                LCD.text("Game over",90,50,LCD.white)
                LCD.text("Score:"+str(score), 90,70,LCD.green)
                LCD.text("Press top button to restart",15,90,LCD.blue)
            
        #draw snake bodies at the end
        snakehead=[]
        snakehead.append(xpos)
        snakehead.append(ypos)
        snakelist.append(snakehead)
        #delete extra bodies
        if len(snakelist) > lengthsnake:
            del snakelist[0]
            if direction == "UP":
                LCD.fill_rect(xpos,ypos+lengthsnake*height,width,height,LCD.white)                    
                
            elif direction == "DOWN":
                LCD.fill_rect(xpos,ypos-lengthsnake*height,width,height,LCD.white)
                
            elif direction == "LEFT":
                LCD.fill_rect(xpos+lengthsnake*height,ypos,width,height,LCD.white)
            
            elif direction == "RIGHT":
                LCD.fill_rect(xpos-lengthsnake*height,ypos,width,height,LCD.white)
        drawsnake(snakelist)
        
        LCD.show()

    time.sleep(1)
    LCD.fill(0xFFFF)



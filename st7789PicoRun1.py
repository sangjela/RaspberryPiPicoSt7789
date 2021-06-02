"""
Raspberry Pi Pico/MicroPython exercise 240x240 ST7789 SPI LCD
using MicroPython library: https://github.com/russhughes/st7789py_mpy
original source from
https://helloraspberrypi.blogspot.com/2021/02/raspberry-pi-picomicropython-st7789-spi.html

"""
import uos
import machine
import st7789py as st7789
from fonts import vga2_8x8 as font1
from fonts import vga1_16x32 as font2
import random
#import dotdict
#from .dotdict import Dotdict
#from sys import exit

#SPI(1) default pins
spi1_sck=10
spi1_mosi=11
spi1_miso=8     #not use
st7789_res = 12
st7789_dc  = 13
disp_width = 240
disp_height = 240
CENTER_Y = int(disp_width/2)
CENTER_X = int(disp_height/2)

imageFile = "utaha_240.raw24"

print(uos.uname())
spi1 = machine.SPI(1, baudrate=40000000, polarity=1)
print(spi1)
display = st7789.ST7789(spi1, disp_width, disp_width,
                          reset=machine.Pin(st7789_res, machine.Pin.OUT),
                          dc=machine.Pin(st7789_dc, machine.Pin.OUT),
                          rotation=0)
  
r_width = disp_width-40
r_height = disp_height-40
for b in range(0, 255, 10):
    display.fill_rect(20, 20, r_width, r_height, st7789.color565(0, 0, b))

display.fill(st7789.BLACK)

for i in range(5000):
    display.pixel(random.randint(0, disp_width),
          random.randint(0, disp_height),
          st7789.color565(random.getrandbits(8),random.getrandbits(8),random.getrandbits(8)))

# Helper function to draw a circle from a given position with a given radius
# see https://en.wikipedia.org/wiki/Midpoint_circle_algorithm#C_example 
def draw_circle(xpos0, ypos0, rad, col=st7789.color565(255, 255, 255)):
    x = rad - 1
    y = 0
    dx = 1
    dy = 1
    err = dx - (rad << 1)
    while x >= y:
        display.pixel(xpos0 + x, ypos0 + y, col)
        display.pixel(xpos0 + y, ypos0 + x, col)
        display.pixel(xpos0 - y, ypos0 + x, col)
        display.pixel(xpos0 - x, ypos0 + y, col)
        display.pixel(xpos0 - x, ypos0 - y, col)
        display.pixel(xpos0 - y, ypos0 - x, col)
        display.pixel(xpos0 + y, ypos0 - x, col)
        display.pixel(xpos0 + x, ypos0 - y, col)
        if err <= 0:
            y += 1
            err += dy
            dy += 2
        if err > 0:
            x -= 1
            dx += 2
            err += dx - (rad << 1)
    
draw_circle(CENTER_X, CENTER_Y, 100)
   
display.text(font2, "Hello!", 10, 10)
display.text(font2, "RPi Pico", 10, 40)
display.text(font2, "MicroPython", 10, 70)
display.text(font1, "ST7789 SPI 240*240 IPS", 10, 100)
display.text(font1, "https://github.com/", 10, 110)
display.text(font1, "russhughes/st7789py_mpy", 10, 120)
    
print("- Text run end -")

#show image rgb 24 read init
rowBufSize = 20
rowStart = 0
fseekoffset = 0

#loop file read and display by rowBufSize height
while fseekoffset < disp_width * disp_height * 3 :
    fseekoffset = rowStart * disp_width * 3
    print( 'fseekoffset %d' % fseekoffset ) 
    #file open RGB stream Read
    f = open(imageFile, 'rb')
    f.seek(fseekoffset)
    content = f.read(disp_width * rowBufSize * 3) #RGB
    f.close() # closing file object
    
    if len(content) < disp_width * 3:
        break;

    #bitmapData = {'HEIGHT': 240, 'WIDTH': 240, 'BPP': 16, 'BITMAP': content}
    #bitmapDot = dotdict.Dotdict(bitmapData)
    #print(bitmapDot)
    #print(bitmapDot.HEIGHT)

    #display.bitmap( bitmapData, 0, 0, 0)
    #traversal for screen bit row->col
    #for bitrow in range(disp_height):
    bufIdx = 0
    for bitrow in range(rowStart, rowStart + rowBufSize ):
        #print( bitrow, end = ' ')
        for bitcol in range(disp_width):
            #bitidx = bitrow * disp_width * 3 + bitcol * 3
            display.pixel(bitcol, bitrow,
                st7789.color565(content[bufIdx],content[bufIdx+1],content[bufIdx+2]))
            bufIdx += 3 #read loaded buffer offset
    rowStart += rowBufSize

print("- Image run end -")
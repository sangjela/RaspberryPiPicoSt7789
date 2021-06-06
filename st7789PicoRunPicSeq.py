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
from utime import sleep

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

picseqdir = "./picseq/"
imageFile = ""
#.raw is 16 bit RGB565 raw file
picseqs = ["utaha240_0.raw",
           "utaha240_1.raw",
           "utaha240_2.raw",
           "utaha240_3.raw",
           "utaha240_4.raw",
           "utaha240_5.raw",
           "utaha240_6.raw",
           "utaha240_7.raw",
           "utaha240_8.raw",
           "utaha240_9.raw",]

print(uos.uname())
spi1 = machine.SPI(1, baudrate=40000000, polarity=1)
print(spi1)
display = st7789.ST7789(spi1, disp_width, disp_width,
                          reset=machine.Pin(st7789_res, machine.Pin.OUT),
                          dc=machine.Pin(st7789_dc, machine.Pin.OUT),
                          rotation=0)

#repeat
while True:

    #multi pic show
    for loopPic in range(0, len(picseqs)):
        
        imageFile = picseqdir + picseqs[loopPic]

        #show image rgb565 16bit read init
        rowBufSize = 40 #must be 1/n value of screen height
        rowStart = 0
        fseekoffset = 0
        pixelByte = 2

        #loop file read and display by rowBufSize height
        while fseekoffset < disp_width * disp_height * pixelByte :
            fseekoffset = rowStart * disp_width * pixelByte
            #print( 'fseekoffset %d' % fseekoffset )

            #file open RGB stream Read
            f = open(imageFile, 'rb')
            f.seek(fseekoffset)
            content = f.read(disp_width * rowBufSize * pixelByte) #RGB565 16bit
            f.close() # closing file object
            
            if len(content) < disp_width * pixelByte:
                break;

            #loaded content (buf) to screen
            display.blit_buffer(content, 0, rowStart, disp_width, rowBufSize)

            rowStart += rowBufSize

        sleep(0.15)

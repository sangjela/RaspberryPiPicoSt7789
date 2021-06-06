"""
noto_fonts Writes the names of three Noto fonts centered on the display
    using the font. The fonts were converted from True Type fonts using
    the font2bitmap utility.
"""

from machine import SoftSPI, Pin, SPI
from time import sleep
import st7789py as st7789

from truetype import NotoSans_32 as noto_sans

#not enough disk, so I delete some truetype fonts
#from truetype import NotoSerif_32 as noto_serif
#from truetype import NotoSansMono_32 as noto_mono


def notoShow():
    
    #SPI(1) default pins
    spi1_sck=10
    spi1_mosi=11
    spi1_miso=8     #not use
    st7789_res = 12
    st7789_dc  = 13
    disp_width = 240
    disp_height = 240    

    def center(font, string, row, color=st7789.WHITE):
        screen = tft.width                        # get screen width
        width = tft.write_width(font, string)     # get the width of the string
        if width and width < screen:              # if the string < display
            col = tft.width // 2 - width // 2     # find the column to center
        else:                                     # otherwise
            col = 0                               # left justify

        tft.write(font, string, col, row, color)  # and write the string

    try:
        spi = SPI(1, baudrate=40000000, polarity=1)
        tft = st7789.ST7789(
            spi,
            disp_width,
            disp_height,
            reset=Pin(st7789_res, Pin.OUT),
            #cs=Pin(5, Pin.OUT),
            dc=Pin(st7789_dc, Pin.OUT),
            #backlight=Pin(4, Pin.OUT),
            rotation=0)

        # enable display and clear screen
        tft.fill(st7789.CYAN)        

        row = 16

        # center the name of the first font, using the font
        center(noto_sans, "NotoSans", row, st7789.RED)
        row += noto_sans.HEIGHT

        #not enough disk, so I delete some truetype fonts
        # center the name of the second font, using the font
        #center(noto_serif, "NotoSerif", row, st7789.GREEN)
        #row += noto_serif.HEIGHT

        # center the name of the third font, using the font
        #center(noto_mono, "NotoSansMono", row, st7789.BLUE)
        #row += noto_mono.HEIGHT
        
        # center the name of the first font, using the font, 한글출력시도 -> 안됨.
        center(noto_sans, "Cannot Korean", row, st7789.RED) #
        row += noto_sans.HEIGHT

    finally:
        # shutdown spi
        if 'spi' in locals():
            spi.deinit()
    sleep(2)

notoShow()

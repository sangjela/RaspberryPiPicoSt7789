"""
Original Source http://www.penguintutor.com/programming/picodisplayanimations
Using Python PNG to read PNG files

https://stackoverflow.com/questions/31142919/how-to-install-the-png-module-in-python/31143108
install png module for python
pip install pypng
   OR
sudo pip3 install pypng
"""

#PNG to RGB565 16bit color Raw Data
import png

#infile = "penguintutorlogo-pico.png"
infile = "utaha_240.png"
#outfile = "logo-image.raw"
outfile = "utaha_240.raw"

def color_to_bytes (color):
    r, g, b = color
    arr = bytearray(2)
    arr[0] = r & 0xF8
    arr[0] += (g & 0xE0) >> 5
    arr[1] = (g & 0x1C) << 3
    arr[1] += (b & 0xF8) >> 3
    return arr

png_reader=png.Reader(infile)
image_data = png_reader.asRGBA8()

with open(outfile, "wb") as file:
    #print ("PNG file \nwidth {}\nheight {}\n".format(image_data[0], image_data[1]))
    #count = 0
    for row in image_data[2]:
        for r, g, b, a in zip(row[::4], row[1::4], row[2::4], row[3::4]):
            #print ("This pixel {:02x}{:02x}{:02x} {:02x}".format(r, g, b, a))
            # convert to (RGB565)
            img_bytes = color_to_bytes ((r,g,b))
            file.write(img_bytes)

file.close()
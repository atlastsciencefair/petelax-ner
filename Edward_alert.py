import requests
import http.client, urllib
import os
import glob
import time
import argparse
from time import sleep
from colour import Color

from Adafruit_AMG88xx import Adafruit_AMG88xx
from PIL import Image, ImageDraw

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
 
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c


# parse command line arguments
parser = argparse.ArgumentParser(description='Take a still image.')
parser.add_argument('-o','--output', metavar='filename', default='amg88xx_still.jpg', help='specify output filename')
parser.add_argument('-s','--scale', type=int, default=2, help='specify image scale')
parser.add_argument('--min', type=float, help='specify minimum temperature')
parser.add_argument('--max', type=float, help='specify maximum temperature')
parser.add_argument('--report', action='store_true', default=False, help='show sensor information without saving image')

args = parser.parse_args()
    
# sensor setup
NX = 8
NY = 8
sensor = Adafruit_AMG88xx()

# wait for it to boot
sleep(.1)

# get sensor readings  
pixels = sensor.readPixels()

if args.report:
    print "Min Pixel = {0} C".format(min(pixels))
    print "Max Pixel = {0} C".format(max(pixels))
    print "Thermistor = {0} C".format(sensor.readThermistor())
    exit()

# output image buffer
image = Image.new("RGB", (NX, NY), "white")
draw = ImageDraw.Draw(image)

# color map
COLORDEPTH = 256
colors = list(Color("indigo").range_to(Color("red"), COLORDEPTH))
colors = [(int(c.red * 255), int(c.green * 255), int(c.blue * 255)) for c in colors]

#some utility functions
def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))

def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

# map sensor readings to color map
MINTEMP = min(pixels) if args.min == None else args.min
MAXTEMP = max(pixels) if args.max == None else args.max
pixels = [map(p, MINTEMP, MAXTEMP, 0, COLORDEPTH - 1) for p in pixels]

# create the image
for ix in xrange(NX):
    for iy in xrange(NY):
        draw.point([(ix,iy%NX)], fill=colors[constrain(int(pixels[ix+NX*iy]), 0, COLORDEPTH- 1)])

# scale and save
image.resize((NX*args.scale, NY*args.scale), Image.BICUBIC).save(args.output)

car_on = True
temp = read_temp 
i = 0
while car_on == True:
    i += 1
    #change the number after >= to change temperature that alert the phone at.
    if read_temp() >= 0:
        r = requests.post("https://api.pushover.net/1/messages.json", data={
            "token":"aajaiutjvx1fwdqy15g2nqcp6av8dt",
            "user":"usqmx1mv4pams23f4nq8igh5a7okzf",
            "message":"Your vehicle has reached a DANGEROUS temperature. Please return to your vehicle."}, 
        files={"attachment":open("/home/pi/Desktop/thermal_pic.jpg","rb")})
        exit()

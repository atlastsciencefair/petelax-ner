import http.client, urllib
import os
import glob
import time
 
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
    


car_on = True
temp = read_temp 
i = 0
while car_on == True:
    i += 1
    #change the number after >= to change temperature that alert the phone at.
    if read_temp() >= 0:
        conn = http.client.HTTPSConnection("api.pushover.net:443")
        conn.request("POST", "/1/messages.json",
            urllib.parse.urlencode({
                "token": "aajaiutjvx1fwdqy15g2nqcp6av8dt",
                "user": "usqmx1mv4pams23f4nq8igh5a7okzf",
	        "message": "Your vehicle has reached a DANGEROUS temperature. Please return to your vehicle.",
            }), { "Content-type": "application/x-www-form-urlencoded" })
        conn.getresponse()
    if i >= 1:
        #spam = input("would you like to continue to spam: ")
        #if spam.strip() == "no" or "n":
        exit()
        
	

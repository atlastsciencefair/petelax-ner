import picamera     # Importing the library for camera module
from time import sleep  # Importing sleep from time library to add delay in program

camera = picamera.PiCamera()    # Setting up the camera

camera.start_preview()      # You will see a preview window while recording
camera.start_recording('/home/pi/Videos/test3.h264') # Video will be saved at videos
sleep(10)
camera.stop_recording()
camera.stop_preview()

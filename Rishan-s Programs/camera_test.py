from picamera import PiCamera
from time import sleep

camera = PiCamera()

camera.resolution = (200, 200)
#camera.start_preview()
#sleep(5)
camera.capture('/home/pi/Desktop/image.png',format='png')
#camera.stop_preview()
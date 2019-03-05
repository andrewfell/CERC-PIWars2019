from picamera import PiCamera
from time import sleep

camera = PiCamera()

camera.resolution = (400, 400)
#camera.start_preview()
#sleep(5)

camera.capture('/home/pi/Pictures/image.png',format='png')
#camera.stop_preview()

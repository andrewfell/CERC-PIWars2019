from picamera import PiCamera
from time import sleep
from subprocess import call 
camera = PiCamera()

camera.resolution = (400, 400)
#camera.start_preview()
filecnt=1
img_dest = "/home/pi/colour.png"
for i in range(20):
    print(i)
    camera.capture(img_dest,format='png')
    #camera.stop_preview()
    img_tg= "/home/pi/Pictures/image" + str(filecnt) + ".png"
    filecnt = filecnt + 1
    call(["cp", img_dest, img_tg])
    sleep(3)      

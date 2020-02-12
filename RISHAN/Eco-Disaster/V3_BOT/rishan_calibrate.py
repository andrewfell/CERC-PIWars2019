from picamera import PiCamera
from time import sleep
from subprocess import call 
camera = PiCamera()

camera.resolution = (400, 400)
camera.rotation = 180
filecnt=1
img_dest = "/home/pi/colour.png"
for i in range(5):
    print(filecnt)
    camera.start_preview()
    sleep(4)
    camera.capture(img_dest,format='png')
    camera.stop_preview()
    img_tg= "/home/pi/Pictures/img-" + str(filecnt) + ".png"
    filecnt = filecnt + 1
    call(["cp", img_dest, img_tg])
    sleep(1)      

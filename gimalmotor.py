import RPi.GPIO as GPIO			# using Rpi.GPIO module
from time import sleep			# import function sleep for delay
#GPIO.setmode(GPIO.BCM)			# GPIO numbering
GPIO.setwarnings(False)			# enable warning from GPIO
GPIO.setmode(GPIO.BOARD)
AN1 = 33				# set pwm1 pin on MD10-hat
DIG1 = 32				# set dir1 pin on MD10-Hat
EN1 = 23
GPIO.setup(AN1, GPIO.OUT)		# set pin as output
GPIO.setup(DIG1, GPIO.OUT)		# set pin as output
GPIO.setup(EN1, GPIO.OUT)		# set pin as output

sleep(1)				# delay for 1 seconds
p1 = GPIO.PWM(AN1, 5000)			# set pwm for M1

try:					
  while True:
    GPIO.output(EN1, GPIO.HIGH)		# set DIG1 as HIGH, M1B will turn ON
    print ("Left")				# display "Forward" when programe run
    GPIO.output(DIG1, GPIO.HIGH)		# set DIG1 as HIGH, M1B will turn ON
    p1.start(50)			# set speed for M1 at 100%
    sleep(2)				#delay for 2 second
    # print ("Forward")
    # GPIO.output(DIG1, GPIO.LOW)          # set DIG1 as LOW, to control direction
    # p1.start(50)                        # set speed for M1 at 100%
    # sleep(2)                             #delay for 2 second                           #delay for 2 second

    # print ("STOP")
    # GPIO.output(DIG1, GPIO.LOW)          # Direction can ignore
    # GPIO.output(EN1, GPIO.LOW)		# set DIG1 as HIGH, M1B will turn ON
    # p1.start(0)                          # set speed for M1 at 0%
    # sleep(3)                             #delay for 3 second
except KeyboardInterrupt:					# exit programe when keyboard interupt
  GPIO.output(EN1, GPIO.LOW)
  p1.start(0)				# set speed to 0
except:					# exit programe when keyboard interupt
  GPIO.output(EN1, GPIO.LOW)
  p1.start(0)
finally:
  GPIO.output(EN1, GPIO.LOW)
  p1.start(0)		
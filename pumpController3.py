import RPi.GPIO as GPIO ## Import GPIO Library
import time ## Import 'time' library.  Allows us to use 'sleep'
import datetime
import FileLogger

# Start File Logger
global logger
logger = FileLogger.startLogger("/var/www/pumpController3.log", 5000, 5)
logger.info("Starting Logger...")

logger.info(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + "Script Started" )
time.sleep(1)

GPIO.setmode(GPIO.BOARD) ## Use BOARD pin numbering
gpio_pump=36
gpio_valveone=38
gpio_valvetwo=40

GPIO.setwarnings(False)
GPIO.setup(gpio_pump, GPIO.OUT)
GPIO.output(gpio_pump, True)
GPIO.setup(gpio_valveone, GPIO.OUT) 
GPIO.output(gpio_valveone, True) 
GPIO.setup(gpio_valvetwo, GPIO.OUT) 
GPIO.output(gpio_valvetwo, True) 

script_path = "/home/pi/Aquaponics/PiPonics/"
valveone_file = script_path + "valve1.txt"
valvetwo_file = script_path + "valve2.txt"

with open(valveone_file, "r+") as fo:
	fo.seek(0, 0)
	fo.write("0")
fo.closed
	
with open(valvetwo_file, "r+") as fo:
	fo.seek(0, 0)
	fo.write("0")
fo.closed


## Define function wateringcycle
def wateringcycle(valveone_time,wait_time,valvetwo_time,pause_time,cycle_count):
	if cycle_count == 0:
		cycle_count=999
	
	for i in range(0,cycle_count): ## Run loop numTimes

		## Valve One Cycle
		print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Valve One Open For " + str(valveone_time*60) + " Seconds "
		logger.info(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Valve One Open For " + str(valveone_time*60) )
                GPIO.output(gpio_valveone, False) ## Open Valve One
		GPIO.output(gpio_pump, False) ## Turn on pump
		with open(valveone_file, "r+") as fo:
			fo.seek(0, 0)
			fo.write("1")
		fo.closed
		
		time.sleep(valveone_time*60) ## valve  timer
		
		print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Valve One Closed "
		logger.info(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Valve One Closed ")
                GPIO.output(gpio_valveone, True)
		GPIO.output(gpio_pump, True) ## Switch off GPIO 
		with open(valveone_file, "r+") as fo:
			fo.seek(0, 0)
			fo.write("0")
		fo.closed

		## Wait Period
		print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Time Before Next Valve " + str(wait_time*60) + " Seconds "
		logger.info(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Time Before Next Valve " + str(wait_time*60))

		time.sleep(wait_time*60) ## Wait For Growbed to Drain

		## Valve Two Cycle
		print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Valve Two Open For " + str(valvetwo_time*60) + " Seconds "
		logger.info(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Valve Two Open For " + str(valvetwo_time*60) )
                GPIO.output(gpio_valvetwo, False) ## Opem Valve Two
		GPIO.output(gpio_pump, False) ## Turn on pump
		with open(valvetwo_file, "r+") as fo:
			fo.seek(0, 0)
			fo.write("1")
		fo.closed
		
		time.sleep(valvetwo_time*60) ## Valve Two Timer
		
		print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Valve Two Closed "
		logger.info(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Valve Two Closed ")
                GPIO.output(gpio_valvetwo, True)
		GPIO.output(gpio_pump, True) ## Switch off GPIO 
		with open(valvetwo_file, "r+") as fo:
			fo.seek(0, 0)
			fo.write("0")
		fo.closed
		
		print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Time Before Next Valve " + str(pause_time*60) + " Seconds " 
		logger.info(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Time Before Next Valve " + str(pause_time*60) )

		time.sleep(pause_time*60) ## Wait For Growbed to Drain

	print "Done" ## When loop is complete, print "Done"
	GPIO.cleanup()

## Prompt user for input
## uncoment for dynamic input
##valveone_time_input = raw_input("Minutes To Hold Valve One Open: ")
##wait_time_input = raw_input("Minutes to wait before watering the next growbed?: ")
##valvetwo_time_input = raw_input("Minutes To Hold Valve Two Open: ")
##pause_time_input = raw_input("Minutes to wait before watering the next growbed?: ")
##cycle_count_input = raw_input("How many cycles: ")
	
## uncomment for hybrid input
##valveone_time_input = 1.5
##wait_time_input = 5
##valvetwo_time_input = 1.75
##pause_time_input = 22.25
##cycle_count_input = raw_input("How Many Cycles: ")
	
## uncomment for static input
valveone_time_input = .025
wait_time_input = .025
valvetwo_time_input = .025
pause_time_input = .025
cycle_count_input = 5000000

wateringcycle(float(valveone_time_input),float(wait_time_input),float(valvetwo_time_input), float(pause_time_input),int(cycle_count_input))

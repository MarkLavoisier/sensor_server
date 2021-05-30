#rm temp
#just time 

import serial
import time
from  mail import sendEmail
import datetime
import os
import RPi.GPIO as GPIO
import socket

#HOST  = '39.124.30.130'
#PORT = 5055

#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#print("socket created")

#try:
#	s.bind((HOST, PORT))
#except socket.error:
#	print ('Bind failed ')

#s.listen(5)
#print ('Socket awaiting messages')
#(conn, addr) = s.accept()
#print ('Connected')

GPIO.setwarnings(False)
#ser = serial.Serial('/dev/ttyUSB0',9600)
valtime=600
prev=0
datedata_1= None
datedata_2= None
datedata_3 =None
days_elapsed=7
path_target = '/home/pi/sensor_server/save_log/'
state =1

delay=0
cpu_pin=40
GPIO.setmode(GPIO.BOARD)
GPIO.setup(cpu_pin,GPIO.OUT)

while True:
#	prt = time.time()
#	while time.time()-prt<5:
#		nothing=1
#	os.system("clear")
	print (str(datetime.datetime.now())) #date and time
	f_time_title_name = datetime.datetime.now().strftime("%Y-%m-%d-%a-%H-%M")
	path = '/home/pi/sensor_server/save_log/'
	f_n = path+f_time_title_name
	log_file = open(f_n,'a')
	f_log_time = str(datetime.datetime.now())
	log_file.write(f_log_time)
	temp = os.popen("vcgencmd measure_temp").readline()
	result = temp.replace("temp=","").replace("'C\n", "")
	c_t=float(result)
	SunTime = datetime.datetime.now().strftime("%H")
	night_time= (int(SunTime) < 7) or (int(SunTime) > 22)
	temp = 55
	if night_time:
		if c_t > 60:
			GPIO.output(cpu_pin,0)
		else:
			print ("fan off")
			GPIO.output(cpu_pin,1)
			log_file.write('\nfan off \n')
		 
	else:
		if c_t >= 55: #fan func
			fan_operate=2
			print ("fan on")
			GPIO.output(cpu_pin,0)
			log_file.write('\nfan on \n') 
		elif c_t <= 48 :
#		else:
			fan_operate=1
			print ("fan off")
			GPIO.output(cpu_pin,1)
			log_file.write('\nfan off \n')
		
	print ("night time : " + str(night_time))
	print ("suntime : " + SunTime)
	print ("cpu temp : %2.1f"% float(result)) #cpu temp
	f_log_temp = "cpu temp : %2.1f \n"% float(result)
	log_file.write(f_log_temp) #log temp

	#result_f = result.decode()[:-2]
	#print(result_f+2)
	
	result=(float(result)*100) #+fan_operate

#	os.system("clear")

	log_file.write('\n')

	for f in os.listdir(path_target):
		f = os.path.join(path_target, f)
		if os.path.isfile(f):
			timestamp_now = datetime.datetime.now().timestamp()
			is_old = os.stat(f).st_mtime < timestamp_now - (days_elapsed  * 24 * 60 * 60)
			if is_old:
				os.remove(f)
				print (f, 'is deleted')
				f_rm = f + 'is deleted\n'
				log_file.write(f_rm)

	log_file.close()
#conn.close() 

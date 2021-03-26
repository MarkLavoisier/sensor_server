import serial
import time
from  mail import sendEmail
import datetime
import os
import RPi.GPIO as GPIO
import socket

HOST  = '39.124.30.130'
PORT = 5055

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("socket created")

try:
	s.bind((HOST, PORT))
except socket.error:
	print ('Bind failed ')

s.listen(5)
print ('Socket awaiting messages')
(conn, addr) = s.accept()
print ('Connected')

GPIO.setwarnings(False)
ser = serial.Serial('/dev/ttyUSB0',9600)
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
		if c_t >= 50: #fan func
			fan_operate=2
			print ("fan on")
			GPIO.output(cpu_pin,0)
			log_file.write('\nfan on \n') 
		elif c_t <= 40 :
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

#	datedata = datetime.datetime.now().strftime("%m%d0%w%H%M%S")
	if state == 1:
		datedata_1 = datetime.datetime.now().strftime("%m%d1")
		print ("datedata_1 : " + datedata_1)
		state = 2
	elif state ==2 :
		datedata_2 = datetime.datetime.now().strftime("%H%M2")
		print ("datedata_2 : " + datedata_2)
		state = 3
	elif state == 3:
		datedata_3 = datetime.datetime.now().strftime("%w4")
		print ("datedata_3 : " + datedata_3)
		state = 1
#	print ("server print : " + datedata_1)
#	print ("server print : " + datedata_2)
#	print ("temp and fan func : %4.0f" % result)
	t_f_func = "temp and fan func : %4.0f \n" % result
	log_file.write(t_f_func)
	#ser.write(str(result).encode("utf-8"))
	if int(datetime.datetime.now().strftime("%S")) <= 4:
		datedata_2 = datetime.datetime.now().strftime("%H%M2")
		print ("on time datedata : " + datedata_2)
		msg = "on time datedata : " + datedata_2
		log_file.write(msg)
		ser.write(str(datedata_2).encode("utf-8"))
		
	else:
		if state == 1:
			ser.write(str(datedata_1).encode("utf-8"))
		elif state == 2:
			ser.write(str(datedata_2).encode("utf-8"))
		elif state == 3:
			ser.write(str(datedata_3).encode("utf-8"))
	
	val = ser.readline()
	os.system("clear")
	svr = val.decode()[:-2]
#	i_svr = int(svr)
#	print (i_svr)
	f_svr = float(svr)
	print (int(f_svr))
	
	str_f_svr = str(int(f_svr))
	#conn.sendall(str_f_svr.encode('utf-8'))
	#now=time.time()
	#if now-delay>:
	#	delay=now
	conn.sendall(str_f_svr.encode('utf-8'))
	print("socket send !-----------------------")
	
#	print ("Server Serial value  : %8.0f" % f_svr)
	serial_val = "Serial value  : %8.0f \n" % f_svr
	log_file.write(serial_val)
	
	h = ( f_svr / 10000) * 0.01
	t = ( f_svr % 10000) * 0.01
	print ("Humd : %2.2f %%" % h+"  //  Temp : %2.2f C" % t)
	
	t_h_log = "Humd : %2.2f %%" % h+"  //  Temp : %2.2f C \n" % t
	log_file.write(t_h_log)
#	if time.time()-prev > valtime:
#		prev=time.time()
#		sendEmail(h,t,c_t)
#		print ("done-------------------------------------------------------!")
#		log_file.write('done--------------------------------------!')
#	print (" ")
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
conn.close() 

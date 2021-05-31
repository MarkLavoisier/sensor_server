import serial
import time
import datetime
import os

ser = serial.Serial('/dev/ttyUSB0',9600)
while True:
	print (str(datetime.datetime.now()))
	temp = os.popen("vcgencmd measure_temp").readline()
	result = temp.replace("temp=","").replace("'C\n", "")
	c_t=float(result)
	print ("cpu temp : %2.1f"% float(result))

	#result_f = result.decode()[:-2]
	#print(result_f+2)
	ser.write(result.encode("utf-8"))

	val = ser.readline()
	svr = val.decode()[:-2]
	f_svr = float(svr)
	#print (f_svr)
	print ("Serial value  : %8.0f" % f_svr)
	h = ( f_svr / 10000) * 0.01
	t = ( f_svr % 10000) * 0.01
	print ("Humidity 습도 : %2.2f %%" % h+"  //  Temperature 온도 : %2.2f C" % t)
	print (" ")

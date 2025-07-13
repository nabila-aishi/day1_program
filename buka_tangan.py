from motor_latihan_pid import motor
from CMPS14 import Compass
from pathlib import Path
import depthai as dai
#from brping import Ping1D
import numpy as np
import time
import cv2


#my_ping = Ping1D() 

try:
    #my_ping.connect_serial("/dev/ttyUSB1", 115200)
    arduino = motor('/dev/ttyUSB0', 115200)
except:
    #my_ping.connect_serial("/dev/ttyUSB0", 115200)
    arduino = motor('/dev/ttyUSB1', 115200)

#if not my_ping.initialize():
#    print("Gagal menginisialisasi Ping Sonar!")
#    exit(1)
    
time.sleep(1)
arduino.send_command_serial_once('rpi 1;', 'ino_oke')

print(Compass().azimuth())

dt_1 = 70
dt_2 = 90
kecepatan = 1530 #kecepatan untuk maju
kecepatan_turun = 1487 #kecepatan untuk turun
kecepatan_geser_R = 1480 #kecepatan untuk geser kanan
kecepatan_geser_L = 1515 #kecepatan untuk geser kiri

timer_maju1 = 5  #maju mendekati 

batas_gawang = 7.5

target_heading1 = int(input('Target_Heading depan='))

str(input('siap?'))

arduino.data_function(target_heading1, 1, False)
arduino.motor_config(target_heading1, kecepatan, kecepatan_turun)
arduino.change_depth(dt_1)
time.sleep(0.5)

main_loop = True
var_loop = 'turun'

while main_loop:
    if var_loop == 'turun':
        print(var_loop)
        arduino.loop_perintah(var_loop)
        arduino.co_serial(arduino.send_da)
        time.sleep(2)
        var_loop = 'maju'
            
    elif var_loop == 'maju':
        print(var_loop)            
        arduino.motor_function_timer(target_heading1,timer_maju1, kecepatan, kecepatan_turun,"maju")
        arduino.rubah()
        var_loop = "turun_ember"
        
    #elif var_loop == "maju_transduser":
    #    distance = my_ping.get_distance_simple()
    #    arduino.motor_function_gerak(target_heading1, kecepatan, kecepatan_turun,"maju")
    #    if distance and 'distance' in distance:                                   
    #        jarak = distance['distance']
    #        if (jarak <= 5000) :
    #            arduino.rubah()
    #            print("terlalu dekat tembok kiri")
    #            arduino.loop_perintah("stop")
    #            time.sleep(1.5)
    #            var_loop = "turun_ember"
        
    elif var_loop == "turun_ember":
        print(var_loop)
        arduino.change_depth(dt_2)
        time.sleep(0.5)
        arduino.co_serial(arduino.send_da)
        time.sleep(1.5)
        var_loop = "buka_tangan"
        
    elif var_loop == "buka_tangan":
        print(var_loop)
        arduino.co_serial(arduino.send_da)
        time.sleep(0.5)
        arduino.co_serial(arduino.send_buka_tangan) 
        time.sleep(1)
        var_loop = "naik"
       
    elif var_loop == 'naik':
        print(var_loop)
        arduino.loop_perintah(var_loop)
        var_loop ='destroy'

    elif var_loop == "destroy":
        print(var_loop)
        arduino.loop_perintah(var_loop)
        print("AUV selesai naik.")
        main_loop = False 
        
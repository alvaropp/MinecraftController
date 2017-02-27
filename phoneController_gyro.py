# Alvaro Perez, 2017
# - Sensor part of the code based on code by Axel Lorenz
# https://play.google.com/store/apps/details?id=de.lorenz_fenster.sensorstreamgps&hl=en_GB

import socket
import pyautogui as pag
import time


def getOrientation(s):
    # Assume a received string of the form:
    # [time,3,accX,accY,accZ,4,gyroX,giroY,giroZ,5,magX,magY,magZ]
    valueList = [x.strip() for x in s.split(',')]
    gyro = valueList[6:9]
    print(gyro)
    return gyro

def processOrientation(gyro):
    # Forward & backward movement
    gyro = [float(gyro[0]), float(gyro[1]), float(gyro[2])] 
    if 35 < float(gyro[2]) < 90:
        # pag.keyDown('w')
        #time.sleep(0.05)
        pag.keyUp("w")            
    elif -90 < float(gyro[2]) < -35:
        # pag.keyDown('s')
        #time.sleep(0.05)
        pag.keyUp("s")
    
    # Sideways motion
    if abs(gyro[0]) > 0.2:
        pag.moveRel(0, -100*gyro[0], 0.001)
    if abs(gyro[2]) > 0.2:
        pag.moveRel(-75*gyro[2], 0, 0.001)

if __name__ == "__main__":
    host = ''
    port = 5555

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.bind((host, port))
    
    while True:
        try:
            message, address = s.recvfrom(8192)
            message = str(message)
            gyro = getOrientation(message)
            if gyro:
                processOrientation(gyro)
        except:
            raise


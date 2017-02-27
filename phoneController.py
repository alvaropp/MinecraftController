# Alvaro Perez, 2017
# - Sensor part of the code based on code by Axel Lorenz
# https://play.google.com/store/apps/details?id=de.lorenz_fenster.sensorstreamgps&hl=en_GB
# - Keyboard press based on code from Phylliida
# stackoverflow.com/questions/13564851/generate-keyboard-events

import socket
import pyautogui as pag
import time


def getOrientation(s):
    # Assume a received string of the form:
    # [time,3,accX,accY,accZ,5,magX,magY,magZ,81,orientX,orientY,orientZ]
    valueList = [x.strip() for x in s.split(',')]
    orient = valueList[-3:]
    orient[-1] = orient[-1][:-1]
    print(orient)
    return orient

def processOrientation(orient):
    # Forward & backward movement
    if 35 < float(orient[2]) < 90:
        pag.keyDown('w')
        #time.sleep(0.05)
        pag.keyUp("w")            
    elif -90 < float(orient[2]) < -35:
        pag.keyDown('s')
        #time.sleep(0.05)
        pag.keyUp("s")
    
    # Sideways motion
    rotDev = screenAngle - float(orient[1])
    if rotDev > 30:
        # Rotate left
        pag.moveRel(-40,0)
    elif rotDev < -30:
        # Rotate right
        pag.moveRel(40,0)


if __name__ == "__main__":
    host = ''
    port = 5555

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.bind((host, port))
    
    # Calibrate screen direction
    input("Calibrating: stand still and hold the phone vertical towards the screen")
    try:
        message, address = s.recvfrom(8192)
        message = str(message)
        orient = getOrientation(message)
        screenAngle = float(orient[1])
    except:
        raise

    input("Calibrated")
    while True:
        try:
            message, address = s.recvfrom(8192)
            message = str(message)
            orient = getOrientation(message)
            processOrientation(orient)
        except:
            raise



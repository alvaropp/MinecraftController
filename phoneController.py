# Alvaro Perez, 2017
# - Sensor part of the code based on code by Axel Lorenz
# https://play.google.com/store/apps/details?id=de.lorenz_fenster.sensorstreamgps&hl=en_GB
# - Keyboard press based on code from Phylliida
# stackoverflow.com/questions/13564851/generate-keyboard-events

import socket
import pyautogui as pag
import time


def processOrientation(orient):
    print(float(orient[0]), screenAngle-float(orient[1]), float(orient[2]))
    # Forward & backward movement
    if 35 < orient[2] < 90:
        pag.keyDown('w')
        time.sleep(0.06)
        pag.keyUp("w")            
    elif -90 < orient[2] < -35:
        pag.keyDown('s')
        time.sleep(0.06)
        pag.keyUp("s")
    
    # Sideways motion
    rotDev = screenAngle - orient[1]
    if rotDev > 30:
        # Rotate left
        pag.moveRel(-20, 0, 0.1)
    elif rotDev < -30:
        # Rotate right
        pag.moveRel(20, 0 ,0.1)


if __name__ == "__main__":
    host = ''
    port = 5555

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.bind((host, port))
    

    # Calibrate screen direction
    input("Calibrating: stand still and hold the phone vertically towards the screen")
    try:
        while True:
            message, address = s.recvfrom(128)
            message = str(message)[:-1]
            message = [x.strip() for x in message.split(',')]
            print(len(message), message)
            if len(message) == 17:
                orient = [float(x) for x in message[-3:]]
                screenAngle = float(orient[1])
                break;
    except:
        raise

    input("Calibrated, angles: {}, screenAngle: {}".format(orient, screenAngle))
    while True:
        try:
            message, address = s.recvfrom(128)
            message = str(message)[:-1]
            message = [x.strip() for x in message.split(',')]
            if len(message) == 17:
                orient = [float(x) for x in message[-3:]]
                processOrientation(orient)
        except:
            raise


# Alvaro Perez-Diaz, 2017

# - Sensor part of the code based on code by Axel Lorenz
# https://play.google.com/store/apps/details?id=de.lorenz_fenster.sensorstreamgps&hl=en_GB
#
# - MCPIPY reference at
# http://www.stuffaboutcode.com/p/minecraft-api-reference.html

import socket
import time
import mcpi.minecraft as minecraft


def processOrientation(orient):
    print(float(orient[0]), screenAngle-float(orient[1]), float(orient[2]))
    # Forward & backward movement
    if 35 < orient[2] < 90:
        # Forward
        playerPos = mc.player.getPos()
        playerDir = mc.player.getDirection().__mul__(0.12)
        mc.player.setPos(playerPos + playerDir)
        time.sleep(0.005)
    elif -90 < orient[2] < -35:
        # Backward
        playerPos = mc.player.getPos()
        playerDir = mc.player.getDirection().__mul__(0.12)
        mc.player.setPos(playerPos - playerDir)
        time.sleep(0.005)

    # Sideways motion
    rotDev = screenAngle - orient[1]
    if rotDev > 30:
        # Rotate left
        mc.player.setRotation(mc.player.getRotation() - 3)
    elif rotDev < -30:
        # Rotate right
        mc.player.setRotation(mc.player.getRotation() + 3)


if __name__ == "__main__":

    # Initialise connection to mobile phone
    host = ''
    port = 5555
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.bind((host, port))
    
    # Initialise connection to Minecraft running Forge and RaspberryJam-Mod
    mc = minecraft.Minecraft.create()

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

    # Main loop
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


from mpu6050 import mpu6050
from time import sleep
import math

sensor = mpu6050(0x68)
DELAY = 0.5 

MAX_ACCEL = 10

def angle_from_accel(accel):
    if accel > 0:
        x = min(accel, MAX_ACCEL) # Prevent app crash by using max cos alpha = 1.0
    else:
        x = max(accel, -MAX_ACCEL)

    #if x < accel:
    #    print ("OVERFLOW, x=", accel)

    alpha = math.acos(x / MAX_ACCEL) - math.pi / 2 # x = MAX * cos beta, beta= pi2 - alpha
    return alpha * 180 / math.pi # Convert to deg


def get_angles():
    accel_data = sensor.get_accel_data()
    alpha = angle_from_accel(accel_data['x']) * 90/84.3 + 6  # Correction for shabby soldering
    beta = angle_from_accel(accel_data['y'])

    return alpha, beta

if __name__ == '__main__':
    while(True):
        alpha, beta = get_angles()
        print("Kąt alfa: %.0f, Kąt beta: %.0f" % (alpha, beta))
        sleep(DELAY)

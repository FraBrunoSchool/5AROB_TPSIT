import RPi.GPIO as GPIO
import time
#from AlphaBot import AlphaBot

#Ab = AlphaBot

DR = 16
DL = 19

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(DR, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(DL, GPIO.IN, GPIO.PUD_UP)

stato_prec = "stop"
while True:
    print(stato_prec)
    DR_status = GPIO.input(DR)
    DL_status = GPIO.input(DL)
    print(f"DR_status: {DR_status} - DL_status: {DL_status}")
    if DL_status == 1 and DR_status == 1 and stato_prec != "libero":
        # tutto libero
        stato_prec="libero"
        print("Cambio: Davanti libero")
    if DL_status == 0 and DR_status == 0 and stato_prec != "occupato":
        # ostacolo davanti
        stato_prec="occupato"
        print("Cambio: Davanti occupato")
    if DL_status == 1 and DR_status == 0 and stato_prec != "sx_libero":
        # ostacolo davanti
        stato_prec = "sx_libero"
        print("Cambio: sx_libero")
    if DL_status == 0 and DR_status == 1 and stato_prec != "dx_libero":
        # ostacolo davanti
        stato_prec = "dx_libero"
        print("Cambio: dx_libero")
    time.sleep(1)


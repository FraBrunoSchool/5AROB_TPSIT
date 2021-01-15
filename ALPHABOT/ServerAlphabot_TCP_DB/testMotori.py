from Classi.AlphaBot import AlphaBot
import time

if __name__ == '__main__':
    Ab = AlphaBot()

    # angolo di 45 con sleep di 0.5
    # angolo di 90 con sleep di 0.8
    print("Sinistra")
    Ab.right()
    time.sleep(0.8)

    """print("Destra")
    Ab.set_pwm_a(22.5)
    Ab.set_pwm_b(22.5)
    Ab.right()
    time.sleep(0.5)"""

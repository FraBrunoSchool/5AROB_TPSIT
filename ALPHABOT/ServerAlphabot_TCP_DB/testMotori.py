from AlphaBot import AlphaBot
import time

if __name__ == '__main__':

    Ab = AlphaBot()

    """print("Avanti")
    Ab.set_pwm_a(100)
    Ab.set_pwm_b(100)
    Ab.forward()
    time.sleep(1)"""

    print("Sinistra")
    Ab.set_pwm_a(90)
    Ab.set_pwm_b(0)
    Ab.left()
    time.sleep(1)
    Ab.stop()

    """print("Indietro")
    Ab.set_pwm_a(100)
    Ab.set_pwm_b(100)
    Ab.backward()
    time.sleep(1)"""
    """"
    print("Destra")
    Ab.set_pwm_a(45)
    Ab.set_pwm_b(45)
    Ab.right()
    time.sleep(1)
    """
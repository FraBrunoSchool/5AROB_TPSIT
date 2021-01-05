from Classi.AlphaBot import AlphaBot
import time

if __name__ == '__main__':
    Ab = AlphaBot()

    """print("Avanti")
    Ab.set_pwm_a(25)
    Ab.set_pwm_b(25)
    Ab.forward()
    time.sleep(1)"""

    print("Sinistra")
    Ab.set_pwm_a(90)
    Ab.set_pwm_b(90)
    Ab.left()
    time.sleep(0.5)

    """print("Indietro")
    Ab.set_pwm_a(100)
    Ab.set_pwm_b(100)
    Ab.backward()
    time.sleep(1)"""

    """print("Destra")
    Ab.set_pwm_a(22.5)
    Ab.set_pwm_b(22.5)
    Ab.right()
    time.sleep(0.5)"""

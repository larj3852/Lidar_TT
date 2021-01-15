import threading
import RPi.GPIO as GPIO
import time

class PWM1(threading.Thread):
    """
    Clase para el control de los motores vibradores
    necesita como entrada una lista con el porcentaje
    del ciclo al que trabajará cada vibrador,
    de izquierda a derecha.
    Ej: CICLE = [1,10,50,100,20]
    ENTRADA -> clices
    SALIDA -> none
    """
    def __init__(self,cicles):
        super().__init__()
        self.CICLE=cicles
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        self.pwm=[]
        """
        NOTAS: PINES 11,13,15,16,18 EN USO
        """
        self.PIN=[11,13,15,16,18]
        for i in range(5):
            GPIO.setup(self.PIN[i], GPIO.OUT, initial=GPIO.LOW)
            self.pwm.append(GPIO.PWM(self.PIN[i],100))
    """
    Secuencia con la que vibrarán los motores por cada
    corrida
    """
    def run(self):
        for j in range(5):
            for i in range(5):
                GPIO.output(self.PIN[i], True)
                self.pwm[i].start(self.CICLE[i])
            time.sleep(0.2)
            for i in range(5):
                self.pwm[i].stop()
                GPIO.output(self.PIN[i], False)
            time.sleep(0.05)
        GPIO.cleanup()

"""
#CODIGO EJEMPLO
PIN=[11,12,13,15,16]
CICLE = [100,10,50,100,100]
thread1 = PWM1(CICLE)
thread1.start()
thread1.join() #Espeara a que termine su ejecución
print ("Exiting Main Thread")

GPIO.cleanup()
"""
#Codigo para limpiar pines
#import RPi.GPIO as GPIO
#GPIO.cleanup()

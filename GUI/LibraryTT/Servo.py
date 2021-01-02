import RPi.GPIO as GPIO
from time import sleep

class Servo:
    """
    Clase para el control de servomotor
    """
    
    def __init__(self,Angle):
        """
        Este siempre se pondrá en 90° por default
        Parametros
        ---------------
        Angle => [0,180]
        """
        GPIO.setwarnings(False) #Quitar warnings
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(12, GPIO.OUT)
        self.setAngle(Angle)
        sleep(1)

        
    def setAngle(self,angle):
        """
        Función para cambiar la posición del servomotor
        solo acepta valores entre 0 y 180° por seguridad
        Parametros
        ----------------
        angle => [0,180]
        """
        if (angle<=180 and angle>=0):
            pwm=GPIO.PWM(12,50)
            pwm.start(0)
            duty = angle/ 18 + 2.2
            GPIO.output(12, True)
            pwm.ChangeDutyCycle(duty)
            sleep(0.3) #Si la diferencia entre angulos es muy grade, no llegará
            GPIO.output(12, False)
            pwm.ChangeDutyCycle(duty)
            pwm.stop()
            
        else:
            pass
    
    def stop(self):
        """
        Funcion para parar el servor
        """
        self.setAngle(90)
        GPIO.cleanup()
    
    def __del__(self):
        """
        Destrucción del Objeto
        """
        self.setAngle(90)
        GPIO.cleanup()

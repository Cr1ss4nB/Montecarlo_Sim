from statistics import mean
from math import sqrt
from scipy.stats import norm

class AverageTest:
    # Clase que implementa la Prueba de Promedio para una secuencia de números generados.
    def __init__(self, ri_nums):

        self.ri_nums = ri_nums
        self.average = 0
        self.alpha = 0.05
        self.acceptation = 0.95
        self.passed = False
        self.n = len(ri_nums)
        self.z = 0.0
        self.superior_limit = 0.0
        self.inferior_limit = 0.0

    def calcAverage(self):
       # Calcula el promedio de la secuencia de números generados.
        if self.n != 0:
            self.average = mean(self.ri_nums)

    def calculateZ(self):
        #Calcula el valor Z necesario para la prueba.

        self.z = norm.ppf(1 - (self.alpha / 2))

    def calculateSuperiorLimit(self):
        #Calcula el límite superior para la prueba.
        if self.n > 0:
            self.superior_limit = (1/2) + (self.z * (1 / sqrt(12 * self.n)))

    def calculateInferiorLimit(self):
        # Calcula el límite inferior para la prueba.
        if self.n > 0:
            self.inferior_limit = (1/2) - (self.z * (1 / sqrt(12 * self.n)))
    
    def checkTest(self):
        # Realiza la prueba de Promedio y establece si ha sido superada.
        self.calcAverage()
        self.calculateZ()
        self.calculateSuperiorLimit()
        self.calculateInferiorLimit()
        return self.inferior_limit <= self.average <= self.superior_limit

    def checkIfPassed(self):
        #Comprueba si la prueba ha sido superada.
        if self.inferior_limit <= self.average <= self.superior_limit:
            self.passed = True
        else:
            self.passed = False
        return self.passed
    
    def clear(self):
        # Restablece los valores de la prueba a sus valores iniciales.
        self.average = 0
        self.alpha = 0.05
        self.acceptation = 0.95
        self.passed = False
        self.z = 0.0
        self.superior_limit = 0.0
        self.inferior_limit = 0.0

    
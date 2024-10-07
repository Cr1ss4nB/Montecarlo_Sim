from numpy import mean, var
import scipy.stats as st

class VarianceTest:
    #Clase que implementa la Prueba de Varianza para una secuencia de números generados.
    def __init__(self, ri_numbers):
        #Inicializa una instancia de VarianceTest.
        self.ri_numbers = ri_numbers
        self.variance = 0.0
        self.alpha = 0.05
        self.average = 0.0
        self.acceptation = 0.95
        self.passed = False
        self.n = len(ri_numbers)
        self.superior_limit = 0.0
        self.inferior_limit = 0.0
        self.chi_square1 = 0.0
        self.chi_square2 = 0.0

    def calculateVariance(self):
       # Calcula la varianza de la secuencia de números generados.
        self.variance = var(self.ri_numbers)

    def calculateAverage(self):
        #Calcula el promedio de la secuencia de números generados.
        self.average = mean(self.ri_numbers)

    def calculateChiSquare1(self):
        #Calcula el valor crítico de chi-cuadrado para el límite inferior.
        self.chi_square1 = st.chi2.ppf(self.alpha / 2, self.n - 1)

    def calculateChiSquare2(self):
        #Calcula el valor crítico de chi-cuadrado para el límite superior.
        self.chi_square2 = st.chi2.ppf(1 - self.alpha / 2, self.n - 1)

    def calculateInferiorLimit(self):
        #Calcula el límite inferior para la varianza.
        self.inferior_limit = self.chi_square1 / (12 * (self.n - 1))

    def calculateSuperiorLimit(self):
        #Calcula el límite superior para la varianza.
        self.superior_limit = self.chi_square2 / (12 * (self.n - 1))

    def checkTest(self):
        #Realiza la Prueba de Varianza y establece si ha sido superada.
        self.calculateAverage()
        self.calculateVariance()
        self.calculateChiSquare1()
        self.calculateChiSquare2()
        self.calculateSuperiorLimit()
        self.calculateInferiorLimit()
        return self.inferior_limit <= self.variance <= self.superior_limit

    def clear(self):
        #Restablece los valores de la prueba.
        self.variance = 0.0
        self.alpha = 0.05
        self.average = 0.0
        self.acceptation = 0.95
        self.passed = False
        self.superior_limit = 0.0
        self.inferior_limit = 0.0
        self.chi_square1 = 0.0
        self.chi_square2 = 0.0

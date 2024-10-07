from typing import Any
from scipy.stats import chi2
import numpy as np

class ChiTest:
    # Clase que implementa la Prueba de Chi-Cuadrado para una secuencia de números generados.
    def __init__(self, ri_values=[], intervals_amount=8, a=8, b=10):
        self.ri_values = ri_values
        self.ni_values = []
        self.a = a
        self.b = b
        self.niMin = 0
        self.niMax = 0
        self.num_amount = len(ri_values)
        self.intervals_amount = intervals_amount
        self.intervals_values = []
        self.frequency_obtained = []
        self.expected_frequency = []
        self.chi_squared_values = []
        self.chiReverse = 0
        self.sumChi2 = 0
        self.passed = False

    def fillNiValues(self):
       # Calcula y llena la lista 'ni_values' con los valores 'ni'.
        for i in range(self.num_amount):
            value = self.a + (self.b - self.a) * self.ri_values[i]
            self.ni_values.append(value)

    def sortNiArray(self):
       # Ordena la lista 'ni_values'.
        self.ni_values.sort()

    def obtainMinNiValue(self):
       # Obtiene el valor mínimo de 'ni_values'.
        self.niMin = min(self.ni_values)
        return min(self.ni_values)

    def obtainMaxNiValue(self):
       # Obtiene el valor máximo de 'ni_values'.
        self.niMax = max(self.ni_values)
        return max(self.ni_values)

    def fillIntervalsValuesArray(self):
       # Llena la lista 'intervals_values' con los valores de los intervalos.
        min_value = self.obtainMinNiValue()
        max_value = self.obtainMaxNiValue()
        self.intervals_values.append(min_value)

        for i in range(self.intervals_amount):
            value = round(self.intervals_values[i] + (max_value - min_value) / self.intervals_amount, 5)
            self.intervals_values.append(value)

    def fillFrequenciesArrays(self):
        #Llena las listas 'frequency_obtained' y 'expected_frequency' con las frecuencias observadas y esperadas respectivamente.
        expected_freq = round(float(len(self.ni_values)) / self.intervals_amount, 2)
        counter = 0

        for i in range(len(self.intervals_values) - 1):
            for j in range(len(self.ni_values)):
                if (self.ni_values[j] >= self.intervals_values[i]) and (self.ni_values[j] < self.intervals_values[i + 1]):
                    counter += 1
            self.frequency_obtained.append(counter)
            self.expected_frequency.append(expected_freq)
            counter = 0

    def fillChiSquaredValuesArray(self):
        #Llena la lista 'chi_squared_values' con los valores calculados de Chi-Cuadrado.
        for i in range(len(self.frequency_obtained)):
            value = round(((self.frequency_obtained[i] - self.expected_frequency[i]) ** 2) / self.expected_frequency[i], 2)
            self.chi_squared_values.append(value)

    def cumulativeObtainedFrequency(self):
        #Calcula la frecuencia acumulada de los valores observados.
        result = sum(self.frequency_obtained)
        return result

    def cumulativeExpectedFrequency(self):
        #Calcula la frecuencia acumulada de los valores esperados.
        result = sum(self.expected_frequency)
        return result

    def cumulativeChiSquaredValues(self):
        #Calcula la sumatoria de los valores de Chi-Cuadrado.
        result = sum(self.chi_squared_values)
        return result

    def chi_squared_test_value(self):
        #Calcula el valor crítico de Chi-Cuadrado para la prueba.
        margin_of_error = 0.05
        degrees_of_freedom = self.intervals_amount - 1

        chiSquared = chi2(degrees_of_freedom)
        return chiSquared.ppf(1.0 - margin_of_error)

    def checkTest(self):
        #Realiza la prueba de Chi-Cuadrado y establece si ha sido superada.
        self.fillNiValues()
        self.sortNiArray()
        self.fillIntervalsValuesArray()
        self.fillFrequenciesArrays()
        self.fillChiSquaredValuesArray()
        self.chiReverse = self.chi_squared_test_value()
        self.sumChi2 = self.cumulativeChiSquaredValues()

        return self.cumulativeChiSquaredValues() <= self.chi_squared_test_value()
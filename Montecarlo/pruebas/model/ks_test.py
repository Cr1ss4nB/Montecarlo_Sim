from statistics import mean
from scipy import stats
from scipy.stats import norm
import numpy as np

class KsTest:
   # Clase que implementa la Prueba de Kolmogorov-Smirnov (KS) para una secuencia de números generados.

    def __init__(self, ri_nums=[], n_intervals=10):
      #  Inicializa una instancia de KsTest.
        self.ri = ri_nums
        self.n = len(ri_nums)
        self.average = 0
        self.d_max = 0
        self.d_max_p = 0
        self.min = 0
        self.max = 0
        self.oi = []
        self.oia = []
        self.prob_oi = []
        self.oia_a = []
        self.prob_esp = []
        self.diff = []
        self.passed = False
        self.alpha = 0.05
        self.intervals = []
        self.n_intervals = n_intervals

    def calculate_oia(self):
        #Calcula la sumatoria acumulada de las frecuencias observadas (oia).
        cum_freq = 0

        for freq in self.oi:
            cum_freq += freq
            self.oia.append(cum_freq)

    def calculate_min(self):
       # Calcula el valor mínimo en la secuencia de números generados.
        if self.n != 0:
            self.min = min(self.ri)

    def calculate_max(self):
        #Calcula el valor máximo en la secuencia de números generados.
        if self.n != 0:
            self.max = max(self.ri)

    def calculateAverage(self):
       # Calcula el promedio de la secuencia de números generados.
        if self.n != 0:
            self.average = mean(self.ri)

    def checkTest(self):
       # Realiza la prueba de Kolmogorov-Smirnov (KS) y establece si ha sido superada.
        self.calculate_min()
        self.calculate_max()
        self.calculateAverage()
        self.calculate_intervals()
        self.calculate_oi()
        self.calculate_oia()
        self.calculate_prob_oi()
        self.calculate_oia_a()
        self.calculate_prob_esp()
        self.calculate_diff()
        self.d_max = max(self.diff)
        self.calculate_KS()
        return self.d_max <= self.d_max_p

    def calculate_KS(self):
      #Calcula el valor crítico de Kolmogorov-Smirnov (KS) para la prueba.
        alpha = self.alpha
        n = self.n
        if self.n <= 50 and self.n > 0:
            # Calcular el valor crítico usando la función scipy.stats.ksone.ppf()
            critical_value = stats.ksone.ppf(1 - alpha / 2, n) 
            # OJO: Usamos 1 - alpha / 2 para una prueba bilateral
        if self.n > 50:
            # Calcular el valor crítico usando la función scipy.stats.kstwobign.isf()
            critical_value = stats.kstwobign.isf(alpha) / np.sqrt(n)
        self.d_max_p = critical_value

    def calculate_prob_esp(self):
       # Calcula las probabilidades esperadas para cada intervalo.
        for i in range(len(self.oia_a)):
            self.prob_esp.append(self.oia_a[i] / self.n)

    def calculate_diff(self):
        #Calcula las diferencias absolutas entre las probabilidades observadas y esperadas.
        for i in range(len(self.prob_esp)):
            self.diff.append(abs(self.prob_esp[i] - self.prob_oi[i]))

    def calculate_oia_a(self):
        #Calcula la sumatoria acumulada de las probabilidades esperadas (oia_a).
        n1 = self.n / self.n_intervals
        for i in range(self.n_intervals):
            self.oia_a.append(n1 * (i + 1))

    def calculate_prob_oi(self):
        #Calcula las probabilidades observadas para cada intervalo.
        for i in range(len(self.oia)):
            self.prob_oi.append(self.oia[i] / self.n)

    def calculate_oi(self):
        #Calcula las frecuencias observadas para cada intervalo.
        ri_temps = self.ri.copy()

        ri_temps.sort() #ordena una copia del set

        self.oi = [0] * self.n_intervals
        # Iterar a través de los valores de ri y contar en qué intervalo caen
        for valor in ri_temps:
            for i, intervalo in enumerate(self.intervals):
                if intervalo[0] <= valor < intervalo[1]:
                    self.oi[i] += 1
                    break  # No es necesario seguir buscando en otros intervalos

        return self.oi

    def calculate_intervals(self):
        #Calcula los intervalos utilizados para la prueba KS.
        if self.n != 0:
            n_intervals = self.n_intervals
            interval_size = (self.max - self.min) / n_intervals
            initial = self.min
            for _ in range(n_intervals):
                new_interval = (initial, initial + interval_size)
                self.intervals.append(new_interval)
                initial = new_interval[1]

    
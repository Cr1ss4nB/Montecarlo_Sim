import numeros.congruencias as GenCon 
import pruebas.test as test
import time
import math
import random # Permite generar números aleatorios
import csv # Permite leer y escribir datos en formato CSV.
from operator import attrgetter # Permite identificar campos por su nombre.
from scipy.stats import norm

ri_globales = []

def leerArchivo(file):
    with open(file, 'r') as f:
        lista = [float(line.strip()) for line in f]
    return lista

def obtenerSemilla():
    milliseconds = int(round(time.time() * 1000))
    return milliseconds

def generarPseudoAleatorios():

    global ri_globales  # Declara ri_globales como global

    m = 1000000
    ri_generados = []

    try:
        xi_generados = GenCon.contruirNumeroEspecificos(obtenerSemilla(),m,obtenerA(),obtenerC(m))
        ri_generados = GenCon.crearRiAvanzadoCon("",m, xi_generados)

    except:
        print("RI Aprobados - En Caso de Emergencia")
        ri_generados = leerArchivo('ri_aprobados.txt')

    test.do(ri_generados)

    ri_aprobados = test.getPassedData()

    ri_globales = ri_aprobados

def obtenerC(n):
    while True:
        r = random.randint(2, n)
        if math.gcd(n, r) == 1:   # Si el MCD de n y r es 1, son coprimos
            return r


def obtenerA():
    primos_pequeños = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
    return random.choice(primos_pequeños)



def obtenerRandom():
    while(len(ri_globales) == 0 ):
        generarPseudoAleatorios()
    tempNum = ri_globales[0]
    ri_globales.pop(0) #toma el primer dato de la lista y lo borra
    return tempNum  

# Se define como obtener los aleatorios y retorna una lista.
def ObtenerCantidadRi(cantidad):
    listadoRi = []

    for i in range(cantidad):
        listadoRi.append(obtenerRandom()) 

    return listadoRi

def obtenerRandom50():
    moneda = False
    if obtenerRandom() >= 0.5:
        moneda = True
    return moneda


def obtenerRandomNormal(cantidad):
    return crearNiNormales(35,10,ObtenerCantidadRi(cantidad))

def crearNiNormales(media, desv, ri):
    ni = []
    for r in ri:
        ni.append(norm.ppf(r, loc=media, scale=desv))
    return ni


#CLASE JUGADOR
class jugador:
    def __init__(self, id, resistencia, suerte, genero):
        self.id = id
        self.resistencia = resistencia
        self.genero = genero
        self.experiencia = 10
        self.suerte = suerte
        self.resistencia_ronda = resistencia
        self.resistencia_ronda_previa = resistencia
        self.puntos = 0
        self.extra = 0
        self.victorias = 0
        self.total_puntos_jugador = 0
        self.tiros = 0
        self.lanzamiento_especial = False

    # Cada lanzamiento a la diana de arqueria
    def lanzar(self):
        # Si un arquero suma 19 puntos, es decir 9 extra a sus 10 exp inicial obtiene dos rondas donde solo perdera 1 punto de resistencia
        if self.experiencia >= 19 and not self.lanzamiento_especial:
            self.resistencia_ronda -= 5
            self.tiros = 2
            self.lanzamiento_especial = True

        elif self.tiros > 0:
            self.resistencia_ronda -= 1 # Si esta en racha solo perdera 1 punto de resistencia
            self.tiros -= 1

        elif self.tiros == 0:
            self.resistencia_ronda -= 5 

    # Metodo para sumar los puntos al jugador.
    def sumar_puntos_victoria(self, punto_lanzamiento):
        self.puntos += punto_lanzamiento

    def fin_ronda(self):
        self.puntos = 0

    # Cuando un arquero gana una ronda suma 3 puntos de experiencia.
    def sumar_puntos_victoriaRonda(self):
        self.victorias += 1
        self.experiencia += 3

    # Metodo para cambiar la suerte del jugador, en cada lanzamiento este valor cambia en un rango de 1 a 3.
    def asignar_suerte(self, suerte):
        self.suerte = suerte

    # Metodo para modificar la resistencia de la ronda del jugador teniendo en cuenta el cansancio, puede ser 1 o 2.
    def cansancio(self, cansancio):
        self.resistencia_ronda = self.resistencia_ronda_previa - cansancio
        self.resistencia_ronda_previa = self.resistencia_ronda

    # Metodo para restaurar la resistencia del jugador, cada que termina un juego.
    def recuperar_resistencia(self):
        self.resistencia_ronda = self.resistencia
        self.resistencia_ronda_previa = self.resistencia

    # Se suma cuando un arquero obtuvo lanzamientos extra.
    def lanzar_extra(self):
        if self.extra > 0:
            self.extra += 1
        else:
            self.extra = 0

#CLASE EQUIPO
class equipo:
    # Contructor de la clase
    def __init__(self, nombre, jugadores):
        self.nombre = nombre
        self.jugadores = jugadores
        self.puntos = 0

    # Metodo para sumar puntos al equipo cuando gane una ronda.
    def sumar_puntos_victoriaRonda(self):
        self.puntos += 1

    # Se ordenan los jugadores del equipo de acuerdo a la suerte
    def ordenar_suerte(self):
        self.jugadores.sort(key=lambda jugador: jugador.suerte, reverse=True)

    # Se ordenan los jugadores del equipo de acuerdo a sus puntos
    def ordenar_puntos(self):
        self.jugadores.sort(key=lambda jugador: jugador.puntos, reverse=True)

    # Metodo para sumar al puntaje global del equipo
    def sumar_puntuacion_global_equipo(self, individual):
        self.puntos += individual

    # Se identifica al jugador con mayor suerte del equipo.
    def jugador_mayor_suerte(self):
        return max(self.jugadores, key=attrgetter('suerte'))
    
    # Se identifica al jugador con mas lanzamientos adicionales.
    def jugador_mayor_suerte_ronda(self):
        return max(self.jugadores, key=attrgetter('extra'))
    
    # Configura los valores por defecto cuando finaliza un juego.
    def fin_juego(self):
        self.puntos = 0
        for jugador in self.jugadores:
            jugador.recuperar_resistencia()
            jugador.tiros = 0
            jugador.puntos = 0
            jugador.victorias = 0
            jugador.lanzamiento_especial = False

    def jugador_ganador_ronda(self):
        ganador = max(self.jugadores, key=attrgetter('puntos'))
        ganador.sumar_puntos_victoriaRonda()
        return ganador

    # Se obtiene al jugador individual con mayor cantidad de puntos, y lo retorna.
    def jugador_ganador(self):
        return max(self.jugadores, key=attrgetter('puntos'))
    
    # Se restablecen los puntos de cada ronda a todos los jugadores del equipo.
    def nueva_ronda(self):
        for jugador in self.jugadores:
            jugador.fin_ronda()

    # Se identifica al jugador que ha ganado más rondas de cada equipo, y lo retorna.
    def Obtener_victoria_jugador(self):
        return max(self.jugadores, key=attrgetter('victorias'))

# CLASE JUEGO
class Juego:
    historial_equipo_uno = []
    historial_equipo_dos = []
    cantidad_Total_hombres = 0
    cantidad_Total_mujeres = 0
    genero_ganador_Total = ""

    # Metodo para inicializar el juego, con dos equipos.
    def Iniciar_juego(self, equipo_uno, equipo_dos):

        # Se configura por defecto los atributos.
        ganador = {"jugador": self.Crear_jugador(0, 0, 0, 0), "equipo": ""}
        hombres = 0
        mujeres = 0

        # El equipo que obtenga más puntos al cabo de diez rondas gana el juego
        mujeres,hombres = self.jugar10rondas(equipo_uno, equipo_dos, hombres, mujeres)

        # En el caso de que ocurra un empate por rondas ganas, se resuelve el empate.
        if equipo_uno.Obtener_victoria_jugador().victorias == equipo_dos.Obtener_victoria_jugador().victorias:
            self.Resolver_empate_final(equipo_uno, equipo_dos)

        # Se determina el jugador que ganó más rondas entre los dos equipos, será el ganador individual.
        if equipo_uno.Obtener_victoria_jugador().victorias > equipo_dos.Obtener_victoria_jugador().victorias:
            ganador = {"jugador": equipo_uno.Obtener_victoria_jugador(), "equipo": equipo_uno.nombre}
        if equipo_uno.Obtener_victoria_jugador().victorias < equipo_dos.Obtener_victoria_jugador().victorias:
            ganador = {"jugador": equipo_dos.Obtener_victoria_jugador(), "equipo": equipo_dos.nombre}

        # Se agrega el historial de ambos equipos.
        self.historial_equipo_uno.append(equipo_uno)
        self.historial_equipo_dos.append(equipo_dos)

        # Se determina el jugador con más suerte en cada uno de los juegos.
        suerte = {"jugador": self.Crear_jugador(0, 0, 0, 0), "equipo": ""}
        if equipo_uno.jugador_mayor_suerte_ronda().extra > equipo_dos.jugador_mayor_suerte_ronda().extra:
            suerte = {"jugador": equipo_uno.jugador_mayor_suerte_ronda(), "equipo": equipo_uno.nombre}
        if equipo_uno.jugador_mayor_suerte_ronda().extra < equipo_dos.jugador_mayor_suerte_ronda().extra:
            suerte = {"jugador": equipo_dos.jugador_mayor_suerte_ronda(), "equipo": equipo_dos.nombre}


        # Se determina el genero con más victorias en cada juego y se suma al total.
        genero_ganador_ronda =""
        if(mujeres > hombres):
            genero_ganador_ronda = "mujer"
            self.cantidad_Total_mujeres = self.cantidad_Total_mujeres+1
        else:
            genero_ganador_ronda = "hombre"
            self.cantidad_Total_hombres = self.cantidad_Total_hombres+1

        if(self.cantidad_Total_mujeres>self.cantidad_Total_hombres):
            self.genero_ganador_Total= "mujer"
        else:
            self.genero_ganador_Total="hombre"

        return {"equipo_uno": equipo_uno,
                "equipo_dos": equipo_dos,
                "victorias_de_equipo": equipo_uno if equipo_uno.puntos > equipo_dos.puntos else equipo_dos,
                "ganador": ganador,
                "suerte": suerte,
                "hombres": self.cantidad_Total_hombres,
                "mujeres": self.cantidad_Total_mujeres,
                "genero_ganador": genero_ganador_ronda,
                "genero_ganador_Total":self.genero_ganador_Total
                }
    
    # Se simulan las rondas determinadas de un juego entre dos equipos, verificando el genero de sus integrantes. 
    def jugar10rondas(self, equipo_uno, equipo_dos, hombres, mujeres):
        for round in range(0, 10):
            equipo_uno.nueva_ronda()
            equipo_dos.nueva_ronda()

            # Se calculan los lanzamientos de cada equipo, teniendo en cuenta la resistencia por ronda
            lanzar_uno, lanzar_dos = self.obtenerCantidadDisparos(equipo_uno, equipo_dos)

            grupo_r_uno = ObtenerCantidadRi(lanzar_uno)
            grupo_r_dos = ObtenerCantidadRi(lanzar_dos)

            # Se simulan las rondas de los dos equipos.
            self.Ronda_de_juego(equipo_uno, grupo_r_uno)
            self.Ronda_de_juego(equipo_dos, grupo_r_dos)

            self.asignar_suerte(equipo_uno)
            self.asignar_suerte(equipo_dos)

            # El arquero de los dos equipos que sume más puntos en sus lanzamientos gana una ronda individual.
            ganador_uno = equipo_uno.jugador_ganador()
            ganador_dos = equipo_dos.jugador_ganador()

            # En el caso de que ocurra un empate de puntos, se resuelve el empate.
            if ganador_uno.puntos == ganador_dos.puntos:
                self.Resolver_empate(equipo_uno, equipo_dos)

            # Se determina el ganador de la ronda.
            if ganador_uno.puntos != ganador_dos.puntos:
                if ganador_uno.puntos > ganador_dos.puntos:
                    ganador_round = equipo_uno.jugador_ganador_ronda()
                if ganador_uno.puntos < ganador_dos.puntos:
                    ganador_round = equipo_dos.jugador_ganador_ronda()

            # Se determina el genero que gano la ronda
            if ganador_round.genero == "hombre":
                hombres += 1
            if ganador_round.genero == "mujer":
                mujeres += 1

            self.Lanzar_por_suerte(equipo_uno)
            self.Lanzar_por_suerte(equipo_dos)
        return mujeres,hombres

    # Se calcula y retorna la cantidad de lanzamientos de cada equipo.
    def obtenerCantidadDisparos(self, equipo_uno, equipo_dos):
        lanzar_uno = int(sum(jugador.resistencia_ronda for jugador in equipo_uno.jugadores) / 5)
        lanzar_dos = int(sum(jugador.resistencia_ronda for jugador in equipo_dos.jugadores) / 5)
        return lanzar_uno,lanzar_dos

    # Metodo para configurar por defecto los atributos.
    def Reiniciar_historial(self):
        self.historial_equipo_uno = []
        self.historial_equipo_dos = []
        self.cantidad_Total_hombres = 0
        self.cantidad_Total_mujeres = 0

    # Se obtienen la cantidad de puntos totales de cada equipo.
    def Obtener_puntos_Totales(self):
        return {"hombres": self.cantidad_Total_hombres, 
                "mujeres": self.cantidad_Total_mujeres, 
                "equipo_uno": self.historial_equipo_uno[0].nombre,
                "puntos_Totales_uno": sum(equipo.puntos for equipo in self.historial_equipo_uno),
                "equipo_dos": self.historial_equipo_dos[0].nombre,
                "puntos_Totales_dos": sum(equipo.puntos for equipo in self.historial_equipo_dos)}

    # Genera rondas adicionales para que no hayan equipos con la misma cantidad de puntos.
    def Resolver_empate_final(self, equipo_uno, equipo_dos):
        while equipo_uno.jugador_ganador().victorias == equipo_dos.jugador_ganador().victorias:

            lanzar = obtenerRandom()
            lanzar_dos = obtenerRandom()

            punto_uno = self.Obtener_punto(lanzar, equipo_uno.jugador_ganador())
            punto_dos = self.Obtener_punto(lanzar_dos, equipo_dos.jugador_ganador())
            if punto_uno > punto_dos:
                equipo_uno.jugador_ganador().victorias += 1
            elif punto_uno < punto_dos:
                equipo_dos.jugador_ganador().victorias += 1

    # Genera lanzamientos adicionales para el empate de jugadores
    def Resolver_empate(self, equipo_uno, equipo_dos):
        while equipo_uno.jugador_ganador().puntos == equipo_dos.jugador_ganador().puntos:
            lanzar = obtenerRandom()
            lanzar_dos = obtenerRandom()
            punto_uno = self.Obtener_punto(lanzar, equipo_uno.jugador_ganador())
            punto_dos = self.Obtener_punto(lanzar_dos, equipo_dos.jugador_ganador())
            equipo_uno.jugador_ganador().sumar_puntos_victoria(punto_uno)
            equipo_dos.jugador_ganador().sumar_puntos_victoria(punto_dos)

    # Metodo para crear un jugador
    def Crear_jugador(self, id, resistencia, suerte, bool_genero):
        genero = "hombre"
        if (bool_genero):
          genero = "mujer"
        return jugador(id, resistencia, float(1 + (3 - 1) * suerte), genero)
    
    # Metodo para crear un equipo.
    def Crear_equipo(self, nombre):
        jugadores = []
        ri_suerte = ObtenerCantidadRi(5)
        ni_normales_resistencia = obtenerRandomNormal(5)

        for i in range(len(ri_suerte)):
            jugadores.append(self.Crear_jugador((i + 1),ni_normales_resistencia[i],ri_suerte[i],obtenerRandom50()))
        return equipo(jugadores=jugadores, nombre=nombre)


    # Se obtiene la puntuación de un jugador tras realizar su lanzamiento.
    def Obtener_punto(self, tiro_aleatorio, jugador):
        # Se tienen en cuenta los parametros del ejercicio:
        tiro_realizado = int(100 * tiro_aleatorio)

        if jugador.genero == "hombre":
            if tiro_realizado <= 20:
                return 10
            elif 20 < tiro_realizado <= 53:
                return 9
            elif 53 < tiro_realizado <= 93:
                return 8
            elif 93 < tiro_realizado <= 100:
                return 0
        if jugador.genero == "mujer":
            if tiro_realizado <= 30:
                return 10
            elif 30 < tiro_realizado <= 68:
                return 9
            elif 68 < tiro_realizado <= 95:
                return 8
            elif 95 < tiro_realizado <= 100:
                return 0
            
    # Metodo que realiza el lanzamiento de cada jugador. (Resta 5 puntos de resistencia).
    def Lanzamiento_para_jugador(self, tiro_aleatorio, jugador):
        jugador.lanzar() # quita resistencia y ajusta experiencia
        jugador.sumar_puntos_victoria(self.Obtener_punto(tiro_aleatorio, jugador))

    # Cada ronda de juego se calcula aqui, para cada equipo y cada jugador dependiendo la resistencia
    def Ronda_de_juego(self, equipo, lista_Ri): 
        posicion_Ri_inicial = 0
        for jugador in equipo.jugadores:
            limite_Ri_tomados = posicion_Ri_inicial + int(jugador.resistencia_ronda / 5) #calcula cuantos tiros tuvo el jugador
            for tiro_aleatorio in lista_Ri[posicion_Ri_inicial:limite_Ri_tomados]:
                self.Lanzamiento_para_jugador(tiro_aleatorio, jugador)
            equipo.sumar_puntuacion_global_equipo(jugador.puntos)
            posicion_Ri_inicial = limite_Ri_tomados
        self.Lanzar_por_suerte(equipo)
        equipo = self.Asignar_cansancio(equipo)
        return equipo

    # Se establece el cansancio de los jugadores de forma aleatoria
    def Asignar_cansancio(self, equipo):
        for i in range(0, 5):
            if obtenerRandom50():
                equipo.jugadores[i].cansancio(1)
            else:
                equipo.jugadores[i].cansancio(2)
        return equipo

    # Se obtienen numeros aleatorios en determinado rango para usarlos como Ni,
    # para multiplicar tomaremos un dato aleatorio de la lista de self.Ri con su respectivo valor.
    def Obtener_aleatorio_entre(self,min,max):
        return float(min + (max - min) * obtenerRandom())

    def asignar_suerte(self, equipo):
        for i, jugador in enumerate(equipo.jugadores):
            suerte = self.Obtener_aleatorio_entre(1,3)
            jugador.asignar_suerte(suerte)

    """
    lanzamiento extra: En cada ronda se sortea un lanzamiento por equipo, el cual será otorgado al 
    jugador con más suerte en cada uno de ellos. Este lanzamiento se tendrá en 
    cuenta para el marcador global del grupo, pero no para determinar el ganador 
    de ronda individual.

    Si un jugador gana tres lanzamientos extra de forma consecutiva tiene 
    derecho a un lanzamiento extra, sin importar el valor de su resistencia. Este 
    lanzamiento se tendrá en cuenta para el marcador global del grupo, pero no 
    para determinar el ganador de ronda individual.
    """
    def Lanzar_por_suerte(self, equipo):
        porcentaje_diana = obtenerRandom()
        equipo.sumar_puntuacion_global_equipo(self.Obtener_punto(porcentaje_diana, equipo.jugador_mayor_suerte()))
        if equipo.jugador_mayor_suerte().extra == 0:
            equipo.jugador_mayor_suerte().extra = 1
        else:
            equipo.jugador_mayor_suerte().lanzar_extra()
        if equipo.jugador_mayor_suerte().extra >= 3:
            porcentaje_diana = obtenerRandom()
            equipo.sumar_puntuacion_global_equipo(self.Obtener_punto(porcentaje_diana, equipo.jugador_mayor_suerte()))

# RESULTADOS
# Instancia de la clase juego y configuracion por defecto del historial de los equipos y el contador de generos.
juego = Juego()
historial_equipo_uno = []
historial_equipo_dos = []
cantidad_Total_hombres = 0
cantidad_Total_mujeres = 0

def Mostrar_detalle_equipo(equipo):
    jugadores = []
    for jugador in equipo.jugadores:
        jugadores.append({
                            'id ': jugador.id,
                            'suerte ': jugador.suerte,
                            'genero ': jugador.genero,
                            'puntos jugador ': jugador.total_puntos_jugador,
                            'experiencia ': jugador.experiencia
                        })
    return {'nombre : ': equipo.nombre, 'jugadores ': jugadores, 'puntos equipo ': equipo.puntos}

# Metodo que proporciona los datos necesarios para iniciar las rondas.
def play(equipo_uno, equipo_dos, iteraciones):
    resultados = simular_juegos(equipo_uno, equipo_dos, iteraciones)
    mostrar_resumen_final = resumen(resultados)
    return mostrar_resumen_final

# Se realizan la cantidad de iteraciones asignadas y se reducen de forma descendente hasta llegar a 0.
def simular_juegos(equipo_uno, equipo_dos, iteraciones):
    while(iteraciones > 0):
        resultados = juego.Iniciar_juego(equipo_uno, equipo_dos)
        iteraciones = iteraciones-1
        mostrar_iteracion =  {
                        "jugador con más suerte en iteración ": 
                            {
                                'Iteracion':iteraciones,'id': resultados["suerte"]["jugador"].id,
                                'suerte': resultados["suerte"]["jugador"].suerte,
                                'genero': resultados["suerte"]["jugador"].genero,
                                'puntos': resultados["suerte"]["jugador"].puntos,
                                'tiros_extra': resultados["suerte"]["jugador"].extra,
                                "equipo": resultados["suerte"]["equipo"]
                            },
                        "Genero ganador": resultados["genero_ganador"]
                    }
        print(mostrar_iteracion)
    print("********************************************************************************************************************")
    return resultados

# Metodo para mostrar la cantidad total de puntos.
def total_puntos():
    pantalla = juego.Obtener_puntos_Totales()
    return pantalla

# Se organiza la informacion en diccionarios y se muestra via consola.
def resumen(resultados):
    mostrar_resumen_final =  {
                    "Equipo 1: ": Mostrar_detalle_equipo(resultados["equipo_uno"]),
                    "Equipo 2: ": Mostrar_detalle_equipo(resultados["equipo_dos"]),
                    "Equipo ¡Ganador!: ": Mostrar_detalle_equipo(resultados["victorias_de_equipo"]),
                    "Ganador individual: ": {
                                                'id': resultados["ganador"]["jugador"].id,
                                                'Suerte: ': resultados["ganador"]["jugador"].suerte,
                                                'Género: ': resultados["ganador"]["jugador"].genero,
                                                'Puntos: ': resultados["ganador"]["jugador"].puntos,
                                                "equipo: ": resultados["ganador"]["equipo"]
                                            },
                    "Victorias Mujeres: ": resultados["mujeres"],
                    "Victorias Hombres: ": resultados["hombres"],
                    "Genero con mas victorias totales: ": resultados["genero_ganador_Total"]
                }
    
    for clave, valor in mostrar_resumen_final.items():
        print(f"{clave}{valor}")

    print("********************************************************************************************************************")

    print(total_puntos())
    juego.Reiniciar_historial()

    return mostrar_resumen_final

# Metodo para iniciar la simulacion.
def Simular():
    print("Iniciando simulación...")
    equipo_uno = juego.Crear_equipo("Team Arduino")
    equipo_dos = juego.Crear_equipo("Team Raspberry")
    iteraciones = int(input("Ingrese el número de juegos: "))
    play(equipo_uno, equipo_dos, iteraciones)
# Se ejecuta la simulacion.
if __name__ == "__main__":
    Simular()
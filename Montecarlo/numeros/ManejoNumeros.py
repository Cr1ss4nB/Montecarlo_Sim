import numpy as np


def descargar(file,numeros):
    # Escribe los datos de la lista ri en un archivo de texto
    
    with open(file, 'w') as f:
        for r in numeros:
            f.write(str(r) + '\n')

def obtener_largo_numero(numero):
    # Convertir el número a cadena
    numero_str = str(numero)
    
    # Obtener la longitud de la cadena
    longitud = len(numero_str)
    
    return longitud

def extraer_numero(entero,inicio,fin):
    extraccion = str(entero)[inicio:fin]
    return int(extraccion)

def truncar(numero: float, max_decimales: int) -> float:
    int_part, dec_part = str(numero).split(".")
    return float(f"{int_part}.{dec_part[:max_decimales]}")


def calcularMedia(lista):
    return sum(lista) / len(lista)
    
def calcularDesviacion(lista):
    return np.std(lista, ddof=1)


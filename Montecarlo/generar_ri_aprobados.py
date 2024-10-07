import random

def generar_numeros_aleatorios(cantidad, archivo_salida):
    with open(archivo_salida, 'w') as f:
        for _ in range(cantidad):
            numero = random.uniform(0, 1)
            f.write(f"{numero}\n")

if __name__ == "__main__":
    cantidad_numeros = 1000000  # 1,000,000 de números
    archivo_salida = 'ri_aprobados.txt'
    print(f"Generando {cantidad_numeros} números aleatorios y guardándolos en {archivo_salida}...")
    generar_numeros_aleatorios(cantidad_numeros, archivo_salida)
    print("Generación completada.")

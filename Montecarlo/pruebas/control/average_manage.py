from pruebas.model.average_test import AverageTest

passed_data = []


def fastTest(ri_numbers):

    global passed_data

    passed_data.clear()
    
    all_data = ri_numbers.copy()
    num_passedTwo = 0  # Inicializar contador de datos pasados

    num_iterations = len(ri_numbers) // 1000
    for i in range(num_iterations):
        start_index = i * 1000
        end_index = (i + 1) * 1000

        subset_data = all_data[start_index:end_index]

        test = AverageTest(subset_data)
        
        if test.checkTest():
            for value in subset_data:
                passed_data.append(value)
        # Actualizar contador de datos pasados
        num_passedTwo += len(subset_data)
    if len(passed_data) > 0:
        num_passedOne = len(passed_data)
        print(f"Estado de la prueba (PROMEDIO): Pasaron {num_passedOne} de {num_passedTwo} Datos")
    else:
        print(f"Estado de la prueba (PROMEDIO): El set de datos no pasó la prueba Average")


def getPassedData():
    return passed_data
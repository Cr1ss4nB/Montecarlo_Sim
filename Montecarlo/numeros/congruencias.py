import numeros.ManejoNumeros as ManejoNumeros

xi = []
ri = []

def getXi(semilla, paridad, avanzado,k,c,g,m,a):  

    xi.clear()
    ri.clear()

    if not avanzado:
        contruirNumeros(semilla, paridad,k,c,g)
    else:
        contruirNumeroEspecificos(semilla,m,a,c)

    return xi


def contruirNumeroEspecificos(semilla,m,a,c):

    xi.clear()
    
    if m >= 0 and a >= 0 and c >= 0:

        crearPrimerfilaXi(semilla, c, a, m)

        crearXi(c,a,m)
    else:
        print("ERROR VALORES!")
    return xi

def contruirNumeros(semilla, paridad,k,c,g):


    if (k > -1 and c > -1 and g > -1):

        a, m = inicializar(semilla, k, c, g)

        if a == 1:
            print("Aditiva")

        
        crearXi(c, a, m)

        crearRi(paridad, m)
    else:
        print("ERROR VALORES!")


def crearXi(c, a, m):
    for i in range(m - 1):
        numero = (a * xi[i] + c) % m
        xi.append(numero)

def crearRi(paridad, m):
    if paridad == "par":
        for i in range(len(xi)):
            ri.append(xi[i]/ m)
    else:
        for i in range(len(xi)):
            ri.append(xi[i]/ (m - 1))

def crearRiAvanzadoCon(paridad, m, xi):
    ri = []
    if paridad == "par":
        for i in range(len(xi)):
            numero_ri = ManejoNumeros.truncar(xi[i]/ m, 5)
            if numero_ri < 1:
                ri.append(numero_ri)
    else:
        for i in range(len(xi)):
            float_number = float(xi[i]/ (m - 1))
            numero_ri = ManejoNumeros.truncar(float_number, 5)
            if numero_ri < 1:
                ri.append(numero_ri)
    return ri

def inicializar(semilla, k, c, g):

    if c == 0:
        a = 8 * k + 3
    else:
        a = 1 + 2 * k

    m = pow(2,g)

    crearPrimerfilaXi(semilla, c, a, m)

    return a,m

def crearPrimerfilaXi(semilla, c, a, m):
    xi.append( (a * semilla + c) % m)

    


def getRi():
    ri_trunc = []
    for r in ri:
        ri_trunc.append(ManejoNumeros.truncar(r,5))
    return ri_trunc


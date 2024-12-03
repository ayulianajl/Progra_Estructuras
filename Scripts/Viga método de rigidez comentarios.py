import numpy as np 

# Código de Python para resolver una viga por el método de rigidez utilizando la librería Numpy 

L = np.array([1, 0.8 , 2, 2, 3])  #Lista donde se guarda la longitud en metros de cada uno de los tramos
EI = 1000*np.array([6, 6 , 9, 9, 4]) # Lista donde se guarda la rigidez de cada tramo de la viga

P = np.array([[1, -20] , [3, -40]]) #Matriz de cargas puntuales aplicadas en los grados de libertad correspondientes

q = np.array([[3 , 0 , -30] , [4, -30 , -30] , [5, -30, 0]]) #Matriz que relaciona la aplicación de cargas distribuidas con los grados de libertad

gdlr = np.array([5, 9 , 11, 12]) #Grados de libertad restringidos

ntramos = len(L)
numgdl = (ntramos + 1)*2 #Número de grados de libertad. Siempre sigue el patrón del número de tramos +1 multiplicado por 2 en el caso de vigas. En el caso de marcos se debe considerar un grado de libertad adicional en la dirección horizontal
kglobal = np.zeros([numgdl, numgdl])  #Se calcula el número de grados de libertad y se crea una matriz de ceros que representa la matriz global del elemento

m_gdl = np.zeros([ntramos,4]) #Matriz con los grados de libertad Barras

for i in range(ntramos): #Bucle for que se repite 5 veces y que empieza en 1 para poder asignar el número de cada grado de libertad en la matriz mgdl.
    num_elem = i+1
    m_gdl[i][0] = num_elem*2-1
    m_gdl[i][1] = num_elem*2
    m_gdl[i][2] = num_elem*2+1
    m_gdl[i][3] = num_elem*2+2
print(m_gdl)
    

for i in range(ntramos) : #Bucle for que itera sobre los tramos de la viga para ir creando la matriz k de cada tramo de la viga. Este bucle debe ir llenando la matriz de rigidez global 

    a = 12*EI[i]/L[i]**3
    b = 6*EI[i]/L[i]**2
    c = 4*EI[i]/L[i]
    d = 2*EI[i]/L[i]
    kelem = np.array([[a,b,-a,b] , [b,c,-b,d] , [-a,-b,a,-b] , [b,d,-b,c]])
    print("\n")
    print("Matriz de rigidez : " , i+1)
    print(kelem)

    gdlElem = m_gdl[i] 
    for j in range(0,4) : #Este bucle se repite de cero a tres, es decir 4 veces.
        for k in range(0,4) :
            kglobal[int(gdlElem[j]-1)][int(gdlElem[k]-1)] = kelem[j][k] + kglobal[int(gdlElem[j]-1)][int(gdlElem[k]-1)] #Ensamblaje de la matriz de rigidez global de la estructura a partir de las matrices de cada elemento. 

print("\n Matriz de rigidez global de toda la estructura :")

for i in range(12):
    cadena = ''
    for j in range(12):
        cadena = cadena + str('{:10.2f}'.format(kglobal[i][j])) #Formato para impresión. 10.2 significa 10 espacios con 2 decimales, la f es punto flotante. 
    print(cadena)

Ptotal = np.zeros([numgdl])
print(Ptotal)

numpuntuales = len(P)

for i in range(numpuntuales):
        gdlcargado = P[i][0]
        valorcarga = P[i][1]
        Ptotal[gdlcargado-1] = valorcarga + Ptotal[gdlcargado-1]

print("\n Vector de fuerzas puntuales ")

print(Ptotal)

F = np.zeros(numgdl) # Vector de cargas distribuidas

num_Fdistri = len(q) 

print(num_Fdistri)

for i in range(num_Fdistri): # Bucle for que itera sobre la longitud del vector de fuerzas distribuidas y va tomando cada valor q1 y q2 de los tramos de la viga.
     num_elem = q[i][0] - 1
     q1 = q[i][1]
     q2 = q[i][2]

     if (abs(q1)<abs(q2)) :
          qRect = q1
          qTri = q2-q1
          fIzq = qRect*L[num_elem]/2 + 3/20*qTri*L[num_elem]
          Mizq = qRect*L(num_elem)**2/12 + qTri*L[num_elem]**2/30
          fder = qRect*L[num_elem]/2 + 7/20*qTri*L[num_elem]
          Mder = -qRect*L(num_elem)**2/12 - qTri*L[num_elem]**2/20

     elif (abs(q1)>abs(q2)) :
          qRect = q2
          qTri = q1-q2
          fIzq = qRect*L[num_elem]/2 + 7/20*qTri*L[num_elem]
          Mizq = qRect*L(num_elem)**2/12 + qTri*L[num_elem]**2/20
          fder = qRect*L[num_elem]/2 + 3/20*qTri*L[num_elem]
          Mder = -qRect*L(num_elem)**2/12 - qTri*L[num_elem]**2/30

     elif (abs(q1)==abs(q2)) :
          qRect = q1
          fIzq = qRect*L[num_elem]/2 
          Mizq = qRect*L(num_elem)**2/12 
          fder = qRect*L[num_elem]/2 
          Mder = -qRect*L(num_elem)**2/12 

     print("Fuerzas y Momentos equivalentes :")

     print("\n" , fIzq)
     print("\n" , Mizq)
     print("\n" , fder)
     print("\n" , Mder)

     

          






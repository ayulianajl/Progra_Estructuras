import openseespy.opensees as ops
import pandas as pd
import opsvis as opv
import matplotlib.pyplot as plt  #Importación de librerías que se utilizan en el código

ops.model('basic', '-ndm' , 3 , '-ndf' , 6) # Modelo básico de 3 dimensiones y 6 grados de libertad por nodo
ops.wipe()
#Importar desde pandas para leer archivo csv 

df = pd.read_csv('d:/Documentos/Angie/Otros/Angie Yuliana Jiménez L/Especialización Estructuras INESA TECH/Python/nodos.csv')


for index, nodo in df.iterrows(): #se itera sobre las filas del archivo 
    tag, x,y,z = nodo # Se asignan los puntos x,y,z al nodo correspondiente
    ops.node(int(tag), x,y,z)

ops.fixZ(0, 1, 1, 1, 1, 1, 1) #Restricciones del modelo

df2 = pd.read_csv('d:/Documentos/Angie/Otros/Angie Yuliana Jiménez L/Especialización Estructuras INESA TECH/Python/elementos.csv')


secTag_HEB300 = 1
col_tag = 1

ops.section('Elastic', secTag_HEB300, 2.1e7, 149.1, 25166, 8563, 810000, 186) #Se definen las secciones. Valores en cm


secTag_IPE270 = 2
vig_tag = 2

ops.section('Elastic', secTag_IPE270, 2.1e7, 45.90, 5790, 420, 810000, 11.59)

ops.geomTransf('Linear', col_tag , 1 , 0 , 0 ) #Transformación de coordenadas. Es similar a los ejes locales de los elementos en ETABS y SAP. Acá debe darse un vector paralelo al vector x (inico y fin de elemento), es decir un vector en el plano. De esta forma con este vector el sistema determina el tercer vector perpendicular al plano que se genera por los vectores dados.
ops.geomTransf('Linear', vig_tag , 1, -1 , 0 )

for index, element in df2.iterrows(): #Se itera el archivo elementos
    tag, nodo1,nodo2 = element
    if tag < 13: 
        ops.element('elasticBeamColumn', int(tag), int(nodo1), int(nodo2) , secTag_HEB300, col_tag) #las celdas del 1 al 12 son columnas
    else:
        ops.element('elasticBeamColumn', int(tag), int(nodo1), int(nodo2) , secTag_IPE270, vig_tag) #las celdas del 13 al 20 son vigas

ops.timeSeries('Constant', 1) #Método que se utiliza para representar cargas que varían en función del tiempo.

ops.pattern('Plain', 1, 1, '-fact', 1) #Método que se utiliza para añadir patrones los factores de carga. 

ops.load(7, 0,25000,0, 0, 0, 0) #Se añaden las cargas

ops.load(15, 0,25000,0, 0, 0, 0)

ops.eleLoad('-ele', 15,'-type', 'beamUniform',0,-200)

ops.wipeAnalysis() #Se elimina cualquier análisis realizado previamente
ops.constraints('Plain') 
ops.numberer('Plain')
ops.system('FullGeneral') #Se construye un sistema de ecuaciones lineales
ops.algorithm('Linear')
ops.integrator('LoadControl',1)  #Se usa para análisis dinámico. Se puede ir incrementando la carga de acuerdo al time series.
ops.analysis('Static')
ops.analyze(1)  # 1 significa que solo corre una vez.

desplazamientos = [] #Se genera una lista vacía donde se van a guardar los desplazamientos

max_desplazamiento_abs = None #Se define la variable como none

for node in range(1,21): #Se itera sobre cada nodo y se solicitan los desplazamientos por cada uno de ellos. Estos desplazamientos se guardan en la lista previamente definida y se solicita el máximo valor absoluto
    contador = 0
    d = ops.nodeDisp(node)
    des_abs = [abs(valor) for valor in d]
    contador += node
    print(contador,d)
    desplazamientos.extend(des_abs)
    max_d_abs = max(des_abs)
    max_index = node

max_desplazamiento_abs = max(desplazamientos)


opv.plot_model() #Se genera el modelo

plt.show()

ops.printModel('-file', 'ModeloPrueba.txt') 

print('El máximo desplazamiento absoluto es:' , max_desplazamiento_abs) #Se muestra el máximo desplazamiento. 






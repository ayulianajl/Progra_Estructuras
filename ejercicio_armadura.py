import openseespy.opensees as ops
import math
import matplotlib.pyplot as plt
import opsvis as opsv

#Modelado y análisis estático de una armadura

#unidades → SI
m = 1
kg = 1
s = 1
g = 9.81*m/s**2
N = kg*m/s**2
kgf = N*g # 1 kgf = kg * 9.81 m/s**2
kN = 1000*N

ops.wipe()

ops.model('basic','-ndm',2,'-ndf',2)

ops.node(1,*[0,0])
ops.node(2,*[0,3*m])
ops.node(3,*[4*m,0])
ops.node(4,*[4*m,3*m])
ops.node(5,*[8*m,0])
ops.node(6,*[8*m,3*m])
ops.node(7,*[12*m,0])

ops.fix(1,1,1,0) #Restricciones en x y y dependiendo del tipo de apoyo y su correspondiente nodo. 
ops.fix(3,1,1,0)
ops.fix(5,0,1,0)


#Se define el material y los elementos de la armadura

ops.tag = 1
E = 200e9*N/m**2
A_1 = 0.001*m**2
A_2 = 0.0005*m**2

material = ops.uniaxialMaterial('Elastic',1,E)

#Definición de elementos
ops.element('Truss',1,1,3,A_1,1)
ops.element('Truss',2,3,5,A_1,1)
ops.element('Truss',3,5,7,A_1,1)

ops.element('Truss',4,1,2,A_2,1)
ops.element('Truss',5,3,4,A_2,1)
ops.element('Truss',6,5,6,A_2,1)
ops.element('Truss',7,7,6,A_2,1)
ops.element('Truss',8,2,4,A_2,1)
ops.element('Truss',9,4,6,A_2,1)
ops.element('Truss',10,1,4,A_2,1)
ops.element('Truss',11,3,6,A_2,1)

#Definición de cargas actuantes en la armadura
ops.timeSeries('Constant',1)
ops.pattern('Plain',1,1) # El primer 1 es el tag y el segundo se refiere al timeseries
ops.load(7,*[10000*N,-20000*N])

#Definir el análisis
ops.constraints('Plain') 
ops.numberer('Plain') 
ops.algorithm('Linear') 
ops.system('BandGeneral') 
ops.integrator('LoadControl',1) 
ops.analysis('Static') 
ops.analyze(1) 

ops.wipeAnalysis()

#opsv.plot_model()
opsv.plot_loads_2d(nep=17, sfac=False, fig_wi_he=False, fig_lbrt=False, fmt_model_loads={'color': 'black', 'linestyle': 'solid', 'linewidth': 1.2, 'marker': '', 'markersize': 1}, node_supports=True, truss_node_offset=0, ax=False)
opsv.plot_defo(sfac=50)
opsv.section_force_diagram_2d('N',sfac=0.00005)
#ops.printModel() 
plt.show()










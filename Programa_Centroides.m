%Introducción de Datos
clear %Borrar variables
clc %Borrar pantalla
clf %Limpiar dibujo
coords =  [1 5 4;
           2 19 4;
           3 19 7;
           4 9 7;
           5 9 14;
           6 22 14;
           7 22 20;
           8 5 20;
           1 5 4; 
]

%%Programa de Centroide de Polígonos

temp = size(coords);
n = temp(1)

x = coords(:,2)
y = coords(:,3)

A = 0;

for i = 1: (n-1)
A = A + 1/2*(x(i)*y(i+1)-x(i+1)*y(i));
endfor

A 

Cx = 0;
Cy = 0;
for i = 1: (n-1)
Cx = Cx + 1/(6*A)*(x(i)+x(i+1))*(x(i)*y(i+1)-x(i+1)*y(i));
Cy = Cy + 1/(6*A)*(y(i)+y(i+1))*(x(i)*y(i+1)-x(i+1)*y(i));
endfor

Cx
Cy

plot(x,y,"linewidth",3,"color","K")
plot(Cx,Cy,"marker","o","markersize",15)
plot(Cx,Cy,"marker","+")
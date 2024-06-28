% Introducción de datos código Octave
clc
m = 175000 %kg
k = 140e6 %N/m
Sa1 = 1
Sa2 = 1
Sa3 = 1

%Cálculos
m1 = 2*m
m2 = 2*m
m3 = 1*m

k1 = 3*k
k2 = 2*k
k3 = 1*k

M = [m1 0  0; 
     0  m2 0; 
     0  0  m3]


K = [k1+k2 -k2 0;
     -k2 k2+k3 -k3;
     0 -k3  k3 ]

% Para normalizar el sistema de Eigen valores y Eigen vectores 
% a la forma A-xI = 0

kmod = K;
kmof(1,:) = kmodif(1,:)/m1; %Tomar la primera fila todas las columnas y dividirlas entre m1
kmodf(2,:) = kmodif(2,:)/m2;
kmodf(3,:) = kmodif(3,:)/m3;

kmodif

%EigenValores y EigenVectores
[A,B] = eig(kmodif) 
fi1 = (:,3)/A(3,3)
fi2 = (:,2)/A(3,2)
fi3 = (:,1)/A(3,1)

w1 = B(3,3)^0.5
w2 = B(2,2)^0.5
w3 = B(1,1)^0.5


T1 = 2*pi/w1
T2 = 2*pi/w2
T3 = 2*pi/w3

%Normalización de masas modales
M1 = f1'*M*f1
M2 = f2'*M*f2
M3 = f3'*M*f3

%Factores de excitación modal 
L1 = f1'*M*ones(3,1)
L2 = f2'*M*ones(3,1)
L3 = f3'*M*ones(3,1)

%Desplazamientos máximos de cada modo 
U1modal = f1*L1/M1*Sa1/w1^2
U2modal = f2*L2/M2*Sa2/w2^2
U3modal = f3*L3/M3*Sa3/w3^2

u1max = ((U1modal(1))^2+(U2modal(1))^2+(U3modal(1))^2)^0.5
u2max = ((U1modal(2))^2+(U2modal(2))^2+(U3modal(2))^2)^0.5
u3max = ((U1modal(3))^2+(U2modal(3))^2+(U3modal(3))^2)^0.5


%https://marcelopardo.com/ejemplo-desplazamientos-modal-espectal/ 

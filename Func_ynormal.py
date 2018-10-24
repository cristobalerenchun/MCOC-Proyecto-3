# -*- coding: utf-8 -*-

#FUNCION PARA HALLAR LA ALTURA NORMAL DE UN CANAL TRAPEZOIDAL
#USANDO NEWTON-RHAPSON (NR)

# Q   >>>  [m^3*s^-1] Caudal que debe transportar la seccion
# C_0 >>>  [SI=>1 - SB=>1.49] Factor de conversion unidades
# n   >>>  [s*m^(-1/3)] Coeficiente rugosidad de Manning
# S   >>>  [%] Pendiente longitudinal
# z   >>>  Relacion Horizontal/Vertical del talud
# b   >>>  [m] Ancho del fondo del canal


def ynormal(C_0, n, S, z, b, Q):        # Definicion de funcion ynormal
    yn = 1.0                            # Altura inicial para proceso interativo
    #Funcion de solucion
    def D(y):                           # Definicion de funcion argumento NR
        global A, P
        #Variables de calculo
        k   = (10*Q*n/(C_0*S**0.5))**3  # [m^8] Constante del modelo hidraulico 
        A   = y*(b + z*y)               # [m^2] Area mojada
        P   = b + 2*y*(z**2+1)**0.5     # [m] Perimetro mojado
        d_A = b + 2*z*y                 # [m] Derivada total de A respecto a y
        d_P = 2*(z**2+1)**0.5           # Derivada total de P respecto a y   
        #Funcion solucion y su derivada
        f   = A**5-k*P**2               # Funcion solucion f(y)=0
        d_F = 5*A**4*d_A - 2*k*P*d_P    # Derivada total  f'(y)
        return f/d_F                    # Segundo termino de ecuacion de NR
    # Proceso de aproximaciones sucesivas
    tol = abs(D(yn))                    # Tolerancia itieracion 1
    while tol > 1e-6:
        yn1 = yn - D(yn)                # Ecuacion de NR
        tol = abs(yn1-yn)               # Toleranacia del paso
        yn  = yn1                       # Mutacion de yn
    return yn

#APLICACION.
# Un canal trapezoidal de seccion constante con un coeficiente de Manning
# n= 0.013, talud lateral z = 1.25 (H:V), pendiente longigutudinal S= 0.32%,
# ancho en la base b = 9.10 m, transporta un caudal Q = 38.53 m3/s.
# Determinar la altura del flujo yn, para un estado de flujo uniforme.
# Determinar la altura del flujo yc, para un estado de flujo uniforme.

#Solucion
Altura_normal = ynormal(1.0, 0.013, 0.32, 1.25, 9.10, 38.53)
print "Altura normal yn =",Altura_normal,"m"          # Imprimiendo la solucion

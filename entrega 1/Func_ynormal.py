# -*- coding: utf-8 -*-

#FUNCIÓN PARA HALLAR LA ALTURA NORMAL DE UN CANAL TRAPEZOIDAL
#USANDO NEWTON-RAPHSON (NR)

# Q   >>>  [m^3*s^-1] Caudal que debe transportar la sección
# C_0 >>>  [SI=>1 - SB=>1.49] Factor de conversión unidades
# n   >>>  [s*m^(-1/3)] Coeficiente rugosidad de Manning
# S   >>>  [%] Pendiente longitudinal
# z   >>>  Relación Horizontal/Vertical del talud
# b   >>>  [m] Ancho del fondo del canal

def ynormal(C_0, n, S, z, b, Q):        # Definición de función ynormal
    yn = 1.0                            # Altura inicial para proceso iterativo
    #Función de solución
    def D(y):                           # Definición de función argumento NR
        global A, P
        #Variables de calculo
        k   = (10*Q*n/(C_0*S**0.5))**3  # [m^8] Constante del modelo hidráulico 
        A   = y*(b + z*y)               # [m^2] Área mojada
        P   = b + 2*y*(z**2+1)**0.5     # [m] Perímetro mojado
        d_A = b + 2*z*y                 # [m] Derivada total de A respecto a y
        d_P = 2*(z**2+1)**0.5           # Derivada total de P respecto a y   
        #Función solución y su derivada
        f   = A**5-k*P**2               # Función solución f(y)=0
        d_F = 5*A**4*d_A - 2*k*P*d_P    # Derivada total  f'(y)
        return f/d_F                    # Segundo termino de ecuación de NR
    # Proceso de aproximaciones sucesivas
    tol = abs(D(yn))                    # Tolerancia iteración 1
    while tol > 1e-6:
        yn1 = yn - D(yn)                # Ecuación de NR
        tol = abs(yn1-yn)               # Tolerancia del paso
        yn  = yn1                       # Mutación de yn
    return yn

#APLICACIÓN.
# Un canal trapezoidal de sección constante con un coeficiente de Manning
# n= 0.013, talud lateral z = 1.25 (H:V), pendiente longitudinal S= 0.32%,
# ancho en la base b = 9.10 m, transporta un caudal Q = 38.53 m3/s.
# Determinar la altura del flujo yn, para un estado de flujo uniforme.
# Determinar la altura del flujo yc, para un estado de flujo uniforme.

#Solución
Altura_normal = ynormal(1.0, 0.013, 0.32, 1.25, 9.10, 38.53)
print "Altura normal yn =",Altura_normal,"m"          # Imprimiendo la solución

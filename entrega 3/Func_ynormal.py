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
        T   = b + 2*z*y                 # [m] Derivada total de A respecto a y
        d_P = 2*(z**2+1)**0.5           # Derivada total de P respecto a y   
        #Función solución y su derivada
        f   = A**5 - k*P**2             # Función objetivo f(y)=0
        d_F = 5*A**4*T - 2*k*P*d_P    # Derivada total  f'(y)
        return f/d_F                    # Segundo termino de ecuación de NR
    # Proceso de aproximaciones sucesivas
    tol = abs(D(yn))                    # Tolerancia iteración 1
    while tol > 1e-6:
        yn1 = yn - D(yn)                # Ecuación de NR
        tol = abs(yn1 - yn)             # Tolerancia del paso
        yn  = yn1                       # Mutación de yn
    return yn

#EJERCICIOS DE APLICACIÓN.
#Solución
print "Canal 1, Altura normal yn =",ynormal(1.0, 0.013, 0.32, 1.25, 9.10, 38.53),"m"
print "Canal 2, Altura normal yn =",ynormal(1.0, 0.016, 0.26, 8.00, 0.0, 0.72),"m"
print "Canal 3, Altura normal yn =",ynormal(1.0, 0.009, 0.80, 0.00, 0.50, 0.15),"m"

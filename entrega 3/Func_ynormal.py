# -*- coding: utf-8 -*-

#FUNCIÓN PARA HALLAR LA ALTURA NORMAL DE UN CANAL TRAPEZOIDAL
#USANDO NEWTON-RAPHSON (NR)

# Argumentos de la función:
# units >>>[SI=> C_0 = 1.00 - SB=>C_0 = 1.49]
# n     >>>  [s*m^(-1/3) o pie^3*s^-1] Coeficiente rugosidad de Manning
# S     >>>  [%] Pendiente longitudinal
# z     >>>  Relación Horizontal/Vertical del talud
# b     >>>  [m o pie] Ancho del fondo del canal
# Q     >>>  [m^3*s^-1 o pie^3*s^-1] Caudal que debe transportar la sección

def ynormal(Units, n, S, z, b, Q):         # Definición de función ynormal
    yn = 1.0                               # Altura inicial para proceso iterativo
    # Condición del sistema de unidades (SI o SB)
    if Units == "SI":
        C_0  = 1.00                  
    else:
        C_0  = 1.49 
    # Función objetivo
    def D(y):                              # Definición de función argumento NR
        global A, P
        # Variables de calculo
        k   = (10.*Q*n/(C_0*S**0.5))**3.   # [m^8 o pie^8] Constante del modelo hidráulico 
        A   = y*(b + z*y)                  # [m^2 o pie^2] Área mojada
        P   = b + 2.*y*(z**2.+1.)**0.5     # [m o pie] Perímetro mojado
        T   = b + 2.*z*y                   # [m o pie] Derivada total de A respecto a y
        d_P = 2*(z**2+1)**0.5              # Derivada total de P respecto a y   
        # Función objetivo y su derivada total
        f   = A**5. - k*P**2.              # Función objetivo f(y)=0
        d_F = 5.*A**4.*T - 2.*k*P*d_P      # Derivada total  f'(y)
        return f/d_F                       # Segundo termino de ecuación de NR
    # Proceso de aproximaciones sucesivas
    tol = abs(D(yn))                       # Tolerancia iteración 1
    while tol > 1e-6:
        yn1 = yn - D(yn)                   # Ecuación de NR
        tol = abs(yn1 - yn)                # Tolerancia del paso
        yn  = yn1                          # Mutación de y
    return yn                              # [m o pie] altura normal del canal

#EJERCICIOS DE APLICACIÓN.
#Solución
print "Canal 1, Altura normal yn =",ynormal("SI", 0.013, 0.32, 1.25, 9.10, 38.53)
print "Canal 2, Altura normal yn =",ynormal("SI", 0.016, 0.26, 8.00, 0.0, 7.2)
print "Canal 3, Altura normal yn =",ynormal("SI", 0.009, 0.80, 0.00, 0.50, 0.15)

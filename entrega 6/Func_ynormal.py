# -*- coding: utf-8 -*-

# FUNCIÓN PARA HALLAR LA ALTURA NORMAL DE UN CANAL TRAPEZOIDAL
# DE SECCIÓN SIMETRICA GENERAL, USANDO NEWTON-RAPHSON (NR)

# Argumentos de la función:
# units >>>  [SI=> C_0 = 1.00 - SB=>C_0 = 1.49]
# n     >>>  [s*m^(-1/3) o pie^3*s^-1] Coeficiente rugosidad de Manning
# S     >>>  [m/m o pie/pie] Pendiente longitudinal
# z     >>>  Relación Horizontal/Vertical del talud
# b     >>>  [m o pie] Ancho del fondo del canal
# Q     >>>  [m^3*s^-1 o pie^3*s^-1] Caudal que debe transportar la sección

from Func_ycritical import ycritical
# Argumentos función = ycritical(units, z, b, Q)

# FUNCIÓN PRINCIPAL
def ynormal(units, n, S, z, b, Q):
    yn = ycritical(units, z, b, Q)         # Altura inicial para proceso iterativo
    # Condición del sistema de unidades:
    if units == 'SI':
        C_0  = 1.00                        # Factor de conversión unidades (SI)
    else:
        C_0  = 1.49                        # Factor de conversión unidades (SB)
    # Función de aproximación:
    def D(y):                              # Definición de función argumento NR
        global A, P
        # Parámetros de calculo:
        k   = (Q*n/(C_0*S**0.5))**3.       # [m^8 o pie^8] Constante del modelo hidráulico 
        A   = y*(b + z*y)                  # [m^2 o pie^2] Área mojada
        P   = b + 2.*y*(z**2.+1.)**0.5     # [m o pie] Perímetro mojado
        T   = b + 2.*z*y                   # [m o pie] Ancho superficial (dA/dy)
        dP  = 2.*(z**2.+1.)**0.5           # Derivada total de P respecto a y (dP/dy)  
        # Función objetivo y su derivada total
        f   = A**5. - k*P**2.              # Función objetivo f(y)=0
        df  = 5.*A**4.*T - 2.*k*P*dP       # Derivada total df(y)/dy
        return f/df                        # Segundo termino de ecuación de NR
    # Proceso de aproximaciones sucesivas:
    tol = abs( D(yn) )                     # Tolerancia iteración 1
    while tol > 1e-6:
        yn1 = yn - D(yn)                   # Ecuación de NR
        tol = abs(yn1 - yn)                # Tolerancia del paso
        yn  = yn1                          # Mutación de y
    return yn                              # [m o pie] altura normal del canal
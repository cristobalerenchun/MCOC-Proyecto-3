# -*- coding: utf-8 -*-

#FUNCIÓN PARA HALLAR LA ALTURA CRITICA DE UN CANAL TRAPEZOIDAL
#USANDO NEWTON-RAPHSON (NR)

# Argumentos de la función:
# units >>>  [SI=> g = 9.91 m*s^-2 - SB=> g = 32.2 pie*s^-2]
# z     >>>  Relación Horizontal/Vertical del talud lateral
# b     >>>  [m o pie] Ancho del fondo del canal
# Q     >>>  [m^3*s^-1 o pie^3*s^-1] Caudal transporta la sección

def ycritical(units, z, b, Q):
    # Condición sistema de unidades (SI o SB):
    if units == 'SI':
        g  = 9.81                               # [SI ==> m*s^-2] Gravedad nominal terrestre
    else:
        g  = 32.2                               # [SB ==> pie*s^-2] Gravedad nominal terrestre
    # yc para aplicación eficiente de NR:
    c   = g*b**5./z**3.
    yc  = 1./(8.*g*z**2.)**0.2*(abs(c**0.2 - (c**0.4 + 4.*Q)**0.5))**0.8
    Fr1 = (b + z*yc)/(b + 2.*z*yc)
    Fr2 = 2.*Fr1
    Q2  = 0.25*((c*Fr1)**0.2 - ((c*Fr1)**0.4 + 4.*Q)**0.5)**2.
    yc  = (2./g*(Q2/z)**2./Fr2)**0.2            # Magnitud aproximada (85% < yc < 1.15%)
    # Función de refinamiento de la raiz:
    def D(y):                                   # Definición de función argumento NR
        global A, P
        # Parámetros de calculo:
        k   = Q**2./g                           # [m^5 o pie^5] Constante del modelo 
        A   = y*(b + z*y)                       # [m^2 o pie^2] Área mojada
        T   = b + 2.*z*y                        # [m o pie] Ancho superficial (dA/dy)
        dT  = 2.*z                              # Derivada total de T respecto a y (dT/dy)  
        # Función objetivo y su derivada total:
        f   = A**3. - k*T                       # Función objetivo f(y) = 0
        df  = 3.*A**2.*T - k*dT                 # Derivada total  df(y)/dy
        return f/df                             # Segundo termino de formula de NR
    # Proceso de aproximaciones sucesivas:
    tol = abs(D(yc))                            # Tolerancia iteración 1
    while tol > 1e-10:
        yc1 = yc - D(yc)                        # Formula de NR
        tol = abs(yc1-yc)                       # Tolerancia del paso
        yc  = yc1                               # Mutación de y
    return yc                                   # [m o pie] altura critica
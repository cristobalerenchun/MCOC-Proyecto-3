# -*- coding: utf-8 -*-

#FUNCIÓN PARA HALLAR LA ALTURA CRITICA DE UN CANAL TRAPEZOIDAL
#USANDO NEWTON-RAPHSON (NR)

# Q   >>>  [m^3*s^-1] Caudal que debe transportar la sección
# C_0 >>>  [SI=>1 - SB=>1.49] Factor de conversión unidades
# z   >>>  Relación Horizontal/Vertical del talud
# b   >>>  [m] Ancho del fondo del canal

def ycritical(C_0, z, b, Q):       # Definición de función ycritical
    yc = 1.0                       # Altura inicial para proceso iterativo
    #Función de solución
    def D(y):                      # Definición de función argumento NR
        global A, P
        #Variables de calculo
        k   = Q**2/9.81            # [m^2*s] Constante del modelo 
        A   = y*(b + z*y)          # [m^2] Área mojada
        T   = b + 2*z*y            # [m] Derivada total de A respecto a y
        d_T = 2*z                  # Derivada total de T respecto a y   
        #Función solución y su derivada
        f   = A**3 - k*T           # Función objetivo f(y) = 0
        d_F = 3*A**2*T - k*d_T     # Derivada total  f'(y)
        return f/d_F               # Segundo termino de ecuación de NR
    # Proceso de aproximaciones sucesivas
    tol = abs(D(yc))               # Tolerancia iteración 1
    while tol > 1e-6:
        yc1 = yc - D(yc)           # Ecuación de NR
        tol = abs(yc1-yc)          # Tolerancia del paso
        yc  = yc1                  # Mutación de yn
    return yc

#EJEMPLOS DE APLICACIÓN:
#Solución
print "Canal 1, yc =",ycritical(1.0, 1.25, 9.10, 38.53),"m"
print "Canal 2, yc =",ycritical(1.0, 8.0, 0.0, 7.2),"m"
print "Canal 3, yc =",ycritical(1.0, 0.0, 0.50, 0.15),"m"

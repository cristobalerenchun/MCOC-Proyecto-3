# -*- coding: utf-8 -*-

#FUNCIÓN PARA HALLAR LA ALTURA CRITICA DE UN CANAL TRAPEZOIDAL
#USANDO NEWTON-RAPHSON (NR)

# Argumentos de la función:
# units >>>  [SI=> g = 9.91 m*s^-2 - SB=> g = 32.2 pie*s^-2]
# z     >>>  Relación Horizontal/Vertical del talud lateral
# b     >>>  [m o pie] Ancho del fondo del canal
# Q     >>>  [m^3*s^-1 o pie^3*s^-1] Caudal transporta la sección

def ycritical(units, z, b, Q):     # Definición de función ycritical
    yc = 1.0                       # Altura inicial para proceso iterativo
     #Condición del sistema de unidades (SI o SB)
    if units == "SI":
        g  = 9.81                  # [SI=> 9.81 m*s^-2] Gravedad nominal terrestre
    else:
        g  = 32.2                  # [SB=> 32.2 pie*s^-2] Gravedad nominal terrestre
    #Función de solución
    def D(y):                      # Definición de función argumento NR
        global A, P
        #Variables de calculo
        k   = Q**2./g              # [m^5 o pie^5] Constante del modelo 
        A   = y*(b + z*y)          # [m^2 o pie^2] Área mojada
        T   = b + 2.*z*y           # [m o pie] Ancho superficial (dA/dy)
        dT  = 2.*z                 # Derivada total de T respecto a y (dT/dy)  
        #Función objetivo y su primera derivada total
        f   = A**3. - k*T          # Función objetivo f(y) = 0
        df  = 3.*A**2.*T - k*dT    # Derivada total  df(y)/dy
        return f/df                # Segundo termino de formula de NR
    # Proceso de aproximaciones sucesivas
    tol = abs(D(yc))               # Tolerancia iteración 1
    while tol > 1e-6:
        yc1 = yc - D(yc)           # Formula de NR
        tol = abs(yc1-yc)          # Tolerancia del paso
        yc  = yc1                  # Mutación de y
    return yc                      # [m o pie] altura critica

#EJEMPLOS DE APLICACIÓN:
#Solución
print "Canal 1, yc =",ycritical("SI", 1.25, 9.10, 38.53)
print "Canal 2, yc =",ycritical("SI", 8.0, 0.0, 7.2)
print "Canal 3, yc =",ycritical("SI", 0.0, 0.50, 0.15)

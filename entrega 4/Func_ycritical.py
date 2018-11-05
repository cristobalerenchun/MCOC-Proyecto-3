# -*- coding: utf-8 -*-

#FUNCIÓN PARA HALLAR LA ALTURA CRITICA DE UN CANAL TRAPEZOIDAL
#USANDO NEWTON-RAPHSON (NR)

# Q   >>>  [m^3*s^-1 o pie^3*s^-1] Caudal que debe transportar la sección
# g   >>>  Gravedad nominal terrestre [SI=> 9.81 m*s^-2 - SB=> 32.2 pie*s^-2]
# z   >>>  Relación Horizontal/Vertical del talud
# b   >>>  [m o pie] Ancho del fondo del canal

def ycritical(C_0, z, b, Q):       # Definición de función ycritical
    yc = 1.0                       # Altura inicial para proceso iterativo
     #Condición del sistema de unidades (SI o SB)
    if Units == "SI":
        g  = 9.81
    else:
        g  = 32.2
    #Función de solución
    def D(y):                      # Definición de función argumento NR
        global A, P
        #Variables de calculo
        k   = Q**2/9.81            # [m^5 o pie^5] Constante del modelo 
        A   = y*(b + z*y)          # [m^2 o pie^2] Área mojada
        T   = b + 2*z*y            # [m o pie] Derivada total de A respecto a y
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
    return yc                      # [m o pie] altura critica

#EJEMPLOS DE APLICACIÓN:
#Solución
print "Canal 1, yc =",ycritical("SI", 1.25, 9.10, 38.53)
print "Canal 2, yc =",ycritical("SI", 8.0, 0.0, 7.2)
print "Canal 3, yc =",ycritical("SI", 0.0, 0.50, 0.15)

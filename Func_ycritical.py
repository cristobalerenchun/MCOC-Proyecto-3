#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 20:45:00 2018

@author: jespildora
"""
#FUNCION PARA HALLAR LA ALTURA CRITICA DE UN CANAL TRAPEZOIDAL
#USANDO NEWTON-RHAPSON (NR)

# Q   >>>  [m^3*s^-1] Caudal que debe transportar la seccion
# z   >>>  Relacion Horizontal/Vertical del talud
# b   >>>  [m] Ancho del fondo del canal

def ycritical(q,b,z):
    yc=1.0                                                                                    # Altura inicial para proceso interativo    
    def    f(q,b,z,y):                                                                        # Funcion solucion f(y)=0
            A   = y*(b + z*y)                                                                 # [m^2] Area mojada
            T   = b + 2*z*y                                                                   # [m] Perimetro Mojado
            return ((A**3)/T)-((q**2)/9.81)                                                   # Funcion solucion f(y)=0
    def    d_F(q,b,z,y):                                                                      
            return ((y**2)*((b+y*z)**2)*(3*(b**2)+10*b*y*z+10*(y**2)*(z**2)))/((b+2*y*z)**2)  # Derivada total  f'(y)
    # Proceso de aproximaciones sucesivas
    tol = abs(f(38.53,9.1,1.25,yc)/d_F(38.53,9.1,1.25,yc))          # Tolerancia itieracion 1
    while tol > 1e-6 and d_F(38.53,9.1,1.25,yc)!=0:                 # Condiciones de NR
        yc1 = yc - f(38.53,9.1,1.25,yc)/d_F(38.53,9.1,1.25,yc)      # Ecuacion de NR
        tol = abs(yc1-yc)                                           # Toleranacia del paso
        yc  = yc1                                                   # Mutacion de yn
    return yc

#APLICACION.
# Un canal trapezoidal de seccion constante con un coeficiente de Manning
# n= 0.013, talud lateral z = 1.25 (H:V), pendiente longigutudinal S= 0.32%,
# ancho en la base b = 9.10 m, transporta un caudal Q = 38.53 m3/s.
# Determinar la altura del flujo yc, para un estado de flujo uniforme.

#Solucion
Altura_critica = ycritical(38.53,9.10,1.25)
print "Altura critica yc =",Altura_critica,"m"          # Imprimiendo la solucion 
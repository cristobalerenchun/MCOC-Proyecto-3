# -*- coding: utf-8 -*-

# FUNCIÓN PARA CALCULAR LA ALTURA DEL AGUA DE UN FLUJO GRADUALMENTE VARIADO (FGV)
# DE UNA SECCIÓN TRAPEZOIDAL SIMÉTRICA GENERAL

# Argumentos de la función:
# units > [SI=> C_0 = 1 y g = 9.91m*s^-2 - SB=>C_0 = 1.49 y g = 32.2 pie*s^-2]
# b   >>> [m o pie] Ancho del fondo del canal
# z   >>> Relación Horizontal/Vertical del talud lateral
# y   >>> [m o pie] Profundidad del agua en la sección
# n   >>> [s*m^(-1/3) o pie^3*s^-1] Coeficiente rugosidad de Manning
# Q   >>> [m^3*s^-1 o pie^3*s^-1] Caudal que debe transportar la sección
# S   >>> [%] Pendiente longitudinal del tramo
# T   >>> [m o pie] Ancho superficial de la sección
# A   >>> [m^2 o pie^2] Área mojada de la sección
# R   >>> [m o pie] Radio hidráulico de la sección
# dx  >>> [m o pie] Longitud en un plano horizontal entre sección 1 y 2

# FUNCIONES DE APOYO
from Func_geom import geom
import math
# Función para cálculo de parámetros hidráulicos en una sección:
def hidr(units, b, z, y, n, Q, S, T, A, R):
	global theta, alpha
	theta = math.atan(S)							# [rad] Angulo de inclinación del fondo
	alpha = 1.0										# Coeficiente de Coriolis
	# Condición del sistema de unidades (SI o SB):
	if units == 'SI':
		C_0 = 1.00									# Factor de conversión unidades (SI)
		g   = 9.81									# [m*s^-2 o pie*s^-2] Gravedad nominal terrestre [SI]
	else:
		C_0 = 1.49									# Factor de conversión unidades [SB]
		g   = 32.2									# [m*s^-2 o pie*s^-2] Gravedad nominal terrestre [SB]
	# Parámetros hidráulicos:
	K  = C_0*A*R**(2./3.)/n   				 		# Conductividad hidráulica del modelo
	Sf = (Q/K)**2.							 		# [m/m o pie/pie] Gradiente de energía	
	V  = Q/A 										# [m/s o pie/] Velocidad media
	E  = y*math.cos(theta)**2.+alpha*V**2./(2.*g) 	# [m o pie] Energía especifica
	Fr = V/(g*geom(b, z, y)['D'])**0.5			 	# Numero de Froude
	# Guardado parámetros en diccionario:
	return {'V':V, 'Sf':Sf, 'E':E, 'Fr':Fr}

# FUNCIÓN PRINCIPAL DEL FLUJO GRADUALMENTE VARIADO
def NR_FGV(units, b, z, y1, n, Q, S, dx):
	# Datos sección transversal 1:
	st1 = geom(b, z, y1)						                        	# Parámetros geométricos sección 1
	hd1 = hidr(units, b, z, y1, n, Q, S, st1['T'], st1['A'], st1['R'])	 	# Parámetros hidráulicos sección 1
	# Calculo profundidad y2 usando NR:
	y2  = 0.95*y1															# Profundidad inicial sección 2
	tol = abs(y2 - y1)														# Tolerancia de inicio
	while tol > 1e-15:
		# Datos sección transversal 2:
		st2 = geom(b, z, y2)												# Parámetros geométricos sección 2
		hd2 = hidr(units, b, z, y2, n, Q, S, st2['T'], st2['A'], st2['R'])	# Parámetros hidráulicos sección 2
		# Función objetivo y primera derivada total:
		f   = hd2['E'] - hd1['E'] + 0.5*(hd2['Sf'] + hd1['Sf'] - 2*S)*dx    # f(y2)=0
		df  = math.cos(theta)**2. - alpha*hd2['Fr']**2. - dx*hd2['Sf']*(5.*st2['T'] - 2.*st2['dP/dy']/st2['R'])/3.
		# Proceso de aproximaciones sucesivas:
		y_i = y2 - f/df								# Formula de NR
		tol = abs(y_i - y2)							# Tolerancia del paso
		y2  = y_i           						# Mutación de y
	return y2
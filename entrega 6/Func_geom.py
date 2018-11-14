# -*- coding: utf-8 -*-

# FUNCIÓN PARA CALCULAR LOS PARÁMETROS GEOMÉTRICOS
# DE UNA SECCIÓN TRAPEZOIDAL SIMÉTRICA GENERAL

# Argumentos de la función:
# b >>> [m o pie] Ancho del fondo del canal
# z >>> Relación Horizontal/Vertical del talud lateral
# y >>> [m o pie] Profundidad del agua

def geom(b, z, y):
	# Parámetros geométricos:
	A  = y*(b + y*z)				# [m^2 o pie^2] Área mojada
	T  = b + 2.*y*z					# [m o pie] Ancho superficial
	P  = b + 2.*y*(z**2.+1.)**0.5	# [m o pie] Perímetro mojado
	dP = 2.*(z**2.+1)**0.5			# Derivada total de T respecto a y
	R  = A/P 					    # [m o pie] Radio hidráulico
	D  = A/T 					    # [m o pie] Profundidad hidráulica
	# Guardado parámetros en diccionario:
	return {'A':A ,'T':T ,'P':P, 'dP/dy':dP,'R':R, 'D':D}
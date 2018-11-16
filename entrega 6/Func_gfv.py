# -*- coding: utf-8 -*-

# FUNCIÓN PARA CALCULAR EL PERFIL UNIDIMENSIONAL DE LA SUPERFICIE DEL AGUA PARA UN
# FLUJO GRADUALMENTE VARIADO (FGV) DE UNA SECCIÓN TRAPEZOIDAL SIMÉTRICA GENERAL

# Argumentos de la función:
# units 	 >>> [SI=> Sistema internacional - SB=> Sistema británico]
# b     	 >>> [m o pie] Ancho del fondo del canal
# z     	 >>> Relación Horizontal/Vertical del talud lateral
# n     	 >>> [s*m^(-1/3) o pie^3*s^-1] Coeficiente rugosidad de Manning
# Q     	 >>> [m^3*s^-1 o pie^3*s^-1] Caudal permanente que transporta el canal
# S     	 >>> [m/m o pie/pie] Pendiente longitudinal del canal
# dx    	 >>> [m o pie] Longitud del paso estándar
# control 	 >>> [DS=> Aguas abajo ó US => Aguas arriba] Ubicación del control de flujo
# y     	 >>> [m o pie] Profundidad del agua en la sección de control (Altura conocida)
# elev_control > [m o pie] Elevación en la sección de control

# Funciones auxiliares:
from numpy       import array
from Func_NR_FGV import NR_FGV
	# Argumentos = (units, b, z, y1, n, Q, S, dx, control)

def gfv(units, b, z, n, Q, S, dx, control, y_control, elev_control, y_final):
	# Valores iniciales de los vectores:
	x0 = 0.					# Distancia inicial
	y0 = y_control				# Altura de agua conocida e incial
	z0 = elev_control			# Elevación inicial en sección de control
	# Listas para guardado de datos:
	X  = [x0]				# Inicializando lista de distancia horizontal
	Y  = [y0]				# Inicializando lista de alturas del agua
	Z  = [z0]				# Inicializando lista elevación fondo del canal
	# Ubicación del control de flujo:
	if control == 'DS':			# Control aguas abajo [Downstream: 'DS']
		a = -1.
	else:					# Control aguas arriba [Upstream: 'US']
		a = +1.
	# Generando listas de datos:
	i  = 0					# Indice de la lista
	dy = 1e-6				# Criterio de finalización del proceso
	criterio = True				# Criterio de inicio del proceso

	while criterio and i < 1e6:
		# Calculando datos para cada estación i+1:
		X.append(X[i] + dx)						# Distancia horizontal
		Y.append(NR_FGV(units, b, z, Y[i], n, Q, S, dx, control))	# Alturas del agua
		Z.append(Z[i] - a*S*dx)						# Elevacion fondo del canal
		i  = i + 1							# Mutación del índice
		# Evaluando el criterio del proceso:
		if y_control < y_final:
			criterio = Y[i] < y_final
		else:
			criterio = Y[i] > y_final + dy
	# Elevación superficie del agua:
	elsa = array(Y) + array(Z)					
	return [X, Y, Z, elsa]	# Notese que la función proporciona una lista de tres (3) "columnas"

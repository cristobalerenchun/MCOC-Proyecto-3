# -*- coding: utf-8 -*-

# META 6 (GOAL 6). PROBLEMA DE APLICACIÓN:

# Use su código (gvf) para calcular la elevación de la superficie del agua de un canal trapezoidal
# que tiene una pendiente longitudinal de 0.001, transportando un caudal de 30 metros cúbicos por
# segundo. El ancho basal es de 10 metros, y la relación de la inclinación lateral de los muros es
# 2H a 1V. Una presa de concreto construida aguas abajo al final del trayecto eleva la profundidad
# del agua a 5 m. Calcule el perfil de la superficie del agua, teniendo en cuenta un coeficiente de
# Manning de 0.013 para el canal. 


# SOLUCIÓN DEL PROBLEMA

# Llamando las funciones requeridas:
from Func_ycritical import ycritical
	# Argumentos = (units, z, b, Q)
from Func_ynormal   import ynormal
	# Argumentos = (units, z, b, Q)
from Func_profile   import gvf_profile
	# Argumentos = (units, b, z, n, Q, S, dx, control, y_control, elev_control, y_final, muros)

	# Descripción:
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
	# y_final    >>> [m o pie] Profundidad esperada en el extremo opuesto al control
	# muros      >>> [m o pie] Altura de los muros laterales del canal


# Argumentos explícitos:
u   = 'SI' # Argumento: units
	# u >>> Debido que todos los datos dados en el problema se presentan en el sistema
	# internacional de unidades se asignó el valor 'SI' respectivo.

b, z, n, Q, S = 10., 2., 0.013, 30., 0.001  # [Cada unidad de medida dada en el enunciado]


# Argumentos complementarios:
z_i=100.# [metros] Argumento: elev_control
	# z_i >>> Con el objetivo de producir un gráfico con estética adecuada y dado el contexto del
	# problema, se consideró pertinente adoptar una elevación para la sección de control diferente
	# de cero; la cual es arbitraria y no interviene en los cálculos respectivos, únicamente tiene
	# efectos sobre la visualización gráfica de los resultados.

h_wll = 5.3 # [metros] Argumento: muros
	# Debido que el problema no define de forma clara cuál es la altura de los muros del canal, se
	# adoptó a criterio el uso de muros hasta una altura igual a la profundidad en la zona de la
	# presa, mas 30 cm de borde libre. Los muros se incorporan en el grafico únicamente con el
	# objeto de dotar de contexto gráfico los resultados.


# Análisis cualitativo del perfil para adopción de argumentos no explícitos:
yc = ycritical(u, z, b, Q)			# (0.9116) [m] Altura critica
yn = ynormal(u, n, S, z, b, Q)		# (1.091 ) [m] Altura normal
print 'yc=', yc, '- yn=', yn		# Resultados de profundidad normal y critica

# La altura normal es mayor que la altura critica (yn>yc) y entonces el flujo normal es
# Subcrítico, en efecto la pendiente (S) es "suave" (S<Sc). Por otro lado, la altura
# conocida aguas abajo (y=5.0m) es >yn>yc; esto suscita que la altura aguas arriba deba
# ser igual a la altura normal (yn); no obstante, no se conoce la ubicación de esta sección.
# De acuerdo lo anterior, se dispone de la información y claridad cualitativa del comportamiento
# del perfil para seleccionar convenientemente la sección de control ('ctrl'), la profundidad
# (y_control) y la profundidad esperada en el extremo final (y_final).

# A partir de la ecuación fundamental del flujo gradualmente variado, es más conveniente 
# desarrollar el computo numérico con aproximaciones hacia la altura normal (yn), de esta manera
# se garantiza la precisión de la altura en la sección conocida, y también la estabilidad de
# computo para un espectro más amplio del paso estándar (dx).

# En síntesis, la sección de control se establece aguas abajo (Downstream), donde la altura es
# conocida y la sección esperada aguas arriba corresponderá al desarrollo del flujo normal. Por
# tanto, se adoptan los argumentos:

ctrl   = 'DS'	# (Downstream) Argumento: control
y_ctrl =  5.	# [# metros]   Argumento: y_control
y_end  = yn		# [# metros]   Argumento: y_final

# El paso estándar (dx) fue establecido mediante análisis de "sensibilidad" calculando el perfil
# usando todos los argumentos ya definidos, usando valores de dx a partir de 0.1 m variando en
# incrementos de 0.1 m; donde, hasta una medida de 0.5m no se obtuvo cambio en los resultados;
# sin embargo, para una magnitud de 1.0 m, se obtuvo una diferencia de 0.8m en la localización de
# la sección en flujo uniforme. Debido que esta diferencia no es representativa, versus la longitud
# total de desarrollo del flujo uniforme se consideró adecuada emplearla en el análisis,
# considerando que valores dx > 1.0 arrojaron diferencias no submétricas y además esta permite
# reducir a la mitad la cantidad de datos y cálculos que resulta de emplear el paso dx=0.5m
# donde no se observó cambios en el resultado.

dx  = 1.	# [metro]


# Implementación de la función gfv en generación de perfil gráfico mediante función gvf_profile:
perfil   = gvf_profile(u, b, z, n, Q, S, dx, ctrl, y_ctrl, z_i, y_end, h_wll)

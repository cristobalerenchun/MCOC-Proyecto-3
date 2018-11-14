# -*- coding: utf-8 -*-

# META 6 (GOAL 6). PROBLEMA DE APLICACIÓN:
# Use su código (gvf) para calcular la elevación de la superficie del agua de un canal trapezoidal que tiene una
# pendiente longitudinal de 0.001, transportando un caudal de 30 metros cúbicos por segundo. El ancho basal es de
# 10 metros, y la relación de la inclinación lateral de los muros es 2H a 1V. Una presa de concreto construida aguas
# abajo al final del trayecto eleva la profundidad del agua a 5 m. Calcule el perfil de la superficie del agua,
# teniendo en cuenta un coeficiente de Manning de 0.013 para el canal. 

# SOLUCIÓN DEL PROBLEMA
# Llamando las funciones requeridas:
from numpy          import array
from matplotlib     import pyplot
from Func_ynormal   import ynormal
	# Argumentos = ynormal(units, n, S, z, b, Q)
from Func_ycritical import ycritical
	# Argumentos = ycritical(units, z, b, Q)
from Func_gfv       import gfv
	#Argumentos = gfv(units, b, z, n, Q, S, dx, control, y_control, elev_control):

# Descripción de argumentos de asignación:
	# units   >>> [SI=> Sistema internacional - SB=> Sistema británico]
	# control >>> [DS=> Aguas abajo ó US => Aguas arriba] Ubicación del control de flujo

# Argumentos explícitos:
b, z, n, Q, S = 10., 2., 0.013, 30., 0.001  # Dados explícitamente en el problema
# Argumentos interpretados:
u      = 'SI'
	# u >>> Debido que todos los datos dados en el problema se presentan en el sistema internacional de unidades
	# se asignó el valor 'SI' respectivo.
ctrl   = 'DS'
	# ctrl >>> La altura conocida del problema se encuentra aguas abajo al final del tramo, correspondiente a  
	# la profundidad que suscita la presa; por tanto, se asigna el valor 'DS' (Downstream).
y_ctrl =  5.
	# y_ctrl >>> Corresponde a la altura y conocida del problema en la sección de control.

# Argumentos adoptados para solución:
dx  = 1.# [metro]
	# dx >>> Fue definido mediante análisis de "sensibilidad" calculando el perfil para valores de dx a partir de 0.1 m
	# variando en incrementos de 0.1 m; donde, hasta una medida de 0.5 m no se obtuvo cambio en los resultados; sin
	# embargo, para una magnitud de 1.0 m, se obtuvo una diferencia de 0.8m en la localización de la sección en flujo
	# uniforme. Debido que esta diferencia no es representativa, versus la longitud total de desarrollo del flujo
	# uniforme se consideró adecuada emplearla en el análisis, considerando que valores dx > 1.0 arrojaron diferencias no
	# sub-metricas.

z_i=100.# [metros]
	# z_i >>> Con el objetivo de producir un gráfico con estética adecuada y dado el contexto del problema, se consideró
	# pertinente adoptar una elevación para la sección de control diferente de cero; la cual es arbitraria y no interviene
	# en los cálculos respectivos, unicamente tiene efectos sobre la vizualización gráfica de los resultados. 

# Implementación de la función gfv:
perfil = gfv(u, b, z, n, Q, S, dx, ctrl, y_ctrl, z_i) # Notese que la función proporciona una lista de tres (3) "columnas".
# Datos adicionales solicitados:
yn       = ynormal(u, n, S, z, b, Q)	                   # Altura normal del canal (para incorporar en el gráfico)
yc       = ycritical(u, z, b, Q)	                   # Altura critica del canal (para incorporar en el gráfico)
normal   = yn + array(perfil[2])                           # Vector de altura normal a graficar
critical = yc + array(perfil[2])                           # Vector de altura critica a graficar

walls    = max(array(perfil[1])) + 0.3 + array(perfil[2])  # Vector que representa la corona de los muros del canal
	# Debido que el problema no define de forma clara cuál es la altura de los muros del canal, se adoptó a criterio el
	# uso de muros hasta una altura igual a la profundidad máxima del agua del perfil, mas 30 cm de borde libre. Los muros
	# se incorporan en el grafico únicamente con el objeto de dotar de contexto gráfico los resultados.

# Graficando la solución:
pyplot.axis([perfil[0][0], perfil[0][-1], perfil[2][0]-1., walls[-1] + 2.])
pyplot.xlabel('Distancia, metros')
pyplot.ylabel('Elevacion, metros')
pyplot.title('PERFIL DE FLUJO GRADUALMENTE VARIADO')
pyplot.plot(perfil[0], perfil[2], 'k', linewidth=4)     # Línea del fondo del canal
pyplot.plot(perfil[0], normal, 'k--')			# Línea de altura normal
pyplot.plot(perfil[0], critical, 'k:')			# Línea de altura critica
pyplot.plot(perfil[0], perfil[3], 'b', linewidth=2)	# Línea de superficie del agua
pyplot.plot(perfil[0], walls, 'k')			# Línea de la corona del muro lateral
pyplot.legend(['Fondo del canal', 'Altura normal', 'Altura critica' , 'Superficie del agua', 'Muros del canal'])
pyplot.show()

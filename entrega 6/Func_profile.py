# -*- coding: utf-8 -*-

# FUNCIÓN PARA GRAFICAR EL PERFIL UNIDIMENSIONAL DE LA SUPERFICIE DEL AGUA PARA UN
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
# y_final    >>> [m o pie] Profundidad esperada en el extremo opuesto al control
# muros      >>> [m o pie] Altura de los muros laterales del canal

# Llamando funciones axuliares:
import numpy             as np
import matplotlib.pyplot as plt
from numpy          import array
from Func_ynormal   import ynormal
	# Argumentos = (units, n, S, z, b, Q)
from Func_ycritical import ycritical
	# Argumentos = (units, z, b, Q)
from Func_gfv       import gfv
	# Argumentos = (units, b, z, n, Q, S, dx, control, y_control, elev_control):


def gvf_profile(units, b, z, n, Q, S, dx, control, y_control, elev_control, y_final, muros):
	# Implementación de la función gfv:
	profile  = gfv(units, b, z, n, Q, S, dx, control, y_control, elev_control, y_final)
	# Datos adicionales:
	yn       = ynormal(units, n, S, z, b, Q)	   # Altura normal (para incorporar en el gráfico)
	yc       = ycritical(units, z, b, Q)	       # Altura critica (para incorporar en el gráfico)
	Z        = profile[2]
	normal   = np.array(yn    + array(Z)).tolist() # Lista de altura normal a graficar
	critical = np.array(yc    + array(Z)).tolist() # Lista de altura critica a graficar
	walls    = np.array(muros + array(Z)).tolist() # Lista que representa la corona de los muros

	# Preparando información para graficado:
	plt.title('PERFIL DE FLUJO GRADUALMENTE VARIADO')
	Y = np.array(profile[3]).tolist()			   # Lista de profundidades de agua
	if control == 'DS':							   # Ajustando al sentido de flujo de izq. a derecha
		normal.reverse(), critical.reverse(), walls.reverse(), Y.reverse(), Z.reverse()
	# Etiquetas de ejes;
	if units == 'SI':
		und_x = 'metros'
		und_y = 'metros'
	else:
		und_x = 'pies'
		und_y = 'pies'
	plt.xlabel('Distancia planimetrica, ' + und_x)
	plt.ylabel('Elevacion, ' + und_y)
	plt.axis([profile[0][0], profile[0][-1], Z[-1] - 1., walls[0] + 2.]) 

	# Complementos al grafico:
	plt.text(profile[0][0], Z[-1], "Direccion flujo", ha="center", va="center", rotation=0, size=8,
			fontstyle = 'italic', bbox=dict(boxstyle="rarrow,pad=0.5", fc="white", ec="r", lw=1))
	# Graficando la solución:
	plt.plot(profile[0], Z, 'k', linewidth=4)     		# Línea del fondo del canal
	plt.plot(profile[0], normal, 'k--')					# Línea de altura normal
	plt.plot(profile[0], critical, 'k:')				# Línea de altura critica
	plt.plot(profile[0], Y, 'b', linewidth=2)	    	# Línea de superficie del agua
	plt.plot(profile[0], walls, 'k')			    	# Línea de la corona del muro lateral
	plt.legend(['Fondo del canal', 'Altura normal',
				'Altura critica' , 'Superficie del agua', 'Muros del canal'])
	return plt.show()
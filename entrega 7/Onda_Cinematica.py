# -*- coding: utf-8 -*-

import matplotlib.pyplot    as plt
import matplotlib.animation as animation
import numpy                as np
from numpy            import math, linspace, zeros, mean
from matplotlib.lines import Line2D
from Func_ynormal     import ynormal
    # Argumentos = (dimens, n, S, z, b, Q)

# INFORMACIÓN DE ENTRADA:
# Características del canal:
und= 'SB'                         # [Sistema británico] Sistema de unidades
b  = 100.                         # [pies] Ancho del fondo del canal
z  = 0.                           # Relación Horizontal/Vertical del talud lateral
n  = 0.045                        # [pie^3/s] Coeficiente rugosidad de Manning
S  = 0.001                        # [pie/pie] Pendiente longitudinal del canal
L  = 150000.                      # [pies] Longitud total del canal
# Condiciones antes de la perturbación:
Qn = 250.                         # [pie^3*/s] Flujo base
yn = ynormal(und,n,S,z,b,Qn)      # [pies] Altura del agua
An = yn*(b+yn*z)                  # [pies^2] Área mojada
Vn = Qn/An                        # [pies/s] Velocidad media
# Parametros de la simulación: 
tf = 1300.                        # [minutos] Duración total
ni = 1000                         # Cantidad de puntos en rejilla espacial
NC = 1.                           # Numero de Courant, Vonda/Vnumerica<1. (estable)
dx = L/(ni - 1.)                  # [pies] Diferencial constante del cambio espacial

# CALCULO POR DIFERENCIAS FINITAS:
# Inicializando "Vectores" Caudal(Q), altura(y), área(A), velocidad(V):
Q, y, A, V = [zeros(ni)], [zeros(ni)], [zeros(ni)], [zeros(ni)]  

# Asignando valores iniciales:
k = 0
t = [0.]                       # [min] Tiempo de inicio
for i in range(ni):            # Recorriendo todos los nodos en k=0
    Q[k][i] = Qn
    y[k][i] = yn
    A[k][i] = An
    V[k][i] = Vn

# Simulando modelo de onda cinemática (valores en k+1):
k  = k+1
dt = dx*NC/Vn                   # [segundos] Cambio temporal inicial
t.append(t[k-1] + dt)           # [segundos] Tiempo en k=1
while t[k] <= 60.*tf :
    # Inicializando campo para almacenar datos:
    Q.append(zeros(ni)), y.append(zeros(ni)), A.append(zeros(ni)), V.append(zeros(ni))
    
    # Calculando caudal en i=0
    angle = math.pi*t[k]/(60.*75.)
    if angle < 2.*math.pi:           # Condición causal de la perturbación
        # [pies^3*s-1] Caudal total durante el evento de perturbación
        Q[k][0] = Qn + 750.*(1. - math.cos(angle))/math.pi  
    else:                            # Final de la perturbación
        Q[k][0] = Qn                 # [pies^3/s] Flujo base
    
    # Calculando el esténcil:
    for i in range(ni):
        # Altura de agua en nodo i [pies]:
        y[k][i] = ynormal(und,n,S,z,b,Q[k][i])
        # Área mojada en nodo i [pies^2]:
        A[k][i] = y[k][i]*(b + z*y[k][i])
        # Velocidad media en nodo i [pies/s]:
        V[k][i] = Q[k][i]/A[k][i]
        # Caudal en nodo i+1 [pies^3/s]:
        if i < ni-1:
            Q[k][i+1] = Q[k][i] - (dx/dt)*(A[k][i] - A[k-1][i])                             
        
    # Calculando t en k+1 [minutos]:
    Vf = mean(V[k])                 # [pie/s] Velocidad promedio en el canal
    dt = dx*NC/Vf                   # [s] Diferencial de cambio temporal
    if t[k] + dt > 60.*tf and t[k] != 60.*tf:
        dt = 60.*tf - t[k]
    t.append(t[k] + dt)             # [segundos] tiempo en k+1
    k = k+1  
t.pop()                             # Desechando último tiempo excedente a tf


# PRESENTACIÓN DE LOS RESULTADOS:
# Altura y Caudal máximos:
nk = len(t)
Ymax, Qmax = zeros(nk), zeros(nk)
for k in range(nk):
    Ymax[k] = max(y[k])
    Qmax[k] = max(Q[k])
ymax = max(Ymax)              
qmax = max(Qmax)

# Ubicación de ymax:
Xmax = [None]
for k in range(nk):
    Xmax[k] = np.where(y[k]==Ymax[k])
    Xmax[k] = Xmax[k][0][0]*dx 
    Xmax.append([])
Xmax.pop()

# Velocidad de fotogramas (FPS = 1/delta):
Dt = zeros(nk-1)                    # Inicializando vector de cambio temporal
for k in range(nk-1):
    Dt[k] = t[k+1] - t[k]           # Cambio temporal dt entre cada k y k+1    
delta = mean(Dt)                    # Cambio temporal promedio de la simulación    

# Unidades de medida ejes:
if und == 'SI':
    dimen = 'metros'
    fluj  = '(metros cubicos)/s'
else:
    dimen = 'pies'
    fluj  = '(pies cubicos)/s'

# Imprimiendo:
class SubplotAnimation(animation.TimedAnimation):
    def __init__(self):
        fig = plt.figure(figsize=(14., 5.))
        ax1 = fig.add_subplot(2, 1, 1)
        ax2 = fig.add_subplot(2, 1, 2)
        # Impresión:
        self.time   = t
        self.x      = linspace(0., L, ni)
        self.y1     = []
        self.y2     = []
        self.t_tex1 = ax1.text(10.*dx, 1.50*ymax, '')
        self.t_tex2 = ax1.text(10.*dx, 1.750*ymax, '')
        self.t_tex3 = ax1.text(125.*dx, 1.750*ymax, '')
        self.t_tex4 = ax2.text(10.*dx, 1.075*qmax, '')
        # Curva1:
        ax1.set_title('Altura del agua')
        ax1.set_xlabel('Distancia, %s' %dimen)
        ax1.set_ylabel('Altura de agua, %s' %dimen)
        ax1.set_xlim(0., L)
        ax1.set_ylim(0., 2.*ymax)
        self.line1 =  Line2D([], [], lw=2, color='blue')
        ax1.add_line(self.line1)
        # Curva 2:
        ax2.set_title('Transito del caudal')
        ax2.set_xlabel('Distancia, %s' %dimen)
        ax2.set_ylabel('Caudal, %s' %fluj)
        ax2.set_xlim(0., L)
        ax2.set_ylim(0., 1.25*qmax)
        self.line2 = Line2D([], [], lw=2, color='black')
        ax2.add_line(self.line2)

        fig.tight_layout()     
        animation.TimedAnimation.__init__(self, fig, interval=delta/10., blit=True, repeat=False)

    def _draw_frame(self, i):
        ti = t[i]/60.
        Yi, Qi, Xi = Ymax[i], Qmax[i], Xmax[i]
        self.t_tex1.set_text('Tiempo: %.0f min' %ti)
        self.t_tex2.set_text('Altura maxima: %.2f' %Yi)
        self.t_tex3.set_text('>>> en la distancia: %.0f' %Xi)
        self.t_tex4.set_text('Caudal maximo: %.1f' %Qi)
        self.line1.set_data(self.x, y[i])
        self.line2.set_data(self.x, Q[i])
        self._drawn_artists = [self.line1, self.line2, self.t_tex1, self.t_tex2, self.t_tex3, self.t_tex4]

    def new_frame_seq(self):
        large = range(nk-1)
        
        return iter(large)

anim = SubplotAnimation()
plt.show()

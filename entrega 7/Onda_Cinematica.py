# -*- coding: utf-8 -*-
"""
Created on the space
"""
import numpy as np
import scipy as sp
from Func_ynormal   import ynormal
	# Argumentos = (units, n, S, z, b, Q)
from Func_ycritical import ycritical
	# Argumentos = (units, z, b, Q)

#SECCION 1
N=1000
L=150000
B=100
S=0.001
n=0.045
ss=0
Co=1.485
NC=1. #puede ser un numero menor a 1 tambien 
Tfin=600
Tfin=Tfin*600
g=32.3
# SECCION 2

dx=L/(N-1)
x=sp.zeros(N)
i=1
while i <= N-1:
    x[i]=(i)*dx
    i+=1

#SECCION 3

#Condiciones iniciales (k=1, t=0)
Q=sp.zeros((2*N,N))
y=sp.zeros((2*N,N))
A=sp.zeros((2*N,N))
V=sp.zeros((2*N,N))
Q[0,:]=250
y[0,:]=ynormal("SI",n,S,1,B,Q[0,0])
A[0,:]=B*y[0,0]
V[0,:]=Q[0,0]/A[0,0]

# SECCION 4

#  Loop  desde  t=0  a  t=  Tfin

t=0
k=0
tiempo=sp.zeros(2*N)
while t<Tfin:
    k=k+1
    dt=NC*dx/(sp.mean(V[0,:]))   #  dt=NC*dx/(g*mean(y(k,1:N)))^.5
    t=t+dt
    tiempo[k]=t
    tshow=t/60
#  Condiciones  de  borde
while t<Tfin:
    k=k+1
    dt=NC*dx/(sp.mean(V[k,:]))
    t=t+dt
    tiempo[k]=t
    tshow=t/60
    if t<=150*60:
		Q[k+1,0]=250+750/sp.pi*(1-sp.cos(sp.pi*t/(60*75)))  #	hidrograma  de  la  descarga  de  la  represa
    else:
		Q[k+1,0]=250  #  caudal  constante  luego  de  la  descarga  (volviendo  a  las  condiciones  originales)
    A[k+1,0],y[k+1,0]  =  NRalfa(Q[k+1,0],B,ss,n,Co,S)  	#NR  para  encontar  valor  de  A  e  Y  iterando
    V[k+1,0]  =  Q[k+1,0]/A[k+1,0]#  Moviendo  estencil  en  el  tiempo  k,  desde  nodo  1  al  nodo  N
    for i in Q:
		Q[k+1,i+1]=Q[k+1,i]-dt/dx*(A[k+1,i]-A[k,i])    #  ecuacion  de  continuidad
		A[k+1,i+1],y[k+1,i+1]  =  NRalfa(Q[k+1,i+1],B,ss,n,Co,S) #  ecuacion  de  momentum
		V[k+1,i+1]  =  Q[k+1,i+1]/A[k+1,i+1]
            
# Con esto faltaria lo de graficar todos los resultados en tiempo real
#  CAUDAL VS X(DISTANCIA RECORRIDA)    Y      ALTURA VS X (DISTANCIA RECORRIDA)



    
    

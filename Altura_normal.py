#ALTURA NORMAL DE CANAL TRAPEZOIDAL
#USNADO NEWTON-RHAPSON (NR)

Q   = 100.0         # [m^3*s^-1] Caudal que debe transportar la sección

#Parametros del modelo hidraulico
C_0 = 1.00          # Factor dimensional [SI=>1 - SB=>1.49]
n   = 0.013         # [s*m^(-1/3)] Coeficiente rugosidad de Manning
S   = 1/100         # [m/m]
#Parametros geometricos
z = 1.0            # Relación Horizontal/Vertical del talud
B = 5.0            # [m]Ancho inferior del canal

yn_i = 1.0         # Altura inicial para proceso interativo

#Funcion de solución
def D(y): 
    
    #Variables de calculo
    A   = yn*(B + z*yn)               # [m^2] Area mojada
    P   = B + 2*yn*(z**2+1)**0.5      # [m] Perimetro mojado
    d_A = B + 2*z*yn                  # [m] Derivada total de A respecto a yn
    d_P = 2*(z**2+1)**0.5             # Derivada total de P respecto a yn   
    k   = (Q*n/(C_0*S**0.5))**3       # [m^8] Constante del modelo hidraulico    
    #Funcion solucion y su derivada
    f   = A**5-k*P**2                # Funcion solución f(y)=0
    d_F = 5*A**4*d_A - 2*k*P*d_P     # Derivada total  f'(y)
    
    return f/d_F                     # Segundo termino de ecuacion de NR

# Proceso de aproximaciones sucesivas
yn = yn_i                   # Valor de inicio para yn
tol = D(yn)                 # Tolerancia tieracion 1

while tol > 1e-6:
    yn1 = yn - D(yn)        # Ecuacion de NR
    tol = abs(yn1-yn)       # Toleranacia del paso
    yn  = yn1               # Mutacion de yn

print("Altura normal yn    =",round(yn,3),"m")  # Imprimiendo la solución
# Verificacion de la solución
print("Caudal transportado =", round((C_0/n)*A*(A/P)**(2/3)*(S)**0.5,3),"m^3/s")
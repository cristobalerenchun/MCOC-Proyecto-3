import scipy as sp
def geom(y,B,ss):
	A = B*y + ss*(y**2)
	dA = B + 2*y*ss
	P = B + 2*y*sp.sqrt((ss**2)+1)
	dP = 2*sp.sqrt((ss**2)+1)
	R = A/P
	dR = (2*(y**2)*ss*sp.sqrt((ss)**2+1)+2*B*y*ss+(B**2))/((2*y*sp.sqrt(ss*2+1)+B)**2)
#	dF = (5/3)*(A**(4/3))*(P**(-2/3))*dA-(2/3)*(A**(5/3))*(P**(-5/3))*dP
	d = { 'A' : A , 'dA' : dA , 'P':P, 'dP':dp,'R':R,'dR':dR}
	return d

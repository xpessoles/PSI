import numpy as np

t1,t2,t3,t4,t5,t6=15,30,4*60,10*60,15,5

ti1=2*t1+2*t2+2*t3+t4
print("ti1="+str(ti1))

ti2=2*t1+2*t2+(6*3*2)*t5+(5*2+1)*t6
print("ti2="+str(ti2))

diffti=2*t3+t4-(6*3*2)*t5-(5*2+1)*t6

print("$\Delta t_i$="+str(diffti))


Vc=400/60
R=0.47
e=15*1E-3
b=0.2*1E-3/np.pi
RM=0.5
Rm=0.4
k=0.1
Rre=0.175

#ED dwm=-(R*Vc**2*b*(RM**2-Rm**2))/(2*RM*Rm*k*Rre*np.sqrt(e**2+(RM-Rm)**2))

#XP 
dwm=-(R*Vc**2*b*(RM**2-Rm**2))/(2*(RM**2)*(Rm**2)*k*Rre*np.sqrt(e**2+(RM-Rm)**2))
wmmax=R*Vc/(k*Rre*Rm)

#Partie 3
K=28*1E6
m2=788
lamb=14854
Ks=1/K
w0=np.sqrt(K/m2)
xi=lamb/(2*np.sqrt(K*m2))
m1=5522
A=1/m1
w1=np.sqrt(K/m2)
xi1=lamb/(2*w1*m2)
w2=np.sqrt((K*(m1+m2))/(m1*m2))
xi2=0.5*lamb*np.sqrt((m1+m2)/(m1*m2*K))

wr = w0*np.sqrt(1-2*xi**2)

b=5*1e-2/(np.pi)
bl=b*10**(45/20)
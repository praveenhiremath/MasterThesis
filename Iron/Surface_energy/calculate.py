# Author: Praveenkumar Hiremath, TU Bergakademie Freiberg, Sachsen, Germany (Postleitzahl: 09599). May, 2016. 

import numpy as np
from pylab import *
import io
import os
#(hkl) can be (111),(100),(110)
s_ene=[]
#N is number of calculations with different number of layers.
for i in range(1,N,1):
#surfacehkl.dat contains .......
  folder=str(i)+'/surfacehkl.dat'
  with open(folder,'r') as file1:
    lines=file1.readlines()
    temp=lines[1]
    s_ene.append(temp)
  with open('energy_trend.dat','a') as file2:
    file2.writelines(temp)  
print s_ene
layers=np.loadtxt('layers.dat')
ene=np.loadtxt('energy_trend.dat')
###Finding y-intercept in y=mx+c
slope=(ene[N-1]-ene[0])/(layers[N-1]-layers[0])
temp1=slope*(layers[N-1]+layers[0])
temp2=ene[N-1]+ene[0]-temp1
c=temp2/2
area=2*lx*ly
sur_ene=c*16.021/area
print "surface energy is:",sur_ene
plot(layers,ene,'r-o')
ax = gca()
text(0.1,0.8,'Surface energy E(hkl)=E-intercept/(2*lx*ly)' ,
transform = ax.transAxes)
text(0.4,0.7,'Surface energy E(hkl)=%1.2f J/m^2'% sur_ene,
transform = ax.transAxes)
xlabel('Number of layers ',{'fontsize': 15})
ylabel('Total energy (eV)',{'fontsize': 15})
savefig('hkl_tot_ene_vs_layers.png')
show()    

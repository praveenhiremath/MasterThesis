

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

xdata = [ -0.006, -0.004, -0.002, 0.0, 0.002, 0.004, 0.006]
ydata_iso = [0.10786, 0.04909, 0.01377, 0.00000, 0.00807, 0.03643, 0.08437]
ydata_tetra = [0.06567, 0.02946, 0.00754, 0.00000, 0.00765, 0.02993, 0.06746]
ydata = np.add(ydata_iso,ydata_tetra)

ydata_tri = [0.01093, 0.00536, 0.00195, 0.00000, 0.00108, 0.00330, 0.00732]

combox = np.append(xdata,xdata)
comboy = np.append(ydata_iso,ydata_tetra)

if len(xdata) != len(ydata_iso):
    raise(Exception('Unequal xdata and ydata_iso data length'))
if len(xdata) != len(ydata_tetra):
    raise(Exception('Unequal xdata and ydata_tetra data length'))




#Recast xdata and ydata into numpy arrays so we can use their handy features
xdata = np.asarray(xdata)
ydata = np.asarray(ydata)
plt.plot(xdata, ydata, 'o')


# Define the Iso function
def Iso(eta, C11, C12):
    dene_dvol_iso = (1.5)*(C11+(2*C12))*pow(eta,2)   #(eta**2)
    return dene_dvol_iso

# Define the Tetra function
def Tetra(eta, C11, C12):
    dene_dvol_tetra = (3.0)*(C11-(1*C12))*pow(eta,2)   #(eta**2)
    return dene_dvol_tetra

def Iso_Tetra(combo_eta,C11,C12):
    # single data reference passed in, extract separate data
    xdata1 = combo_eta[:len(xdata)] # first data
    xdata2 = combo_eta[len(xdata):] # second data

    iso_result = Iso(xdata1, C11, C12)
    tetra_result = Tetra(xdata2, C11, C12)

    return np.append(iso_result, tetra_result)

#parameters, covariance = curve_fit(Iso, xdata, ydata)

parameters, covariance = curve_fit(Iso_Tetra, combox, comboy)
print (parameters)

print (covariance)

fit_A = parameters[0]
fit_B = parameters[1]

# Define the Tri function
def Tri(eta, C44):
    dene_dvol = (0.5)*(C44)*pow(eta,2)   #(eta**2)
    return dene_dvol
parameters2, covariance2 = curve_fit(Tri, xdata, ydata_tri)

print (parameters2)

print (covariance2)

fit_C = parameters2[0]

print("C11 (in GPa): ",fit_A*.1602176621)
print("C12 (in GPa): ",fit_B*.1602176621)
print("C44 (in GPa): ",fit_C*.1602176621)


fit_y = Iso_Tetra(xdata, fit_A, fit_B)
plt.plot(xdata, ydata, 'o', label='data')
plt.plot(xdata, fit_y, '-', label='fit')
plt.legend()
'''
SE = np.sqrt(np.diag(covariance))
SE_A = SE[0]
SE_B = SE[1]

print(F'The value of A is {fit_A:.5f} with standard error of {SE_A:.5f}.')
print(F'The value of B is {fit_B:.5f} with standard error of {SE_B:.5f}.')
'''
plt.show()



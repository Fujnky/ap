import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
import scipy.constants as const
import uncertainties.unumpy as unp
import tools
B = 1.059

def auswerten(I, U_H, name):
    #print(I, U_H, name)
    slope, intercept, std_dev, r, p = linregress(I, U_H)
    i = np.linspace(0,10)
    plt.plot(i, 1e6*i*slope+intercept, label='Lineare Regression')
    plt.plot(I, U_H*1e6, 'rx', label='Messdaten')
    plt.xlabel(r"$I_q/\si{A}$")
    plt.ylabel(r"$U/\si{µV}$")
    plt.legend(loc='best')
    plt.tight_layout()
    plt.savefig('build/{}.pdf'.format(name))
    plt.clf()
    return slope

data2 = np.genfromtxt('daten/b.txt', delimiter=';', unpack=True)
I_, Zn, Cu = data2
Zn *= 1e-6
Cu *= 1e-6

Vm = (7.11e-6, 9.16e-6)
rho = np.array((1.721e-2, 0.06))*1e-6
L = (0.028, 0.044)
b = np.array((0.025, 0.026))






data = np.genfromtxt('daten/a.txt', dtype=object, unpack=True)
I__ = data.astype(float)[0]
U = 1e-3*data.astype(float)[1:]
R = unp.uarray((U[:,1:]/I__[1:]).mean(axis=1), (U[:,1:]/I__[1:]).std(axis=1))




sl = np.array((auswerten(I_, Cu, 'b2'), auswerten(I_[:-4], Zn[:-4], 'b')))
#d = np.array((18e-6, 1/(sl[1] / (6.4e-11 * B)) ))
d = rho * L / (R * b)
print(R, d)

R_H = sl / B * d
n = 1 / (sl * d / B * const.e)

V = (2.8e-2*2.5e-2, 4.4e-2*2.6e-2)*d
z = n * Vm / const.N_A
#print(R_H, d, n, z)


tau = 1/(R / 2 * const.e**2 / const.m_e * n / (2.8e-2, 4.4e-2) * d * (2.5e-2, 2.6e-2))
v_d = 1e9 / n / const.e
µ = const.e * tau / const.m_e
E_F = const.h**2 / (2* const.m_e) * ((3/8/np.pi * n)**2)**(1/3)
v = unp.sqrt(2*E_F/const.m_e)
l = tau * unp.sqrt(2*E_F/const.m_e)


tools.table((sl, R_H*1e11, d*1e6, n/1e27), (r"m/\ohm", r"R_H/(10^{-11} \cubic\meter\per\coulomb)", r"d/µm", r"n/\per\cubic\nano\meter"), "build/erg.tex", "Ergebnisse der Auswertung, erster Teil.", "tab:erg", round_figures=(3,3,3,3), interrows={0:"Kupfer", 1:"Zink"})
tools.table((z, R*1e3, tau*1e15), ("z", "R/\milli\ohm", r"\bar\tau/fs"), "build/erg3.tex", "Ergebnisse der Auswertung, dritter Teil.", "tab:erg3", round_figures=(3,3,3), interrows={0:"Kupfer", 1:"Zink"})
tools.table((v_d*1e3, 1e4*  µ, v/1e6, l*1e9), (r"\bar v_d/(\milli\meter\per\second)", r"\mu/(\centi\meter\squared\per\volt\per\second)", "v/(\mega\meter\per\second)", r"\bar l/nm"), "build/erg2.tex", "Ergebnisse der Auswertung, zweiter Teil.", "tab:erg2", round_figures=(3,3,3,3), interrows={0:"Kupfer", 1:"Zink"})
tools.table(data, ('I/A', r'U_\text{Zn}/mV', r'U_\text{Cu}/mV'), 'build/datena.tex', 'Messdaten, Widerstandsmessreihe.', 'datena',  split=2)

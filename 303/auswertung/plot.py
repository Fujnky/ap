
import matplotlib.pyplot as plt
import numpy as np
x_syn = np.linspace (0, 360, 1000)
x,y =np.genfromtxt('auswertung/ohnerauschen.txt',unpack=True)
plt.plot(x,y,'rx',label="Messwerte")
plt.xlabel(r'$\phi /\mathrm{°}$')
plt.ylabel(r'$U \ /\ \mathrm{V}$')
plt.xlim(0,360)

plt.plot (x_syn,33*np.cos(np.pi*x_syn/180),'b-',label="Ausgangsspannung")
plt.legend(loc='best')
plt.savefig('build/plot.pdf')

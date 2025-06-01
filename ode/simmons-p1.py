import numpy as np
import matplotlib.pyplot as plt

from scipy.optimize import fsolve

T = np.linspace(start=0.1, stop=2, num=500)
def f(t):
    return 2 * np.log((t + 4)/t) - 3 * np.log((t + 2)/t)

F = [f(t) for t in T]

plt.plot(T, F, label=r"$f(t)$")
plt.hlines(y = 0, xmin=0, xmax=2, linestyles="dashed")
plt.title(r"$f(t) = 2\ln((t+4)/t) - 3\ln((t+2)/t)$")
plt.xlabel(r"$t$")
plt.ylabel(r"$f(t)$")
plt.savefig("simmons-p1.png")

roots = fsolve(func=f, x0=[1])
print(roots)

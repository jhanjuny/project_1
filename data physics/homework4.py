import numpy as np, matplotlib.pyplot as plt
v0 = 1.0; x0 = 0.0; T = 1.0;
dt = 0.01; maxt = 1000.0
t_arr = []; x_arr = []; v_arr = []; v2_arr = []
x, v = x0, v0
a = np.sqrt(6*T/dt)
for t in np.arange(0, maxt, dt):
    t_arr.append(t); x_arr.append(x); v_arr.append(v);
    v2_arr.append(v*v)
    eta = a*(2*np.random.rand() - 1.0)
    x += dt*v
    v += dt*(-v + eta)

plt.plot(t_arr, x_arr)
plt.xlabel("t")
plt.ylabel("x")
plt.show()
plt.plot(t_arr, v_arr)
plt.xlabel("t")
plt.ylabel("v")
plt.show()
print( np.average(v2_arr[len(v2_arr)//2:-1]))


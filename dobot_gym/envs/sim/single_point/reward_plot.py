import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits import mplot3d

s0 = np.array([0, 0])
g = np.array([1, 0])
midpoint = (s0 + g) / 2

fig = plt.figure()
ax = plt.axes(projection='3d')

num_points = 200
num_contours = 100
x = np.linspace(midpoint[0] - 1, midpoint[0] + 1, num_points)
y = np.linspace(midpoint[1] - 1, midpoint[1] + 1, num_points)

scale_factor_s0 = 1
scale_factor_g = 1

X, Y = np.meshgrid(x, y)

Z = scale_factor_s0 * ((X - s0[0]) ** 2 + (Y - s0[1]) ** 2) + scale_factor_g * ((X - g[0]) ** 2 + (Y - g[1]) ** 2)

# Contours are elliptical. Scale factor only shifts the center of ellipses

ax.contour3D(X, Y, Z, num_contours)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('Reward')

plt.show()
# reward_function = np.abs(s0 - s) ** 2 + np.abs(s - g) ** 2 where s = [x,y]

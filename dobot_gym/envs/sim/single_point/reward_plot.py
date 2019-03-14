import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits import mplot3d

s0 = np.array([0, 0])
g = np.array([1, 0])

fig = plt.figure()
ax = plt.axes(projection='3d')

num_points = 300
num_contours = 100
x = np.linspace(-1, 2, num_points)
y = np.linspace(-1, 1, num_points)

scale_factor_s0 = 1
scale_factor_g = 1

X, Y = np.meshgrid(x, y)

Z = scale_factor_s0 * (X ** 2 + Y ** 2) + scale_factor_g * ((X - 1) ** 2 + Y ** 2)

# Contours are elliptical. Scale factor only shifts the center of ellipses

ax.contour3D(X, Y, Z, num_contours)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

plt.show()
# reward_function = np.abs(s0 - s) ** 2 + np.abs(s - g) ** 2 where s = [x,y]


import matplotlib.pyplot as plt
import numpy as np

theta = np.arange(0,2*np.pi,np.pi/180)
print(len(theta))
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(0, 0, 0, marker='.')
ax.set_ylabel('y')
ax.set_xlabel('x')
ax.set_zlabel('z')
ax.set_zlim((0,1))
plt.grid(True)

for phi in np.arange(0,np.pi/2,np.pi/45):
    x = np.cos(theta)* np.cos(phi)
    y = np.sin(theta)
    # #Nota, como el lidar está en 90° se le inverte la función sin(phi)
    z = np.cos(theta)* np.sin(phi)
    ax.scatter(x, y, z, marker='.')

plt.show()
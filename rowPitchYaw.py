import matplotlib.pyplot as plt
import numpy as np

angles = []
# row, prowtch, yaw
for row in range(36):
    for pitch in range(36):
        for yaw in range(36):
            row *= 10; pitch *= 10; yaw *= 10
            angles.append([row,pitch,yaw])

print angles[0]
plt.plot(angles[0,:],angles[1,:])
plt.show()

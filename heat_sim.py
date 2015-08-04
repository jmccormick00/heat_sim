__author__ = 'jr'
import numpy as np
import matplotlib.pyplot as plt

def check(res):
    tol=10e-4
    test = res<tol
    return ~test.any()  # return true if any value in the matrix is true


#--------------------------------------------------------------------------
# Pan width and hight
panHeight = 0.3075  # m
panWidth = 0.3075  # m
eyeWidth = 0.2  # m
eyeHeight = 0.2  # m
delta = 0.0025
#--------------------------------------------------------------------------

#--------------------------------------------------------------------------
# Thickness of the bottom layer
d1 = 0.0060  # m

# Thickness of the second layer on top
d2 = 0.0001  # m
#--------------------------------------------------------------------------

#--------------------------------------------------------------------------
# Thermal Properties
k = 236  # W/mK
q = 61000  # W/m^2
h = 7.9  # W/Km^2
Te = 300  # K Temperature of the ambient air
k2 = 0.45  # second layer thermal conductivity (W/mK)
alpha = 97.1*(10e-6)  # m^2/s
density = 2702  # kg/m^3
c = 903  # j/(kgK)

# Compute constants
# These are pulled out of the grid equations to save a few multiplications
# each iteration
U = 1/(d2/k2 + 1/h)
Xi = 2*k*d1 + U*delta*delta
Yi = 3*k*d1 + U*delta*delta
Zi = 4*k*d1 + U*delta*delta
D = Te*U*delta*delta

#--------------------------------------------------------------------------
ROW = int(panHeight/delta) # +1
COLUMN = int(panWidth/delta) # +1

# Solve for where the Eye is in the Grid
c1 = panHeight/2 - eyeHeight/2
c2 = panWidth/2 - eyeWidth/2
Ieye = c1/delta
Jeye = c2/delta
Ieye = int(Ieye)
Jeye = int(Jeye)
Eye = [Ieye, Jeye, Ieye + eyeHeight/delta, Jeye + eyeWidth/delta]
#--------------------------------------------------------------------------

# Set the grid to a initial temp 450 K
grid = np.empty((ROW, COLUMN))
grid.fill(450.0)

while True:
    oldGrid = grid.copy()
    for i in xrange(ROW):
        for j in xrange(COLUMN):
            # Calculate the corners
            if i == 0 and j == 0:  # Top left
                grid[i, j] = (k*d1*(grid[i, j+1] + grid[i+1, j]) + D) / Xi
            elif i == 0 and j == (COLUMN-1):  # Top right
                grid[i, j] = (k*d1*(grid[i, j-1] + grid[i+1, j]) + D) / Xi
            elif i == (ROW-1) and j == 0:  # Bottom left
                grid[i, j] = (k*d1*(grid[i-1, j] + grid[i, j+1]) + D) / Xi
            elif i == (ROW-1) and j == (COLUMN-1):  # Bottom Right
                grid[i, j] = (k*d1*(grid[i-1, j] + grid[i, j-1]) + D) / Xi

            # Calculate the sides
            elif i == 0 and j > 0 and j < (COLUMN-1):  # Top
                grid[i, j] = (k*d1*(grid[i, j+1] + grid[i+1, j] + grid[i, j-1]) + D) / Yi
            elif i == (ROW-1) and j > 0 and j < (COLUMN-1):  # Bottom
                grid[i, j] = (k*d1*(grid[i, j+1] + grid[i-1, j] + grid[i, j-1]) + D) / Yi
            elif j == 0 and i > 0 and i < (ROW-1):  # Left
                grid[i, j] = (k*d1*(grid[i-1, j] + grid[i, j+1] + grid[i+1, j]) + D) / Yi
            elif j == (COLUMN-1) and i > 0 and i < (ROW-1):  # Right
                grid[i, j] = (k*d1*(grid[i-1, j] + grid[i, j-1] + grid[i+1, j]) + D) / Yi

            # Over the eye
            elif i >= Eye[0] and i <= Eye[2] and j >= Eye[1] and j <= Eye[3]:
                grid[i, j] = (k*d1*(grid[i-1, j] + grid[i, j-1] + grid[i+1, j] + grid[i, j+1]) + q*delta*delta + D) / Zi

            # outside the eye
            else:
                grid[i, j] = (k*d1*(grid[i-1, j] + grid[i, j-1] + grid[i+1, j] + grid[i, j+1]) + D) / Zi

    if check(np.abs(grid-oldGrid)):
        break

# plot the contour plot of the grid
CS = plt.contour(grid)
plt.show()
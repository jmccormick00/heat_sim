__author__ = 'jr'
import numpy as np


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
k1 = 236  # W/mK
q = 61000  # W/m^2
h = 7.9  # W/Km^2
Te = 300  # K Temperature of the ambient air
k2 = 0.45  # second layer thermal conductivity (W/mK)
alpha = 97.1*np.power(10, -6)  # m^2/s
density = 2702  # kg/m^3
c = 903  # j/(kgK)

# Compute constants
U = 1/(d2/k2 + 1/h)
Xi = 2*k1*d1 + U*delta*delta
Yi = 3*k1*d1 + U*delta*delta
D = Te*U*delta*delta

#--------------------------------------------------------------------------
ROW = panHeight/delta + 1
COLUMN = panWidth/delta + 1

# Solve the for where the Eye is in the Grid
c1 = panHeight/2 - eyeHeight/2
c2 = panWidth/2 - eyeWidth/2
Ieye = c1/delta + 0.5
Jeye = c2/delta + 0.5
Ieye = int(Ieye)
Jeye = int(Jeye)
Eye = [Ieye, Jeye, Ieye + eyeHeight/delta, Jeye + eyeWidth/delta]
#--------------------------------------------------------------------------

# Set the grid to a initial temp 450 K
grid = np.empty((10, 10))
grid.fill(450.0)

while True:
    oldGrid = grid.copy()
    # Calculate the corners

    # Calculate the sides

    # Over the eye

    # outside the eye

    if check(np.abs(grid-oldGrid)):
        break










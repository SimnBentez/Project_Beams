import numpy as np
import pylab as plt
from components.Functions import *
from components.Inputs import *
from components.Design import *
from components.Auxiliary_functions import *
from components.Draw_CAD import *

# First the input data is requested

n = numbers_of_elements()
lengths = def_lengths(n)
conditions = nodes_beam(restrictions_beam(n))
loads_applied = kind_loads(n)
loads_fixed = forces_vector(loads_applied, lengths)

# Now the displacements are calculated using the stiffness 
# method. Note that a constant E,I is assumed

k = function_matrix_global(n, lengths, 1, 1)
kr = k[np.ix_(rows_and_columns(conditions), 
        rows_and_columns(conditions))]
ffr = loads_fixed[np.ix_(rows_and_columns(conditions
                ))] # This is the reduced fixed force vector
kr_inv = np.linalg.inv(kr)
displacements_reduced = np.dot(kr_inv, -ffr)
displacements = displacement(displacements_reduced, conditions)

# Now that the displacements have been obtained, we move on to 
# the calculation of the forces, to later obtain the displacement 
# fields and thus obtain the corresponding maximum moments, as well 
# as the moments where the steel becomes zero

forces_beam = np.dot(k, displacements) + loads_fixed
plot_shear_force(forces_beam, loads_applied, n, lengths)
plot_bending_moment(forces_beam, loads_applied, n, lengths)

ans = 0

while ans < 1:
    ans = str(input('¿Desea diseñar la sección? (Sí: Y  No: N) '))
    if ans == 'Y' or ans == 'y':
        ans = 1
    elif ans == 'N' or ans == 'n':
        break
    else:
        print('No estás digitando correctamente las opciones. Inténtalo nuevamente.')
        ans = 0


if ans == 1:

    ans = 0

    while ans < 1:
        try:
            ans = int(input('Ingrese la resistencia a la compresión del concreto (kg/cm²): '))
            fcon = ans
            ans = 1
        except:
            ans = print('¡Algo salió mal!')

    ans = 0

    while ans < 1:
        try:
            ans = int(input('Ingrese la base de la sección (cm): '))
            b = ans
            ans = 1
        except:
            print('¡Algo salió mal!')
            ans = 0

    ans = 0

    while ans < 1:
        try:
            ans = int(input('Ingrese la altura de la sección (cm): '))
            h = ans
            ans = 1
        except:
            print('¡Algo salió mal!')
            ans = 0

    ans = 0

    while ans < 1:
        try:
            ans = int(input('Ingrese la distancia del recubrimiento (cm): '))
            r = ans
            ans = 1
        except:
            print('¡Algo salió mal!') 
            ans = 0

d1, d2 = design_moment_beam(forces_beam, loads_applied, n, lengths, h, b, r, fcon)
d3, d4 = design_shear_beam(forces_beam, loads_applied, n, lengths, h, b, r, fcon)

Excel_data(d1, d2, d3, d4)

lT = sum(lengths) # total length

lT = lT * 100 # pass m to cm

Initialize_Draw(10, 40, lT) 
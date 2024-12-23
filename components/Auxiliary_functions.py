import numpy as np
def re_array_bending(x_M, M):
    """
    Definition
    -------------------------------------
    This function is used to accommodate moments if necessary, 
    so that repeated values are discarded

    Return
    -------------------------------------
    This is how the array returns reorganized

    Args:
    x_M: array with values in x
    M: array with values from maximus moments bending
    """
    j = 0 # find the repeated values
    fill_x, fill_M = [], []

    for i in range(len(M)):
        if i != len(M) - 1 and x_M[i+1] == x_M[i]:
            j += 1
        elif j == 1:
            j -=1
            fill_x.append(x_M[i])
            mf = max([M[i-1], M[i]])
            fill_M.append(mf)
        else:
            fill_x.append(x_M[i])
            fill_M.append(M[i])

    return fill_x, fill_M

def steel_condition(M):
    """
    Definition
    ----------------------------------
    This function is performed to obtain the location of the reinforcement 
    along the beam

    Return
    --------------------------------
    List of condition about location of the reinforcement in concrete beam

    Args:
    M: array with moments bending
    """

    conditions = []

    for i in range(len(M)):
        if M[i] < -8e-2:
            conditions.append('Superior')
        elif M[i] > 8e-2:
            conditions.append('Inferior')
        else:
            conditions.append('N/A')

    return conditions

def Select_bar_steel(As):
    """
    Definition
    --------------------------------
    This function was made so that you can select the area (number of rods) 
    that the rib should have. It is important to note that the smallest error is selected. 
    Also remember that this was designed for a very conservative case

    Return
    ------------------------------
    list of areas, list of name and list of error (%) [Yeah, it's a description]

    Args:
    As: array with areas
    """

    lis1, lis2, lis3 = [], [], []

    d = [3/8, 4/8, 5/8, 6/8] # diameters of road

    d = np.array(d) * 2.54  # array!!

    A = (np.pi / 4) * d ** 2 # areas of road

    road = np.array(['N3', 'N4', 'N5', 'N6'])

    # An IMPORTANT clarification is made here, remember that this program is designed 
    # for elements subjected only to vertical loads, which is why only N6 rods are reached.

    for i in range(len(As)):
        if As[i] != 0 and isinstance(As[i], (int, float)):
            con = 0
            j = 1
            Ap = As[i]
            while con < 1:
                condition = j * A > Ap / 1.12

                Ac = j * A[condition]

                if Ac.size == 0:
                    j += 1
                else:
                    con +=1

            # Here, what is done is to obtain the minimum possible difference 
            # to take the most optimal area. Also, at the end (as can be seen in the return) 
            # two lists are placed containing the selected areas and the type of rod for each area.

            ultimate = Ac - Ap
            road_ultimate = road[condition] # Idk

            As0 = round(float(Ac[np.where(ultimate == np.min(ultimate))]), 2)
            name = f"{j} {road_ultimate[np.where(ultimate == np.min(ultimate))][0]}"
            error = ((As0 - Ap) / Ap) * 100 # in porcentage
            error = round(error, 2)

            lis1.append(As0), lis2.append(name), lis3.append(error)
        else:
            lis1.append(0), lis2.append('N/A'), lis3.append(0)

    return lis1, lis2, lis3
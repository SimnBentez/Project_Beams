# In this Python file there are some functions that are used in 
# the main file (main)

import numpy as np
import pylab as plt

def function_stiffness_matrix(E, I, l):
    """
    Definition
    -------------------------
    This function is used to obtain the local stiffness matrices 
    of the beam. To do this, the concept seen in Structural 
    Analysis must be clear. 

    Return
    ------------------------------------
    This function return matrix stiffness to beam

    Args:
    E: Elasticity modulus of the section
    I: Second moment of area of ​​the section (inertia)
    l: Length of the section
    """
    C1 = 12*(E*I)*(1/l)**3 
    C2 = 6*(E*I)*(1/l)**2
    C3 = 4*(E*I)*(1/l)
    C4 = 2*(E*I)*(1/l)
    M = np.array([[C1, C2, -C1, C2], [C2, C3, -C2, C4],
                [-C1, -C2, C1, -C2], [C2, C4, -C2, C3]])
    return M

def function_matrix_global(number_of_elements, l, E, I):
    """
    Definition
    -----------------------------
    This function is performed to obtain the global matrix of 
    the problem. Receiving the number of sections that the beam 
    has and the array of the lengths

    Return
    -----------------------------
    This matrix is ​​responsible for assembling the global matrix of the problem. 
    Keep in mind that this is simple since the program does not receive joints and 
    it is intended to take them into account in future updates

    Args:
    number_of_elements: The number of elements your beam has
    l: lengths of problem
    E: Young's modulus
    I: Second moment of area
    """
    n = 2*(number_of_elements+1) # Gets number of rows and columns
    lengths = len(l)
    matrix_global = np.zeros((n, n)) # Get matrix stiffness global
    for i in range(0, lengths):
        start = 2*i # This variable is to know where to start adding
        end = 2*(i+2) # This variable is to know where to end adding
        matrix_global[start:end, start:end] += function_stiffness_matrix(E, 
                                                I, l[i])
    # Once you finish adding each local matrix, 
    # this returns the global matrix of the problem
    return matrix_global

def forces_vector(loads_matrix_conditions, lengths_beam):
    """
    Definition
    ---------------------------
    This function is performed to calculate 
    the embedding force vector of the problem (beam)

    For this, all the sections of the beam are first 
    loaded, whether they are subjected to a load or not, 
    and then each case is discretized

    Return
    --------------------------
    This function is responsible for calculating the embedding forces 
    of each problem, in order to apply the stiffness method

    Args:
    loads_matrix_condition: loads condition
    lengths_beam: it's lengths of beam
    """
    total = len(loads_matrix_conditions)
    elements = 2*(total+1)
    loads_matrix = np.zeros((elements, 1), dtype=float)
    for i in range(0, total):
        # For this we move on to the embedded responses 
        # of the most particular and unique cases covered 
        # by the program
        l = lengths_beam[i]
        if loads_matrix_conditions[i][0] == 1:
            p = loads_matrix_conditions[i][1]
            a = loads_matrix_conditions[i][2]
            b = l-a
            R1 = p*(b/l)**2 * (2*(a/l)+1)
            M1 = p*a*(b/l)**2
            R2 = p*(a/l)**2 * (2*(b/l)+1)
            M2 = -p*b*(a/l)**2
        elif loads_matrix_conditions[i][0] == 2:
            q = loads_matrix_conditions[i][1]
            R1 = (q/2)*(l)
            M1 = (q/12)*(l**2)
            R2 = R1
            M2 = -M1
        elif loads_matrix_conditions[i][0] == 3:
            q1 = loads_matrix_conditions[i][1]
            q2 = loads_matrix_conditions[i][2]
            w = q2-q1
            R1 = q1*(l/2) + (3/20)*w*l
            M1 = (q1/12)*l**2 + (w/30)*l**2
            R2 = q1*l/2 + (7/20)*w*l
            M2 = -((q1/12)*l**2 + (w/20)*l**2)
        else:
            R1 = 0
            M1 = 0
            R2 = 0
            M2 = 0
        # Here a matrix is ​​defined that allows the sum 
        # of the global force matrix (vector)
        loads_fixed = [R1, M1, R2, M2]
        loads_matrix[2*i:2*i+4,0] += np.array(loads_fixed)
    return loads_matrix

def rows_and_columns(conditions):
    """
    Definition
    ----------------------
    This function has the objective of generating the 
    number of rows and columns that the submatrix where 
    the reduced stiffness matrix is should generate

    Return
    ---------------------
    Return displacement

    Args:
    conditions: condition
    """
    row = []
    for i in range(0, len(conditions)):
        if conditions[i] == 1:
            row.append(i)
    return row

def displacement(displacement_no_fixed, condition):
    """
    Definition
    -------------------
    This function is defined to obtain the 
    global displacements of the beam

    Return
    ------------------
    This function is responsible for obtaining the displacements corresponding 
    to the possible degrees of freedom in the beam

    Args:
    displacement_no_fixed: displacement freedom
    condition: if it's free or fixed (1 or 0)
    """
    j = 0
    displacement_matrix = []
    for i in range(0, len(condition)):
        if condition[i] == 1:
            displacement_matrix.append(
                [displacement_no_fixed[j][0]])
            j += 1
        else:
            displacement_matrix.append([0])
    return np.array(displacement_matrix)

def plot_shear_force(forces_beam, loads_applied, 
                     elements, lenghts):
    """
    Definition
    --------------------
    This function is defined to obtain the
    plot shear force of the beam

    Args:
    forces_beam: List of forces at each element
    loads_applied: List of loads applied on each element
    elements: Number of elements in the beam
    lengths: List of lengths of each element
    """
    for i in range(0, elements):
        if i == 0:
            l1 = 0
            Vo = forces_beam[2*i][0]
        else:
            l1 = lenghts[i-1]+l1
            Vo = Vo+forces_beam[2*i][0]
        l2 = lenghts[i]+l1
        """
        Depending on the type of 
        load applied to beam, the field graph 
        is different, therefore a conditional 
        is used
        """
        if loads_applied[i][0] == 1:
            a = loads_applied[i][2]+l1
            p = loads_applied[i][1]
            x1 = np.linspace(l1, a, 
                        1000)
            x2 = np.linspace(a, l2, 
                        1000)
            y1 = Vo+0*x1
            y2 = Vo-p+0*x2
            plt.plot(x1, y1, 
                color='black', linestyle='--')
            plt.plot(x2, y2,
                color='black', linestyle='--')
            plt.fill_between(x1[y1<0], y1[y1<0],
                color ='red', alpha=0.35)
            plt.fill_between(x1[y1>0], y1[y1>0],
                color='yellow', alpha=0.35)
            plt.fill_between(x2[y2<0], y2[y2<0],
                color ='red', alpha=0.35)
            plt.fill_between(x2[y2>0], y2[y2>0],
                color='yellow', alpha=0.35)
            Vo = Vo-p
        elif loads_applied[i][0] == 2:
            w = loads_applied[i][1]
            x = np.linspace(l1, l2, 
                    1000)
            y = Vo-w*(x-l1)
            plt.plot(x, y, 
                color='black', linestyle='--')
            plt.fill_between(x[y<0], y[y<0],
                color='red', alpha=0.35)
            plt.fill_between(x[y>0], y[y>0],
                color='yellow', alpha=0.35)
            Vo = Vo-w*(l2-l1)
        elif loads_applied[i][0] == 3:
            q1 = loads_applied[i][1]
            q2 = loads_applied[i][2]
            t = q2-q1
            dl = l2-l1
            m = (t/dl)*(1/2)
            x = np.linspace(l1, l2, 
                    1000)
            y = Vo-q1*(x-l1)-m*(x-l1)**2
            plt.plot(x, y,
                color='black', linestyle='--')
            plt.fill_between(x[y<0], y[y<0],
                color='red', alpha=0.35)
            plt.fill_between(x[y>0], y[y>0],
                color='yellow', alpha=0.35)
            Vo = Vo-q1*(l2-l1)-m*(l2-l1)**2
        else:
            x = np.linspace(l1, l2,
                    1000)
            y = Vo+0*x
            plt.plot(x, y,
                color='black', linestyle='--')
            plt.fill_between(x[y<0], y[y<0],
                color='red', alpha=0.35)
            plt.fill_between(x[y>0], y[y>0],
                color='yellow', alpha=0.35)
            Vo = Vo
    plt.title('Diagrama de cortante')
    plt.xlabel('x [m]')
    plt.ylabel('V(x) [tf]')
    plt.grid()
    plt.show()

def plot_bending_moment(forces_beam, loads_applied, 
                     elements, lenghts):
    """
    Definition
    -------------------
    This function is defined to obtain the
    plot shear force of the beam

    Args:
    forces_beam: List of forces at each element
    loads_applied: List of loads applied on each element
    elements: Number of elements in the beam
    lengths: List of lengths of each element
    """
    for i in range(0, elements):
        if i == 0:
            l1 = 0
            Vo = forces_beam[2*i][0]
            Mo = -forces_beam[2*i+1][0]
        else:
            l1 = lenghts[i-1] + l1
            Vo = Vo+forces_beam[2*i][0]
            Mo = Mo-forces_beam[2*i+1][0]
        l2 = lenghts[i] + l1
        # Depending on the type of 
        # load applied to beam, the field graph 
        # is different, therefore a conditional 
        # is used
        if loads_applied[i][0] == 1:
            a = loads_applied[i][2] + l1
            p = loads_applied[i][1]
            x1 = np.linspace(l1, a, 
                        1000)
            x2 = np.linspace(a, l2, 
                        1000)
            y1 = Mo+Vo*(x1-l1)
            y2 = Mo+Vo*(x2-l1)-p*(x2-a)
            plt.plot(x1, y1, 
                color='black', linestyle='--')
            plt.plot(x2, y2,
                color='black', linestyle='--')
            plt.fill_between(x1[y1<0], y1[y1<0],
                color ='red', alpha=0.35)
            plt.fill_between(x1[y1>0], y1[y1>0],
                color='yellow', alpha=0.35)
            plt.fill_between(x2[y2<0], y2[y2<0],
                color ='red', alpha=0.35)
            plt.fill_between(x2[y2>0], y2[y2>0],
                color='yellow', alpha=0.35)
            Mo = Mo+Vo*(l2-l1)-p*(l2-a)
            Vo = Vo-p
        elif loads_applied[i][0] == 2:
            w = loads_applied[i][1]
            x = np.linspace(l1, l2, 
                    1000)
            y = Mo+Vo*(x-l1)-(w/2)*(x-l1)**2
            plt.plot(x, y, 
                color='black', linestyle='--')
            plt.fill_between(x[y<0], y[y<0],
                color='red', alpha=0.35)
            plt.fill_between(x[y>0], y[y>0],
                color='yellow', alpha=0.35)
            Mo = Mo+Vo*(l2-l1)-(w/2)*(l2-l1)**2
            Vo = Vo-w*(l2-l1)
        elif loads_applied[i][0] == 3:
            q1 = loads_applied[i][1]
            q2 = loads_applied[i][2]
            t = q2-q1
            dl = l2-l1
            m = (t/dl)*(1/2)
            x = np.linspace(l1, l2, 
                    1000)
            y = Mo+Vo*(x-l1)-(q1/2)*(x-l1)**2-(m/3)*(x-l1)**3
            plt.plot(x, y,
                color='black', linestyle='--')
            plt.fill_between(x[y<0], y[y<0],
                color='red', alpha=0.35)
            plt.fill_between(x[y>0], y[y>0],
                color='yellow', alpha=0.35)
            Mo = Mo+Vo*(l2-l1)-(q1/2)*(l2-l1)**2-(m/3)*(l2-l1)**3
            Vo = Vo-q1*(l2-l1)-m*(l2-l1)**2
        else:
            x = np.linspace(l1, l2,
                    1000)
            y = Mo+Vo*(x-l1)
            plt.plot(x, y,
                color='black', linestyle='--')
            plt.fill_between(x[y<0], y[y<0],
                color='red', alpha=0.35)
            plt.fill_between(x[y>0], y[y>0],
                color='yellow', alpha=0.35)
            Mo = Mo+Vo*(l2-l1)
            Vo = Vo
    plt.title('Diagrama de momento flector')
    plt.xlabel('x [m]')
    plt.ylabel('M(x) [tf - m]')
    plt.grid()
    plt.show()

def points_bending_moment(forces_beam, loads_applied, elements, lengths):
    """
    Definition
    --------------------
    This function is defined to obtain the plot shear force of the beam
    and identify the locations where the bending moment is zero, as well 
    as the maximum and minimum moments along each element

    Return
    --------------------
    List of x-coordinates where the bending moment is zero and list of 
    bending moment values corresponding to x_bending
    
    Args:
    forces_beam: List of forces at each element
    loads_applied: List of loads applied on each element
    elements: Number of elements in the beam
    lengths: List of lengths of each element
    """

    x_bending = []
    M_bending = []
    extrema_points = []

    for i in range(elements):
        if i == 0:
            l1 = 0
            Vo = forces_beam[2*i][0]
            Mo = -forces_beam[2*i+1][0]
        else:
            l1 = lengths[i-1] + l1
            Vo = Vo + forces_beam[2*i][0]
            Mo = Mo - forces_beam[2*i+1][0]
        
        l2 = lengths[i] + l1
        
        if loads_applied[i][0] == 1:
            a = loads_applied[i][2] + l1
            p = loads_applied[i][1]
            x1 = np.linspace(l1, a, 2000)
            x2 = np.linspace(a, l2, 2000)
            y1 = Mo + Vo*(x1 - l1)
            y2 = Mo + Vo*(x2 - l1) - p*(x2 - a)
            y = np.concatenate((y1, y2))
            x = np.concatenate((x1, x2))
            Mo = Mo + Vo*(l2 - l1) - p*(l2 - a)
            Vo = Vo - p
        elif loads_applied[i][0] == 2:
            w = loads_applied[i][1]
            x = np.linspace(l1, l2, 2000)
            y = Mo + Vo*(x - l1) - (w/2)*(x - l1)**2
            Mo = Mo + Vo*(l2 - l1) - (w/2)*(l2 - l1)**2
            Vo = Vo - w*(l2 - l1)
        elif loads_applied[i][0] == 3:
            q1 = loads_applied[i][1]
            q2 = loads_applied[i][2]
            t = q2 - q1
            dl = l2 - l1
            m = (t / dl) * (1/2)
            x = np.linspace(l1, l2, 2000)
            y = Mo + Vo*(x - l1) - (q1/2)*(x - l1)**2 - (m/3)*(x - l1)**3
            Mo = Mo + Vo*(l2 - l1) - (q1/2)*(l2 - l1)**2 - (m/3)*(l2 - l1)**3
            Vo = Vo - q1*(l2 - l1) - m*(l2 - l1)**2
        else:
            x = np.linspace(l1, l2, 2000)
            y = Mo + Vo*(x - l1)
            Mo = Mo + Vo*(l2 - l1)
            Vo = Vo

        if i == 0 and abs(forces_beam[1][0]) >  0.01:
            x_bending.append(0)
            M_bending.append(round(-forces_beam[1][0],3))
        elif i == 0:
            x_bending.append(0)
            M_bending.append(0)
        elif i == (elements - 1) and abs(Mo) > 0.01:
            x_bending.append(l2)
            M_bending.append(round(Mo, 3))

        # Identifying zero crossings
        zero_crossings = np.where(np.diff(np.sign(y)))[0]
        for zc in zero_crossings:
            x_bending.append(round(x[zc], 2))
            M_bending.append(round(y[zc], 3))
        
        # Finding maxima and minima
        maximun = np.argmax(y)
        minimun = np.argmin(y)
        
        extrema_points.append((x[maximun], y[maximun]))
        extrema_points.append((x[minimun], y[minimun]))
        
    
    # Removing duplicates and sorting extrema points by x-coordinate
    extrema_points = sorted(list(set(extrema_points)), key=lambda point: point[0])

    # In one list get all points in order

    xaux = []
    Maux = []

    for i in range(len(extrema_points)):
        xaux.append(round(extrema_points[i][0],2))
        Maux.append(round(extrema_points[i][1],3))
    
    for i in range(len(x_bending)):
        xaux.append(x_bending[i])
        Maux.append(M_bending[i])
    
    combined_points = list(zip(xaux, Maux))
    
    combined_points.sort(key=lambda point: point[0])
    
    xaux_sorted, Maux_sorted = zip(*combined_points)
    
    xaux_sorted = list(xaux_sorted)
    Maux_sorted = list(Maux_sorted)

    if not xaux_sorted[-1] == l2:
        xaux_sorted.append(l2)
        Maux_sorted.append(0)

    return xaux_sorted, Maux_sorted

def shear(Vo, load, length):
    """
    Definition
    --------------------
    This function is used to perform the calculation corresponding 
    to the shear equation for each different section

    Return
    --------------------
    Returns a list with shear forces and another with the lengths 
    where each corresponding shear force is located

    Args:
    Vo: shear force at the beginning of each section to perform the corresponding function
    load: load of the section in question
    length: length of section
    """

    l = length # is a constant that represent a length to section

    if load[0] == 1:
        a = load[2]
        p = load[1]
        x1 = np.linspace(0, a, 1000) # Note that here it is divided into two
        x2 = np.linspace(a, l, 1000) # sections of 1000, giving a total section of 2000
        V1 = Vo + 0*x1
        V2 = Vo - p + 0*x2
        x = np.concatenate([x1, x2])
        V = np.concatenate([V1, V2])
    elif load[0] == 2:
        w = load[1]
        x = np.linspace(0, l, 2000)
        V = Vo - w * x
    elif load[0] == 3:
        q1 = load[1]
        q2 = load[2]
        x = np.linspace(0, l, 2000)
        t = q2 - q1
        m = (t / l) * (1/2)
        V = Vo - q1 * x - m * x**2
    else:
        x = np.linspace(0, l, 2000)
        V = Vo + 0 * x
    
    # At the end it returns two lists that contain: a list 
    # with the shear stresses of the section and a second with 
    # the locations of each shear force. Note: to understand 
    # the calculation specified above it is necessary to review 
    # the shear force and moment diagrams found in books such as 
    # Mechanics of Materials

    return V, x

def shear_design(V, x, d, length, total_length, Vc, fi, b, com_con):
    """
    Definition
    -------------------------
    This function is used to perform the corresponding calculations to 
    obtain the transverse reinforcement of the beam. To do this, two arrays 
    containing the information from the shear force diagrams are reviewed. 
    Likewise, the length of the section and the height d are requested, 
    to determine where the beam begins to support the shear

    Return
    ------------------------
    According to the definition given, it returns values that correspond 
    to the design and are explained throughout the function. Therefore, no emphasis 
    is placed on a prior explanation

    Args:
    V: list with shear
    x: list with ubication shear
    d: height
    length: length of section
    total_length: is the cumulative length up to that section
    Vc: The shear stress that concrete can withstand
    fi: security factor
    b: base of section
    com_con: compresion of concrete (according to design)
    """

    l = length
    lt = total_length
    d = d / 100 # pass cm to m
    Vc = round(Vc, 3)
    try:
        lfi = l - d
        result = np.where((x > d) & (x < lfi))
        # The maximum shear is taken where the beam really begins to support, 
        # which is at a distance called d, which is found in the NSR - 10, title C
        V = V[result]
        x = x[result]
        Vd, Vi= abs(V[0]), abs(V[-1])
        ld, li = x[0], x[-1] # corresponds to the right and left cutters
        Vsd = (Vd/fi) - Vc
        Vsi = (Vi/fi) - Vc
        x1 = lt + ld
        x4 = lt + li
        if Vsd > 0 or Vsi > 0:
            As = 2 * (((3/8) * 2.54)**2) * (np.pi/4) # Normally an N3 rod is used for stirrups
            obs = "El nervio requiere estribos!" 
        else:
            As = 0
            obs = "El nervio no requiere estribos!"
        if Vsd < 0:
            x2 = "NA"
            s1 = 0
            s2 = 0
        else:
            result = np.where(V < Vc)
            xd = x[result]
            x2 = lt + xd[0]
            x2 = round(x2, 2)
            if Vsd > 1.1 * b * d * (com_con**0.5): # according to NSR - 10, title C11
                if d/2 > 60:
                    s1 = 15 # cm
                    s2 = 2*s1
                else:
                    s1 = d/4
                    s2 = 2*s1
            else:
                smin1, smin2 = (4200*As)/(0.2*(com_con)**0.5*b), (4200*As)/(3.5*b)
                if smin1 > smin2:
                    smin = smin2
                    if smin > d/2:
                        s1 = d/2
                    elif smin > 60:
                        s1 = 60
                    else:
                        s1 = smin
                else:
                    smin = smin1
                    if smin > d/2:
                        s1 = d/2
                    elif smin > 60:
                        s1 = 60
                    else:
                        s1 = smin
                s2 = 2*s1

        if Vsi < 0:
            x3 = "NA"
            s3 = 0
            s4 = 0
        else:
            result = np.where(V > -Vc)
            xi = x[result]
            x3 = lt + xi[-1]
            x3 = round(x3, 2)
            if Vsi > 1.1 * b * d * (com_con**0.5): # according to NSR - 10, title C11
                if d/2 > 60:
                    s3 = 15 # cm
                    s4 = 2*s1
                else:
                    s3 = d/4
                    s4 = 2*s1
            else:
                smin1, smin2 = (4200*As)/(0.2*(com_con)**0.5*b), (4200*As)/(3.5*b)
                if smin1 > smin2:
                    smin = smin2
                    if smin > d/2:
                        s3 = d/2
                    elif smin > 60:
                        s3 = 60
                    else:
                        s3 = smin
                else:
                    smin = smin1
                    if smin > d/2:
                        s3 = d/2
                    elif smin > 60:
                        s3 = 60
                    else:
                        s3 = smin
                s4 = 2*s3

        s1, s2 = np.min(np.array([s1, s2, s3, s4])), np.max(np.array([s1, s2, s3, s4]))

        # conditional to avoid errors in data processing.
        # That is, 0 does not appear if it is not necessary
        if x2 != "NA":
            if abs(x1 - x2) < 0.01:
                x2 = "NA"

        if x3 !="NA":
            if abs(x3 - x4) < 0.01:
                x3 = "NA"

        if x2 == "NA" and x3 == "NA":
            s1 = 0
        elif s1 == 0:
            s1 = s2/2
    except:
        Vd, Vi, As, x1, x2, x3, x4, s1, s2 = 0, 0, 0, 0, 0, 0, 0, 0, 0 
        obs = "No se comporta el problema como un nervio"

    # Several values ​​are provided that help with the design, these are:
    # 1. Vd, Shear at the beginning of the section
    # 2. Vi, Shear at the end of the section
    # 3. As, Cross section steel (area)
    # 4. Vmax, The largest shear supported by the beam
    # 5. x1, Location of the first section of abutments
    # 6. s1, Separation of reinforcement
    # 7. x2, Location of the second section of abutments
    # 8. s2, separation of reinforcement
    # 9. obs, string with information of calculation 

    Vd, Vi, As, x1 = round(Vd, 2), round(Vi, 2), round(As, 2), round(x1, 2)
    x4, s1, s2 =  round(x4, 2), round(s1, 2), round(s2, 2)

    return Vd, Vi, As, x1, x2, x3, x4, s1, s2, obs     
# This code is responsible for asking the user for all the input 
# data to generate the output data.

import numpy as np
def numbers_of_elements():
    """
    Definition
    ------------------------
    This function is responsible for asking the user to enter 
    the number of elements that correspond to the beam

    Return
    -----------------------
    The number of sections that the user was asked to enter 
    (it is important to clarify that this number cannot be corrected at any 
    time and if the user does so, he/she must re-enter the data by restarting 
    the program)

    Args:
    Nothing
    """
    j = 0
    while j<1:
        try:
            n = int(input('Ingrese el número de tramos que ' +
                          'tiene la viga: '))
            if n<=0:
                print('Un número negativo o igual a cero (0) ' 
                      + 'no tiene sentido.')
            elif n < 101:
                j += 1
            else:
                print('El programa no permite un número de ' 
                      + 'tramos superior a los 100.')
        except:
            print('El número digitado no es válido')
        
    return n
    
def def_lengths(n):
    """
    Definition
    -------------------------
    This function asks the user for the length of each section, note 
    that it has to avoid possible errors. Also, caution must be taken, 
    since the program can crash if the user does not type correctly

    Return
    -------------------------
    list of lengths for each respective leg, in the order they were 
    requested (i.e., as people normally count)

    Args:
    n: number of elements
    """
    lengths = []
    for i in range(0, n):
        j = 0
        while j < 1:
            try:
                l = float(input('Ingrese la longitud ' +
                                f'del tramo {i+1}: '))
                if l <= 0:
                    print('Un número negativo o igual ' +
                          'a cero (0) no tiene sentido.')
                elif l < 16:
                    j += 1
                    lengths.append(l)
                else:
                    print('El programa no contempla ' 
                + 'longitudes superiores o iguales a los 16 m.')
            except:
                print('El valor digitado no es válido')
            
    return lengths

def restrictions_beam(n):
    """
    Definition
    -------------------------
    This function is responsible for storing the type 
    of restrictions that a beam has along its length.
    

    Return
    -------------------------
    list

    Args:
    n: number of element
    
    """
    restriction = []
    for i in range(0, n):
        j = 0
        while j < 1:
            if i+1 == n:
                try:
                    con1 = str(input(f'Al inicio del tramo {i+1} ' +
                    'está empotrado [e], empotrado con patines ' +
                    '[ep], \napoyado [a] o libre [l]:'))
                    con2 = str(input(f'Al final del tramo {i+1} ' +
                    'está empotrado [e], empotrado con patines ' +
                    '[ep], \napoyado [a] o libre [l]:'))
                    j += 1  
                    restriction.append(con1)
                    restriction.append(con2)                 
                except:
                    print('Ingrese una condición válida.')
            else:
                try:
                    con = str(input(f'Al inicio del tramo {i+1} ' + 
                            'está empotrado [e], empotrado con ' + 
                            'patines [ep], \napoyado [a] o libre [l]:'))
                    j += 1   
                    restriction.append(con)                
                except:
                    print('Ingrese una condición válida.')
    restriction = [0 if conditions == "e" or conditions == 'E'
        else conditions for conditions in restriction]
    restriction = [1 if conditions == "eP" or conditions == 'Ep' or
        conditions == 'ep' or conditions == 'EP'
        else conditions for conditions in restriction]
    restriction = [2 if conditions == "A" or conditions == 'a'
        else conditions for conditions in restriction]
    restriction = [3 if conditions == "L" or conditions == 'l'
        else conditions for conditions in restriction]
    nodes_beam(restriction)
    return restriction

def nodes_beam(restriction):
    matrix_X = []
    for i in range(0, len(restriction)):
        if restriction[i] == 0:
            matrix_X.append(0)
            matrix_X.append(0)
        elif restriction[i] == 1:
            matrix_X.append(1)
            matrix_X.append(0)
        elif restriction[i] == 2:
            matrix_X.append(0)
            matrix_X.append(1)
        else:
            matrix_X.append(1)
            matrix_X.append(1)
    return matrix_X

def kind_loads(n):
    """
    Definition
    ----------------------
    This function stores the type of loads that the beam has. This is categorized as:
       1. Point load
       2. Distributed load
       3. Linear load
       4. No load

    Return
    ----------------------
    list with loads

    Args:
    n: number of elements
    """
    loads_applied = []
    for i in range(0, n):
        j = 0
        while j<1:
            print('Seleccione la carga aplicada '+
            f'en el tramo {i+1}, según el numeral '+
            'que aplique:\n 1. Puntual.\n 2. Dis'+
            'tribuida.\n 3. Trapezoidal.\n 4. No está'+
            ' sometido a ninguna carga.')
            try:
                op = int(input('Digite la opción: '))
                if op in [1,2,3,4]:
                    j+=1
                else:
                    print('Ha seleccionado un rango '+
                    'diferente al establecido. Por favor, '+
                    'vuelva a intentarlo.')
            except:
                print('Ha digitado un número no ' +
                      'válido.')
        j=0
        while j<1:
            try:
                if op==1:
                    p = float(input('Digite el valor de '+
                    'la carga puntual [tf]: '))
                    l = float(input('Digite la ubicación de '+
                    'la carga puntual, medida desde la derecha\n' +
                    'del tramo inicial [m]: '))
                    matrix_draw = [op, p, l]
                elif op==2:
                    w = float(input('Digite la carga distribuida '+
                    'sometida [tf/m]: '))
                    matrix_draw = [op, w]
                elif op==3:
                    w1 = float(input('Digite la carga distribuida '+
                    'al inicio del tramo [tf/m]: '))
                    w2 = float(input('Digite la carga distribuida '+
                    'al final del tramo [tf/m]: '))
                    matrix_draw = [op, w1, w2]
                else:
                    matrix_draw = [4]
                j+=1
                loads_applied.append(matrix_draw)
            except:
                print('Ha ingresado un valor no válido.\n Por favor'+
                ', vuelva a digitar correctamente.')
    return loads_applied
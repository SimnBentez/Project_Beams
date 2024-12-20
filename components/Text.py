import ezdxf

def Diameter_bar(N_road):
    """
    Definition
    ----------------------
    
    
    Return
    ----------------------

    Args:
    N_road: number of road (N3, N4, ...)
    """

    try:
        db = int(N_road)/8
        db = db * 2.54
    except:
        db = 1

    return db

def Beam_lengthwise():
    """
    Definition
    -------------------------
    This function performs the breakdown of the design of the concrete beam. 
    A drawing is made in .dxf format (compatible with AutoCAD) where the drawing 
    corresponding to the beam with its respective longitudinal and transverse 
    reinforcement is found

    Return
    ------------------------
    Returns a text string indicating that the design has been saved in the Results folder. 
    Note: The user must name the file

    Args:
    """

    name = str(input('Coloque un nombre para el archivo correspondiente: '))

    try:
        a = f"Se ha guaradado correctamente el archivo en Resultados/{name}.dxf."
    except:
        a = f"Se ha presentado un error al guardar el archivo {name}.dxf. Vuelva a intentarlo."

    return print(a)
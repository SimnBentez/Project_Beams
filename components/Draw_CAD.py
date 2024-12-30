import ezdxf
import random  # needed for random placing points
import os
from components.Design import design_moment_beam, design_shear_beam
import numpy as np


def Initialize_Draw(b, h, lt, r, data_long, data_trans):
    """
    Definition
    -------------------------
    This function is responsible for initializing the drawing in dxf, although 
    it has been wrongly named as "AutoCAD", it does not draw the library directly 
    in said program; on the contrary, it is possible to add other things to the 
    drawing from this CAD. It also uses two additional functions to generate the 
    steel reinforcement in the concrete beam. It should be noted that due to the 
    development lengths and moment diagrams, there is always steel in the lower 
    part of the element.

    Receive the first 4 parameters and two dictionaries (data_long and data_trans) 
    that contain enough information to graph the reinforcement as the moment location 
    and its location, what really matters is this and its location as 
    will be seen later, although the type of rod is taken into account, 
    it is more to place it in the legend of the plan.

    Return
    -------------------------
    This function does not return anything specific, but delivers the drawing 
    in the same path where the program is located in the folder previously 
    created for the report.

    Args:
    b: base of beam
    h: height of beam
    lt: total length
    r: reinforcement coating
    data_long: dictionary containing information on longitudinal steel
    data_trans: dictionary containing information on cross sectional steel
    """

    doc = ezdxf.new('R2010')
    doc.header['$INSUNITS'] = 5 # units in cm
    msp = doc.modelspace()

    face = msp.add_lwpolyline([(0,0), (0,h), (b,h),
                                        [b,0]])
    
    face.close(True)
    
    vertices = [(2*b, 0), (2*b, h), (2*b + lt, h), (2*b + lt, 0)]

    body = msp.add_lwpolyline(vertices)

    body.close(True)

    # Reinforcement in cross section

    bar_trans = (3/8)*2.54

    cen_bar_trans = r + bar_trans + 0.8

    center = [(cen_bar_trans, cen_bar_trans), (cen_bar_trans, h - cen_bar_trans), 
              (b - cen_bar_trans, h - cen_bar_trans), (b - cen_bar_trans, cen_bar_trans)]
    
    for i in range(len(center)):
        msp.add_circle(center[i], 0.8, dxfattribs={"color":1})
        
    y_cen_bar_double = cen_bar_trans + 2.5

    center = [(cen_bar_trans, y_cen_bar_double), (cen_bar_trans, h - y_cen_bar_double), 
              (b - cen_bar_trans, h - y_cen_bar_double), (b - cen_bar_trans, y_cen_bar_double)]
    
    for i in range(len(center)):
        msp.add_circle(center[i], 0.8, dxfattribs={"color":5})

    

    msp.add_aligned_dim(p1=(0,0), p2=(0,h), distance=2, override={"dimtad":0,
                                                                  "dimtxt": 2,
                                                                  "dimblk": "OBLIQUE",
                                                                  "dimasz": 2}).render()
    
    msp.add_aligned_dim(p1=(0,0), p2=(b,0), distance=-2, override={"dimtad":0,
                                                                  "dimtxt": 2,
                                                                  "dimblk": "OBLIQUE",
                                                                  "dimasz": 2}).render()

    msp.add_text(
        text="N1", height=2, dxfattribs={"color":1}).set_placement(
            (b/2, 1), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)
    
    text = ["CONVENCIONES:", "SEGUNDA CAPA", "REFUERZO PPL"]

    for i in range(len(text)):
        if i == 0:
            w = -8
            msp.add_text(text=text[i], height=2, dxfattribs={"color":1}).set_placement(
            (b/4, w), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)
        else:
            w -= 3
            msp.add_text(text=text[i], height=2, dxfattribs={"color":1}).set_placement(
            (b/4 + 2.5, w), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)
            if w == -14:
                msp.add_circle((-9, w), 0.8, dxfattribs={"color":1})
            else:
                msp.add_circle((-9, w), 0.8, dxfattribs={"color":5})

    
    msp.add_aligned_dim(p1=(2*b, 0), p2=(2*b+lt, 0), text=f"L={int(lt)}", distance=-2,
                    override={"dimtad":0,
                                "dimtxt": 2,
                                "dimblk": "OBLIQUE",
                                "dimasz": 2}).render()
    
    #reinforcing_steel_long(msp, b, h, r, data_long)

    #reinforcing_steel_trans(msp, b, h, r, data_trans)

    name = str(input('Ingrese el nombre del archivo .dxf: '))
    # save the drawing

    folder_name = "Resultados"
    if not os.path.exists(folder_name):
       os.makedirs(folder_name)
    doc.saveas(f"./Resultados/{name}.dxf")

def reinforcing_steel_long(msp, b, h, r, dict):
    """
    Definition
    -----------------
    This function is responsible for locating the longitudinal 
    reinforcement in the beam in the drawing. To do this, 
    it is necessary to review certain parameters and a dictionary 
    that is responsible for indicating where the steel is located, 
    if it is a doubly reinforced location, and the lengths that must be met.

    Return
    -----------------
    No return

    Args:
    msp: model space
    b: base
    h: height
    r: reinforcement coating
    dict: dictionary longitudinal steel (design)
    """

    d = h - r

    ubi_x = dict["Ubicación del momento (m)"]
    condition = dict['Zona de colocación del refuerzo']
    bar_simple = dict['Número de varilla 1']
    bar_second = dict['Número de varilla 2']

    

def reinforcing_steel_trans(msp, b, h, r, dict):
    """
    Definition
    -----------------
    This function is responsible for distributing the transverse steel 
    that may exist in the beam due to shear. For this you receive a dictionary 
    that contains the information to carry out this type of design.

    Return
    -----------------
    No return

    Args:
    msp: model space
    b: base
    h: height
    r: reinforcement coating
    dict: dictionary transversal steel (design)
    """

    d = h - r
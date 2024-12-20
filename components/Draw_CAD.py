import ezdxf
import random  # needed for random placing points
import os
from components.Design import design_moment_beam, design_shear_beam


def Initialize_Draw(b, h, lt):
    """
    Definition
    -------------------------
    Return
    -------------------------

    Args:
    b: base of beam
    h: height of beam
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
            (b/2, 2), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)
    
    msp.add_aligned_dim(p1=(2*b, 0), p2=(2*b+lt, 0), text=f"L={int(lt)}", distance=-2,
                    override={"dimtad":0,
                                "dimtxt": 2,
                                "dimblk": "OBLIQUE",
                                "dimasz": 2}).render()

    name = str(input('Ingrese el nombre del archivo .dxf: '))
    # save the drawing

    folder_name = "Resultados"
    if not os.path.exists(folder_name):
       os.makedirs(folder_name)
    doc.saveas(f"./Resultados/{name}.dxf")
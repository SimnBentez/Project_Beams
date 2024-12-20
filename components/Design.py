from components.Functions import *
from components.Auxiliary_functions import *
import pandas as pd
import math
import os

def design_moment_beam(forces_beam, loads_applied, elements, lengths, height, base, r, 
                       com_con):
    """
    Definition
    ---------------------------
    This function is performed to make the 
    calculations corresponding to the moment design

    Return
    ---------------------------
    This function returns two dictionaries that are used to have all the design data such 
    as the parameters used, the design moment, the length where this moment is located, 
    the area to be designed, etc

    Args:
    forces_beam: List of forces at each element
    loads_applied: List of loads applied on each element
    elements: Number of elements in the beam
    lengths: List of lengths of each element
    height: height of beam (h)
    base: base of beam (b)
    r: It is known as the coating spacing, this depends on the regulations. In this case, NSR - 10
    com_con: Compressive strength (f'c)
    """

    xM, M = points_bending_moment(forces_beam, loads_applied, elements, 
                                  lengths) # first get interest pointing
    
    xM, M = re_array_bending(xM, M)
    
    # Now some constants are initialized inside the code to get the layout results

    fc, fy, Es, epc = com_con, 4200, 2e6, 0.003 # kgf/cm², kgf/cm², (1)

    b, d, dps = base, height - r, r

    Rmn, Rn, Rmx, Ast1, obs, Ast2 = [], [], [], [], [], []

    for i in range(len(M)):
        Mu = abs(M[i])
        # calculation of constants
        m = fy / (0.85 * fc)
        if fc <= 280:
            Beta = 0.85
        elif fc > 280 and fc < 560:
            Beta = 0.85 - (fc - 280) * (0.05 / 70)
        else:
            Beta = 0.65

        ## Calculation of maximum, minimum and intermediate values

        esmax = 0.005
        FI = 0.9
        CDmax = epc / (epc + esmax)
        Pmax = CDmax * Beta / m
        Rmax = Pmax * fy * (1 - Pmax * m / 2)
        Rmx.append(Rmax)
        Asmax = Pmax * b * d
        esint = 0.004
        CDint = epc / (epc + esint)
        Pint = CDint * Beta / m
        Rint = Pint * fy * (1 - Pint * m / 2)
        Pmin1 = 14 / fy
        Pmin2 = 0.8 * math.sqrt(fc) / fy
        if Pmin1 > Pmin2:
            Pmin = Pmin1
        else:
            Pmin = Pmin2
        CDmin = Pmin * m / Beta
        esmin = epc * (1 - CDmin) / CDmin
        Rmin = Pmin * fy * (1 - Pmin * m / 2)
        Rmn.append(Rmin)
        Asmin = Pmin * b * d
        ## Design of simply reinforced sections
        if Mu > 8e-2:
            R = Mu * 100000 / (FI * b * d ** 2)
            if R > fy / (2 * m):
                R = fy / (2 * m)
                Rn.append(R)
                PD = (1 / m) * (1 - math.sqrt (1 - 2 * m * R / fy))
                CD = PD * m / Beta
                es = epc * (1 - CD) / CD
                As1 = PD * b * d
                Ast1.append(round(As1, 3))
                Ast2.append(0)
                obs.append('R > (fy/2m). ¡Ojo!')
            elif R < Rmin:
                R = Rmin
                Rn.append(R)
                PD = Pmin
                CD = CDmin
                es = esmin
                As1 = Asmin
                Ast1.append(round(As1, 3))
                Ast2.append(0)
                obs.append('La sección requiere valores mínimos')
            elif R > Rmax:
                R = Mu * 100000 / (FI * b * d ** 2)
                Rn.append(R)
                As1 = Asmax
                Mu1 = Rmax * FI * b * d ** 2 / 100000
                Mu2 = Mu - Mu1
                Mu2 = abs(Mu2)
                c = As1 * fy / (0.85 * fc * Beta * b)
                eps = epc * (c - dps) / c
                if eps >= fy / Es:
                    fps = fy
                else:
                    fps = epc * Es * (c - dps) / c
                Aps = Mu2 * 100000 / (FI * fps * (d - dps))
                As2 = Aps * fps / fy
                Ast1.append(round(As1, 3))
                Ast2.append(round(As2, 3))
                obs.append('La sección requirió doble refuerzo')
            else:
                Rn.append(R)
                PD = (1 / m) * (1 - math.sqrt (1 - 2 * m * R / fy))
                CD = PD * m / Beta
                es = epc * (1 - CD) / CD
                As1 = PD * b * d
                Ast1.append(round(As1, 3))
                Ast2.append(0)
                obs.append('Ok')
        else:
            Rn.append(0)
            Ast1.append(0)
            Ast2.append(0)
            obs.append('N/A')

    Areas1, Nareas1, error1 = Select_bar_steel(Ast1)

    Areas2, Nareas2, error2 = Select_bar_steel(Ast2)

    condition = steel_condition(M)

    for i in range(len(M)):
        if abs(M[i]) > 8e-2:
            M[i] = abs(M[i])
        else:
            M[i] = 0
        Rmx[i] = round(float(Rmx[i]), 3)
        Rn[i] = round(float(Rn[i]), 3)
        if Rn[i] == 0:
            Rn[i] = 'N/A'
        
        if Ast1[i] == 0:
            Ast1[i] = 'N/A'
        elif Ast1[i] != 0:
            Ast1[i] = round(float(Ast1[i]), 3)
        
        if Ast2[i] != 0:
            Ast2[i] = round(float(Ast2[i]), 3)
        elif Ast2[i] == 0:
            Ast2[i] = 'N/A'

        Rmn[i] = round(float(Rmn[i]), 3)       

    # Now the data used for the calculation is saved in a dictionary, as well as the results, 
    # to later use a function that passes said data to an Excel

    data2 = {
        "Momentos (tf-m)": M,
        "Ubicación del momento (m)": xM,
        "Zona de colocación del refuerzo": condition,
        "R máxima (kg/cm²)": Rmx,
        "R (kg/cm²)": Rn,
        "R mínima (kg/cm²)": Rmn,
        "As1 Requerido (cm²)": Ast1,
        "Área 1 seleccionada (cm²)": Areas1,
        "Número de varilla 1": Nareas1,
        "Error 1 (%)": error1,
        "As2 Requerido (cm²)": Ast2,
        "Área 2 seleccionada (cm²)": Areas2,
        "Número de varilla 2": Nareas2,
        "Error 2 (%)": error2,
        "Observación": obs
    } # out data

    data1 = {
        'Datos de entrada':['f´c (kg/cm²)','fy (kg/cm²)','Es (kg/cm²)',
        'ℇ´c','B (cm)', 'd (cm)', 'd´ (cm)','β', 'Φ'], 
        '':[fc,fy,Es,epc,b,d,dps,Beta, 0.9]
    } # Entry data to design

    return data1, data2
    

def design_shear_beam(forces_beam, loads_applied, elements, lengths, height, base, r, com_con):
    """
    Definition
    ----------------------------------
    This function is used to obtain the shear design (stirrups) of the beam under 
    the NSR - 10 regulations. Keep in mind that this entire program was made under 
    said regulations, so it is likely to differ slightly from other more demanding 
    standards such as the American and European regulations

    Return
    ---------------------------------
    Returns two dictionaries containing the input data for the shear design and the 
    output data, so that they can be passed to the corresponding Excel file

    Args:
    forces_beam: List of forces at each element
    loads_applied: List of loads applied on each element
    elements: Number of elements in the beam
    lengths: List of lengths of each element
    height: height of beam (h)
    base: base of beam (b)
    r: It is known as the coating spacing, this depends on the regulations. In this case, NSR - 10
    com_con: Compressive strength (f'c)
    """

    fi = 0.75 # Safety factor for shear

    b, d = base, height - r # constants
    # concrete shear

    Vc = 0.53 * math.sqrt(com_con) * b * d * 1 # 1 is lambda

    Vc = Vc / 1000 # kg to tf

    Vd, Vi, As, x1, x2, x3, x4, s1, s2, obs = [], [], [], [], [], [], [], [], [], []

    Vo = 0
    tlen = 0

    for i in range(elements):
        Vo = Vo + forces_beam[2*i]
        loads = loads_applied[i]
        l = lengths[i]

        V, x = shear(Vo, loads, l)

        Vo = V[-1]

        Vdp, Vip, Asp, x1p, x2p, x3p, x4p, s1p, s2p, obsp = shear_design(
            V, x, d, l, tlen, Vc, fi, base, com_con)
        
        Vd.append(Vdp), Vi.append(Vip), As.append(Asp), x1.append(x1p), x2.append(x2p)

        x3.append(x3p), x4.append(x4p), s1.append(s1p), s2.append(s2p), obs.append(obsp)

        tlen += l


    data1 = {
        'Datos de entrada':['f´c (kg/cm²)','fy (kg/cm²)','B (cm)',
        'd (cm)', 'Φ'], 
        '':[com_con, 4200, b, d, fi]
    }

    data2 = {
        "Cortante derecho (tf)": Vd,
        "Cortante izquierdo (tf)": Vi,
        "Área transversal (cm²)": As,
        "Ubicación cortante derecho (m)": x1,
        "Ubicación sin cortante derecho (m)": x2,
        "Espaciamiento del refuerzo 1 (cm)": s1,
        "Ubicación cortante izquierdo (m)": x3,
        "Ubicación sin cortante izquierdo (m)": x4,
        "Espaciamiento del refuerzo 2 (cm)": s2,
        "Observaciones": obs
    }

    return data1, data2

def Excel_data(data_one, data_two, data_three, data_four):
    """
    Definition
    -----------------------------------
    This function was created so that the user can obtain an Excel file with the design results

    Return
    -----------------------------------
    Returns an Excel file with the design data so it can be used as a spreadsheet

    Args:
    data_one: data1 from design_moment_beam
    data_two: data2 from design_moment_beam
    data_three: data1 from design_shear_beam
    data_four: data2 from design_shear_beam
    """

    folder_name = "Resultados"

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    name = str(input('Escriba como quiera que se llame el archivo de Excel del diseño: '))

    data_null = {}

    df_null = pd.DataFrame(data_null)
    df_null.to_excel(f'./Resultados/{name}.xlsx', index=False)
    write = pd.ExcelWriter(f'./Resultados/{name}.xlsx')
    df1 = pd.DataFrame(data_one)
    df2 = pd.DataFrame(data_two)
    df3 = pd.DataFrame(data_three)
    df4 = pd.DataFrame(data_four)
    df1.to_excel(excel_writer=write, sheet_name="Datos RL", index=False)
    df2 .to_excel(excel_writer=write, sheet_name="Refuerzo longitudinal", index=False)
    df3.to_excel(excel_writer=write, sheet_name="Datos RT", index=False)
    df4.to_excel(excel_writer=write, sheet_name="Refuerzo transversal", index=False)
    write.close()

    a = print('El archivo de Excel se encuentra en la misma carpeta del '+
              'código. Se encuentra bajo el nombre de ' + name + '.xlsx')
    return a
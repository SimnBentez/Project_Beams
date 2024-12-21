# Project Beam | Structural Design

## [ES] Español

### Introducción

El proyecto *Project Beam* tiene como objetivo desarrollar una solución eficiente para el diseño estructural de vigas, integrando cálculos de cargas, análisis de esfuerzos y visualización de resultados. Este enfoque combina herramientas computacionales como lo es el lenguaje de programación *python* y metodologías de diseño modernas; basándose en la norma NSR - 10, título C y la ACI.

### Objetivos

1. Crear un modelo estructural que permita analizar el comportamiento de vigas sometidas a diferentes condiciones de carga.
2. Visualizar diagramas de cortante y momento flector para facilitar y corroborar la interpretación de resultados.
3. Generar un reporte en dos archivos: Excel y dxf. Permitiendo revisar el reporte de los cálculos hechos por el programa y un archivo de AutoCAD de los planos.

### Metodología

1. Implementación de modelos matemáticos utilizando Python y bibliotecas especializadas (*Sympy*, *Numpy*, *Matplotlib*, etc).
2. Visualización interactiva de los diagramas estructurales utilizando utilizando *Matplotlib*.
3. Validación de los resultados mediante comparaciones con normas y estándares (NSR-10, ACI).

### Resultados esperados

* Diagramas claros de momento flector y fuerza cortante.
* Código estructurado y documentado para replicar los análisis.
* Reportes exportables, como se mencionó anteriormente, en archivo .xlsx (Excel) y formato .dxf para AutoCAD.

## Guía de usuario

### Instalación

Primero, debe verificar que tenga las librerías instaladas como *sympy*, *numpy*, *ezdxf* y *matplotlib* como se presenta a continuación:

```bash
pip install sympy numpy matplotlib ezdxf
```
Después, sería ideal revisar si se ha descargado correctamente las dependencias correspondientes (carpetas) y archivo principal de este repositorio. De acuerdo con lo anterior, ya se podría utilizar la herramienta sin problemas.

### Inicialización

Para inicializar el programa, basta con ejecutar el archivo de Python. Esto puede realizarse seleccionando la opción "Run" en su entorno de desarrollo integrado (IDE) o presionando la tecla F5 si esta función está habilitada.

Para orientar al usuario en los pasos que debe seguir, se recomienda revisar un ejercicio relacionado con el análisis de una viga. A continuación, se plantea el siguiente problema:

![image](https://github.com/user-attachments/assets/80c9ee5c-d079-4475-ac33-431d91b7a8fe)

Al iniciar el código aparece en la zona inferior o la terminal del editor de código lo siguiente:

![image](https://github.com/user-attachments/assets/d4d8ab37-e913-47a4-8e0e-4242721c1777)

Para definir el número de tramos que tiene la viga, es necesario, primero definir qué es un tramo. Un tramo se define como la longitud donde cambia de apoyo una viga. Es decir; cada vez que haya una longitud entre dos apoyos se considera como un tramo. También, cada vez que cambie una carga distribuida. Por ejemplo, para este caso se tienen dos tramos ya que pasa de un apoyo empotrado a uno libre que es cuando inicia la carga y otro que es cuando inicia y finaliza la carga, respectivamente. De acuerdo con esto, se selecciona entonces que se tienen dos tramos en el problema.

![image](https://github.com/user-attachments/assets/164c18dc-32ee-4a63-b682-561bbe40bb16)

Luego el programa necesitará que se le dé la longitud de los tramos correspondientes (en este caso, la longitud de los 2 tramos), para este ejercicio se supone que la carga distribuida es 1.8 tonf/m y la longitud total es de 6 metros.

![image](https://github.com/user-attachments/assets/45029555-2041-4a49-b920-ffd5a3ef0de1)

Ahora, el programa solicitará que se le indique los apoyos a los que está sometido el problema, en este caso se tiene el siguiente resultado:

![image](https://github.com/user-attachments/assets/0b64acf7-8ed8-4fce-8c43-f5b2b145c9b2)

Posteriormente, el programa pedirá que se le describa las cargas a las que está sometido cada tramo. Por lo cual, se especifica a continuación:

![image](https://github.com/user-attachments/assets/c7d702e0-2e2f-4d51-ae25-7cd160c6a58d)

Una vez se digite toda la información, el programa arrojará los diagramas correspondientes como se muestra a continuación:

#### Diagrama de cortante

![image](https://github.com/user-attachments/assets/f4221272-7076-49dc-8948-2ce411ef4c6a)


#### Diagrama de momento flector

![image](https://github.com/user-attachments/assets/033867d8-304d-41f0-aa41-4fde45521762)

Finalmente, el programa pedirá que se le indique si se desea diseñar o no la viga que se analizó, por lo cual pedirá los últimos datos de entrada que necesitará el programa. **Nota:** se recuerda que este programa **solo** realiza vigas rectangulares de concreto, por lo cual no hay mucha variedad en su geometría, sin embargo, este enfoque permite que se optimice de la mejor manera los cálculos estructurales.

![image](https://github.com/user-attachments/assets/313a88e0-60d9-4b8c-8ece-470d7f3e3950)

Una vez realizado esto último, el programa solicitará los nombres correspondientes para el archivo de Excel y el de dibujo en AutoCAD.

![image](https://github.com/user-attachments/assets/911aa7a8-19f2-4187-981e-420b0c15a75f)

No obstante, se presenta que los archivos son guardados en una carpeta en el propio proyecto llamada "Resultados", donde se encuentran ambos archivos.

![image](https://github.com/user-attachments/assets/4667cccd-9d01-4f3a-901e-8fd6b02ad2a4)

#### Precauciones y recomendaciones

1. No se presenta el contenido de los archivos puesto a que ya se publicaron en el LinkedIn del autor del proyecto original.
2. En caso de que nombre archivos iguales, trate de tener estos cerrados puesto a que puede ocasionar conflictos con el sistema operativo.
3. Este programa no es perfecto, lo cual puede arrojar errores inesperados y se espera seguir mejorando a futuro en un trabajo mucho más completo.
4. Este programa es de uso libre y sin ánimo de lucro, por lo cual cualquier persona puede utilizarlo. Sin embargo, se debe hacer bajo su propia responsabilidad.

![image](https://github.com/user-attachments/assets/1427d2d9-fcfd-4c7a-aa8e-9af232d2499c)

---

## [EN] English

### Introduction

The *Project Beam* aims to develop an efficient solution for the structural design of beams, integrating load calculations, stress analysis, and result visualization. This approach combines advanced computational tools and modern design methodologies.

### Objectives

1. Develop a structural model to analyze the behavior of beams under various loading conditions.
2. Visualize shear and bending moment diagrams to facilitate and verify the interpretation of results.
3. Generate a report in two files: Excel and DXF, allowing for the review of the calculations performed by the program and an AutoCAD file with the plans.

### Metodology

1. Implementation of mathematical models using Python and specialized libraries (Sympy, Numpy, Matplotlib, etc).
2. Interactive visualization of structural diagrams using Matplotlib.
3. Validation of results through comparisons with codes and standards (NSR-10, ACI).

### Expected Results

* Clear diagrams of bending moments and shear forces.
* Structured and documented code for replicating analyses.
* Exportable reports, as mentioned earlier, in .xlsx (Excel) and .dxf formats.

## User Guide

### Installation

First, ensure that the following libraries are installed: *sympy*, *numpy*, *ezdxf*, and *matplotlib*. You can install them by running the following command in the terminal:

```bash
pip install sympy numpy matplotlib ezdxf
```

### Initialization

To start the program, simply execute the Python file. This can be done by selecting the "Run" option in your integrated development environment (IDE) or pressing F5, if this functionality is enabled.

To guide users through the necessary steps, the following example demonstrates the analysis of a beam.

#### Example Problem

Step 1: Define the beam spans
A span is defined as the length between two supports or where a distributed load changes. In this example, the beam has two spans:

![image](https://github.com/user-attachments/assets/80c9ee5c-d079-4475-ac33-431d91b7a8fe)

From the fixed support to where the load begins.
From the start of the load to the end of the distributed load.
The program will prompt you to specify the number of spans in the beam. In this case, select "2".

![image](https://github.com/user-attachments/assets/164c18dc-32ee-4a63-b682-561bbe40bb16)

Step 2: Span lengths
Enter the corresponding lengths for each span. For instance:

![image](https://github.com/user-attachments/assets/45029555-2041-4a49-b920-ffd5a3ef0de1)

Length of the first span: 3 meters.
Length of the second span: 3 meters.
The distributed load is 1.8 tonf/m in this example.

Step 3: Define the supports
Specify the supports for the beam. In this case, select a fixed support and a free support. The result will look like this:

![image](https://github.com/user-attachments/assets/0b64acf7-8ed8-4fce-8c43-f5b2b145c9b2)

Step 4: Enter the loads
Specify the loads applied to each span. For example: a distributed load of 1.8 tonf/m.

![image](https://github.com/user-attachments/assets/c7d702e0-2e2f-4d51-ae25-7cd160c6a58d)

Step 5: Generated results
The program will automatically generate the corresponding diagrams:

* Shear diagram:

![image](https://github.com/user-attachments/assets/f4221272-7076-49dc-8948-2ce411ef4c6a)

* Bending moment diagram:

![image](https://github.com/user-attachments/assets/033867d8-304d-41f0-aa41-4fde45521762)

### Beam design

Once the analysis is complete, the program will ask if you want to design the beam. Note that this program only designs rectangular concrete beams.

To proceed, the program will request the following additional inputs:

Names for the Excel file and AutoCAD drawing.
Information necessary for structural design.
The generated files will be saved in a folder named "Resultados" within the project directory.

### Precautions and Recommendations

1. Content of the files: The internal content of the files is not shown here as they have already been published on the author's LinkedIn page.
2. Existing files: If you plan to save a file with the same name, ensure that the existing file is closed to avoid conflicts with the operating system.
3. Unexpected errors: This program is under development and may produce unexpected errors. It is recommended to report bugs to improve the tool in future versions.
4. Free usage: This program is open-source and free to use. However, any use is at the user’s own responsibility.

![image](https://github.com/user-attachments/assets/1427d2d9-fcfd-4c7a-aa8e-9af232d2499c)

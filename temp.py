import pandas as pd
import numpy as np
from math import isnan, nan
correos_pregrado = pd.read_excel("Alumnos_Vigentes_CAM_2020.xlsx")
correos_pregrado.fillna('', inplace=True)
temp = pd.read_excel("ALUMNOS.xlsx")
for index, row in correos_pregrado.iterrows():
    a = temp.loc[(temp['Apellido Paterno'] == row['Apellido Paterno']) & (temp['Apellido Materno'] == row['Apellido Materno'])]
    if len(a) > 0:
        correos_pregrado.at[index, 'Carrera']= a['Programa'][list(a['Programa'].keys())[0]]
    if len(a) > 1:
        print("Oh noes")
print(correos_pregrado.loc[correos_pregrado['Carrera'].notna()])
print(temp)
correos_pregrado.to_excel("Alumnos_Vigentes_CAM_2020.xlsx")
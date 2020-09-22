import pandas as pd
from sys import stderr
from math import isnan

correos_pregrado = pd.read_excel("Alumnos_Vigentes_CAM_2020.xlsx")
correos_postgrado = pd.read_csv("correos_postgrado.csv")
votacion = pd.read_csv("votacion.csv")

iToGen = ['Generación 2020 Matemática','Generación 2020 Estadística', 'Generación 2019 Estadística', 'Generación 2018 Matemática', 'Generación 2017','Generación 2016', 'Postgrado']

posibles_respuestas = ['Apruebo', 'Rechazo']
n = len(votacion.columns) - 3
conteo_votos = n * [None]
for i in range(n):
    conteo_votos[i] = dict(map(lambda x: (x, 0), posibles_respuestas))
# print(conteo_votos)

otra_gente = []
total = len(correos_pregrado['mail'])
universo_votantes = dict(map(lambda x: (str(x),0), votacion['¿A qué generación perteneces?']))
votantes = dict(map(lambda x: (x, 0), universo_votantes.keys()))

for index, row in correos_pregrado.iterrows():
    for key in universo_votantes.keys():
        if str(row['Periodo Admisión'])[:-2] in '2020 Estadística':
            # print(str(row['Periodo Admisión'])[:-2],row['Carrera'], key,file=stderr)
            pass
        if str(row['Periodo Admisión'])[:-2] in key:
            #print(key,':', row['Carrera'],file=stderr)
            if str(row['Carrera']) in key:
                universo_votantes[key] += 1
                if str(row['Carrera']) == 'Estadística' and str(row['Periodo Admisión'])[:-2] in '2020 Estadística':
                    print('WTF?')
            elif str(row['Periodo Admisión'])[:-2] in "2017 2016":
                universo_votantes[key] += 1
            break
                
        

print(universo_votantes)

for index, row in votacion.iterrows():
    if str(row['¿A qué generación perteneces?']) == 'nan':
        continue
    votantes[row['¿A qué generación perteneces?']]+=1
    if row['¿A qué generación perteneces?'] == 'Postgrado':
        if row['Email Address'].lower() in correos_postgrado['mail'].values:
            for i in range(n):
                if str(row[votacion.columns[i + 3]]) == 'nan':
                    continue
                conteo_votos[i][row[votacion.columns[i+3]]] += 1
        elif row['Email Address'].lower().replace('@', "@mat.") in correos_postgrado['mail'].values:
            for i in range(n):
                if str(row[votacion.columns[i + 3]]) == 'nan':
                    continue
                conteo_votos[i][row[votacion.columns[i + 3]]] += 1
        elif row['Email Address'].lower() in correos_pregrado['mail'].values:
            for i in range(n):
                if str(row[votacion.columns[i + 3]]) == 'nan':
                    continue
                conteo_votos[i][row[votacion.columns[i + 3]]] += 1
        else:
            otra_gente.append((row['Email Address'], 'Postgrado'))
    else:
        if row['Email Address'].lower() in correos_pregrado['mail'].values:
            for i in range(n):
                if str(row[votacion.columns[i + 3]]) == 'nan':
                    continue
                conteo_votos[i][row[votacion.columns[i + 3]]] += 1
        else:
            otra_gente.append((row['Email Address'], 'Pregrado'))
print(conteo_votos)
print(list(votacion.columns)[3:])
universo_votantes["Postgrado"] = votantes["Postgrado"]
print(universo_votantes)


print("Resultado de la votación:\n")
print("Universo de Votantes: {}\n".format(total))
print("Total de votos válidamente emitidos: {} ({:.2%} del universo de votantes)\n".format(
    sum(votantes.values()), sum(votantes.values())/(total)))

for key in universo_votantes.keys():
    print("Votos válidamente emitidos {}: {} ({})".format(key, votantes[key],universo_votantes[key]))
    print(key,votantes[key],universo_votantes[key],file=stderr)
    if votantes[key] > 0.4*universo_votantes[key]:
        # Hay quorum!!!
        print("Se alcanzó el quórum, por lo tanto la votación es válida")
    else:
        # No hay quorum :c
        print("No se alcanzó el quórum, por lo tanto la votación es inválida")
    print()

for i in range(n):
    print("\nMoción: {}".format(votacion.columns[i + 3]))
    total = 0
    for resp in posibles_respuestas:
        total += conteo_votos[i][resp]
    for resp in posibles_respuestas:
        print("{}: {} ({:.2%})".format(
            resp, conteo_votos[i][resp], conteo_votos[i][resp]/(total+0.0000001)))

print("\n\nOtros: {}".format(otra_gente))
pd.set_option('display.max_columns', None)
print(correos_pregrado, file=stderr)
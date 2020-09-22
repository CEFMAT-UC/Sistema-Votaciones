import pandas as pd

correos_pregrado = pd.read_excel("Alumnos_Vigentes_CAM_2020.xlsx")
correos_postgrado = pd.read_csv("correos_postgrado.csv")
votacion = pd.read_csv("votacion.csv")

posibles_respuestas = ['Apruebo', 'Rechazo', 'Abstengo']
n = len(votacion.columns) - 3
conteo_votos = n * [None]
for i in range(n):
    conteo_votos[i] = dict(map(lambda x: (x, 0), posibles_respuestas))


otra_gente = []
total = len(correos_pregrado['mail'])

pregrado = 0
postgrado = 0


for index, row in votacion.iterrows():
    if row['Email Address'].lower() in correos_postgrado['mail'].values:
        postgrado += 1
        for i in range(n):
            conteo_votos[i][row[votacion.columns[i+3]]] += 1
    elif row['Email Address'].lower().replace('@', "@mat.") in correos_postgrado['mail'].values:
        postgrado += 1
        for i in range(n):
            conteo_votos[i][row[votacion.columns[i + 3]]] += 1
    elif row['Email Address'].lower() in correos_pregrado['mail'].values:
        pregrado += 1
        for i in range(n):
            conteo_votos[i][row[votacion.columns[i + 3]]] += 1
    else:
        otra_gente.append((row['Email Address'], 'Algún lugar?'))

total += postgrado

print("Resultado de la votación:\n")
print("Universo de Votantes: {}\n".format(total))
print("Total de votos válidamente emitidos: {} ({:.2%} del universo de votantes)\n".format(
    pregrado+postgrado, (pregrado+postgrado)/(total)))

print("Votos Pregrado: {}".format(pregrado))
print("Votos Postgrado: {}\n".format(postgrado))

if (pregrado + postgrado)*10 > 4*total:
    # Hay quorum!!!
    print("Se alcanzó el quórum, por lo tanto la votación es válida")
else:
    # No hay quorum :c
    print("No se alcanzó el quórum, por lo tanto la votación es inválida")

for i in range(n):
    print("\nMoción: {}".format(votacion.columns[i + 3]))
    for resp in posibles_respuestas:
        print("{}: {} ({:.2%}) ({:.2%})".format(
            resp, conteo_votos[i][resp], conteo_votos[i][resp]/(pregrado+postgrado), conteo_votos[i][resp]/total))


print("\n\nOtros: {}".format(otra_gente))

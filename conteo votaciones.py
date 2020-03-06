archivo_correos_pregrado = open("correos_pregrado.csv")
lineas = archivo_correos_pregrado.readlines()
correos_pregrado = {}
for linea in lineas:
    linea_normal = linea.strip().split(";")     # Los correos deben venir en un csv, separados
    for correo in linea_normal:                 # por ";" y debe ser una única linea (fila)
        correos_pregrado[correo] = 0
        
archivo_correos_pregrado.close()

archivo_correos_postgrado = open("correos_postgrado.csv")
lineas = archivo_correos_postgrado.readlines()
correos_postgrado = {}
for linea in lineas:
    linea_normal = linea.strip().split(";")     # Los correos deben venir en un csv, separados
    for correo in linea_normal:                 # por ";" y debe ser una única linea (fila)
        correos_postgrado[correo] = 0
        
archivo_correos_postgrado.close()

apruebo = 0
rechazo = 0
abstengo = 0
pregrado = 0
postgrado = 0
comentarios = []
otra_gente = []



archivo_votacion = open("votacion_revalidacionparo5.csv")      # Aqui va el excel del formulario google (guardado como csv)
lineas = archivo_votacion.readlines()
for i in range(1, len(lineas)):         # La primera linea es de headers, y las columnas deben ser (en orden): marca temporal, correo, programa, apruebo/rechazo, comentarios
    linea_normal = lineas[i].strip().split(";")
    if (linea_normal[1] in correos_pregrado and linea_normal[2] == "Pregrado" and correos_pregrado[linea_normal[1]] == 0) or \
        (linea_normal[1] in correos_postgrado and linea_normal[2] == "Postgrado" and correos_postgrado[linea_normal[1]] == 0) or \
        (linea_normal[2] == "Postgrado" and linea_normal[1] not in correos_postgrado and (linea_normal[1].split("@")[0]+"@mat.uc.cl" in correos_postgrado and \
        correos_postgrado[linea_normal[1].split("@")[0]+"@mat.uc.cl"] == 0) or (linea_normal[1].split("@")[0]+"@uc.cl" in correos_postgrado and \
        correos_postgrado[linea_normal[1].split("@")[0]+"@uc.cl"] == 0)):
        if linea_normal[2] == "Pregrado":       # Solo se considera pregrado y postgrado (y no gente de fuera)
            pregrado += 1
            correos_pregrado[linea_normal[1]] += 1
        else:
            postgrado += 1
            if linea_normal[1].split("@")[0]+"@mat.uc.cl" in correos_postgrado:     # Esto es porque algunos de postgrado votan con su correo de pregrado
                correos_postgrado[linea_normal[1].split("@")[0]+"@mat.uc.cl"] += 1
            else:
                correos_postgrado[linea_normal[1].split("@")[0]+"@uc.cl"] += 1
            
        if linea_normal[3] == "Apruebo":        # Solo se considera apruebo, rechazo y abstengo
            apruebo += 1
        elif linea_normal[3] == "Rechazo":
            rechazo += 1
        else:
            abstengo += 1

        if linea_normal[5] != "":               # Solo se consideran los comentarios si de
            comentarios.append(linea_normal[5]) # de verdad escribieron algo

    else:
        otra_gente.append([linea_normal[1],linea_normal[2]])

archivo_votacion.close()

print("")
print("Resultados de las votaciones:")
print("")
print("Universo de votantes: "+str(len(correos_pregrado)+postgrado))
print("Total de votos válidamente emitidos: "+str(pregrado + postgrado)+" ("+str('%.2f'%(100*(pregrado+postgrado)/(len(correos_pregrado)+postgrado))+"% del universo de votantes)"))
if (pregrado+postgrado)/(len(correos_pregrado)+postgrado) > 0.4:
    print("Se alcanzó el quórum, por lo tanto la votación es válida")
else:
    print("No se alcanzó el quórum, por lo tanto la votación es inválida")
print("")
print("Apruebo: "+str(apruebo)+" ("+str('%.2f'%(100*apruebo/(pregrado+postgrado))+"%)"))
print("Rechazo: "+str(rechazo)+" ("+str('%.2f'%(100*rechazo/(pregrado+postgrado))+"%)"))
print("Abstengo: "+str(abstengo)+" ("+str('%.2f'%(100*abstengo/(pregrado+postgrado))+"%)"))
print("")
print("Pregrado: "+str(pregrado)+" ("+str('%.2f'%(100*pregrado/(pregrado+postgrado))+"%)"))
print("Postgrado: "+str(postgrado)+" ("+str('%.2f'%(100*postgrado/(pregrado+postgrado))+"%)"))
print("")
print("")
print("Otros: ")
print(otra_gente)
input()
input()

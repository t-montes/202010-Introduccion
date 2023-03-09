
import covinfobogota_module as mod
from flask import Flask, render_template

#Definición de funciones.
def reescribir_datos_por_texto_pastel(nombre_archivo: str, texto_sobreescritura: str, diccionario_casos: dict) -> None:
    #Abrir archivo y guardar datos
    with open(nombre_archivo,'r') as file:
        data = file.readlines()
        
    #Completar el diccionario con la información de la página.
    diccionario = {}
    index = 0
    
    for i in diccionario_casos:
        diccionario[i] = [len(diccionario_casos[i])]
        diccionario[i].append(colors_pastel[index])
        if index < len(colors_pastel) - 1:
            index += 1
        else:
            index = 0    
    
    #Definir linea a sobreescribir en el html.
    linea = 'var valores={'
    for i in diccionario:
        linea += f"'{i}':"+"{valor:"+ f"{diccionario[i][0]}, color:'"+ f"{diccionario[i][1]}'" + "},"

    linea = linea[:-1]
    linea += ' }\n'
        
    #Sobreescribir linea.
    linea_sobreescritura = -1
    for i in range(len(data)):
        if data[i].rstrip() == texto_sobreescritura.rstrip():
            linea_sobreescritura = i + 2
    linea_sobreescritura = 180 if linea_sobreescritura == -1 else linea_sobreescritura
    data[linea_sobreescritura] = linea

    #Añadir valor al archivo html.
    with open(nombre_archivo,'w') as file:
        data = file.writelines(data)

def reescribir_datos_por_texto_barra(nombre_archivo: str, texto_sobreescritura: str, diccionario_casos: dict) -> None:
    #Abrir archivo y guardar datos
    with open(nombre_archivo,'r') as file:
        data = file.readlines()
        
    #Completar el diccionario con la información de la página.
    diccionario = {}
    index = 0
    
    for i in diccionario_casos:
        diccionario[i] = [len(diccionario_casos[i])]
        diccionario[i].append(colors_barra[index])
        if index < len(colors_barra) - 1:
            index += 1
        else:
            index = 0    
    
    #Definir linea a sobreescribir en el html.
    linea1 = 'var MisNiveles={'
    for i in diccionario:
        if type(i) is str:
            k = i.title()
        else:
            k = i
        linea1 += f"'{k}':{diccionario[i][0]},"
    linea1 = linea1[:-1]
    linea1 += ' };\n'

    linea2 = 'var MisColores=['
    for i in diccionario:
        linea2 += f"'#{diccionario[i][1]}',"
    linea2 = linea2[:-1]
    linea2 += ' ];\n'

    #Sobreescribir linea.
    linea_sobreescritura = -1
    for i in range(len(data)):
        if data[i].rstrip() == texto_sobreescritura.rstrip():
            linea_sobreescritura = i + 2
            
    data[linea_sobreescritura] = linea1
    data[linea_sobreescritura + 1] = linea2 

    #Añadir valor al archivo html.
    with open(nombre_archivo,'w') as file:
        data = file.writelines(data)


#Lista de colores:
colors_pastel = ['red', 'Cyan', 'deeppink', 'skyblue', 'Orange', 'pink', 'lavender', 'gray', 'lime', 'magenta',
    'blue', 'tan', 'cornsilk', 'mediumslateblue', 'powderblue', 'cadetblue',
    'aquamarine', 'olive', 'yellowgreen', 'lightgreen', 'indigo', 'plum', 'moccasin', 'gold', 'coral']

colors_barra = ["67b6c7","a55ca5","bccd7a","eb9743", "a58787", "a53939","72d54c","1a0a61","ec27ef",
    "ef275f", "27efca", "90b497", "0a6958", "a8a01c", "85630a", "2e3667", "ff75bd", "ca0505","53002b", "ccdc08",
    "52baee", "9a9a9a", "d57d7d", "0f3428", "cf00a2","340f0f", "ff5050", "bbff29", "baf9e8", "96ad64",
    "06ff00", "564040", "f67e7e", "7243e9", "43e996", "ff00e9", "628985", "ce98c9", "1c3936", "ee923b", "b59679"]

#ACTUALIZACIÓN DE DATOS SEGÚN ARCHIVO CSV
def actualizar() -> None:
    #home
    #Definición de variables.

    cyf = mod.casos_y_fecha('../OSB_EnfTransm-COVID-19', 'csv', ';', 4)
    cases = mod.quitar_caracteres_especiales(cyf[0])
    last_date = cyf[1]

    nom = 'templates/home.html'
    ccrf = mod.cases_c_r_f(cases)
    #Abrir Archivo.
    with open(nom, 'r') as file:
        data = file.readlines()
    #Cambiar Datos.
    data[14] = f'<FONT FACE="Arial" SIZE=20 COLOR="blue">{ccrf["confirmado"]}</FONT>\n'
    data[16] = f'<FONT FACE="Arial" SIZE=15 COLOR="green">{ccrf["recuperado"]}</FONT>\n'
    data[18] = f'<FONT FACE="Arial" SIZE=15 COLOR="red">{ccrf["fallecido"]}</FONT>\n'
    data[20] = f'<p class="lead">La fecha de corte es: {last_date}</p>\n'
    #Sobreescribir archivo.
    with open(nom,'w') as file:
        data = file.writelines(data)

    #fecha
    #Definición de variables.
    file_name = 'fecha.html'
    folder_name = 'templates'
    #Sobreescribir datos.
    c_pd = mod.cases_per_date(cases)
    reescribir_datos_por_texto_barra(f'{folder_name}/{file_name}', '// definimos los valores de nuestra grÃ¡fica', c_pd)

    #localidad
    #Definición de variables.
    file_name = 'localidad.html'
    folder_name = 'templates'
    #Sobreescribir datos.
    c_pl = mod.cases_per_locality(cases)
    reescribir_datos_por_texto_barra(f'{folder_name}/{file_name}', '// definimos los valores de nuestra grÃ¡fica', c_pl)

    #CADA LOCALIDAD
    folder_name = 'templates/locs'
    for i in c_pl:
        file_name = f'{i.title()}.html'
        with open(f'{folder_name}/{file_name}', 'r') as file:
            data = file.readlines()
        #Cambiar Datos.
        data[22] = f'<h1 style="text-align:center;">{len(mod.cases_per_sex(c_pl[i])["f"])}</h1>\n'
        data[28] = f'<h1 style="text-align:center;">{len(mod.cases_per_sex(c_pl[i])["m"])}</h1>\n'
        #Sobreescribir archivo.
        with open(f'{folder_name}/{file_name}','w') as file:
            data = file.writelines(data)
        reescribir_datos_por_texto_barra(f'{folder_name}/{file_name}', '// definimos los valores de nuestra grÃ¡fica', mod.cases_per_ubication(c_pl[i]))


    #edad
    #Definición de variables.
    file_name = 'edad.html'
    folder_name = 'templates'
    #Obtención de casos
    c_par = mod.cases_per_age_range(cases)
    reescribir_datos_por_texto_barra(f'{folder_name}/{file_name}', '// definimos los valores de nuestra grÃ¡fica', c_par)

    #edad2
    #Definición de variables.
    file_name = 'edad2.html'
    folder_name = 'templates'
    #Obtención de casos
    c_pa = mod.cases_per_age(cases)
    reescribir_datos_por_texto_barra(f'{folder_name}/{file_name}', '// definimos los valores de nuestra grÃ¡fica', c_pa)

    #genero
    #Definición de variables.
    nom = 'templates/genero.html'
    #Obtención de casos
    c_pg = mod.cases_per_sex(cases)
    #Abrir Archivo.
    with open(nom, 'r') as file:
        data = file.readlines()
    #Cambiar Datos.
    data[17] = f'<h1>{len(c_pg["f"])}</h1>\n'
    data[23] = f'<h1>{len(c_pg["m"])}</h1>\n'
    #Sobreescribir archivo.
    with open(nom,'w') as file:
        data = file.writelines(data)
    
    #tipo_de_caso
    #Definición de variables.
    file_name = 'tipo_de_caso.html'
    folder_name = 'templates'
    #Obtención de casos.
    c_ptoc = mod.cases_per_type_of_case(cases)
    reescribir_datos_por_texto_barra(f'{folder_name}/{file_name}', '// definimos los valores de nuestra grÃ¡fica', c_ptoc)

    #ubicacion_actual
    #Definición de variables.
    file_name = 'ubicacion_actual.html'
    folder_name = 'templates'
    #Obtención de casos
    c_pu = mod.cases_per_ubication(cases) 
    reescribir_datos_por_texto_barra(f'{folder_name}/{file_name}', '// definimos los valores de nuestra grÃ¡fica', c_pu)

    #estado_actual
    #Definición de variables.
    file_name = 'estado_actual.html'
    folder_name = 'templates'
    #Obtención de casos
    c_ps = mod.cases_per_state(cases)    
    reescribir_datos_por_texto_barra(f'{folder_name}/{file_name}', '// definimos los valores de nuestra grÃ¡fica', c_ps)

#Main App Web.

#actualizar()
#Marcar como comentario la línea de arriba al subir a Heroku. 

app = Flask(__name__)

@app.route('/')
def home():
    #Retornar.
    return render_template('home.html')

@app.route('/fecha')
def casos_por_fecha():
    #Retornar.
    return render_template('fecha.html')

@app.route('/edad')
def casos_por_edad():
    #Retornar
    return render_template('edad.html')

@app.route('/edad2')
def casos_por_edad2():
    #Retornar
    return render_template('edad2.html')

@app.route('/genero')
def casos_por_genero():
    #Retornar
    return render_template('genero.html')

@app.route('/tipo_de_caso')
def casos_por_tipo_de_caso():
    #Retornar
    return render_template('tipo_de_caso.html')

@app.route('/ubicacion_actual')
def casos_por_ubicacion_actual():
    #Retornar
    return render_template('ubicacion_actual.html')

@app.route('/estado_actual')
def casos_por_estado_actual():
    #Retornar
    return render_template('estado_actual.html')

@app.route('/localidad')
def casos_por_localidad():
    #Retornar.
    return render_template('localidad.html')

@app.route('/localidad_Kennedy')
def casos_por_localidad_Kennedy():
    #Retornar.
    return render_template('locs/Kennedy.html')

@app.route('/localidad_Suba')
def casos_por_localidad_Suba():
    #Retornar.
    return render_template('locs/Suba.html')

@app.route('/localidad_Bosa')
def casos_por_localidad_Bosa():
    #Retornar.
    return render_template('locs/Bosa.html')

@app.route('/localidad_Engativa')
def casos_por_localidad_Engativa():
    #Retornar.
    return render_template('locs/Engativa.html')

@app.route('/localidad_Ciudad Bolivar')
def casos_por_localidad_Ciudad_Bolivar():
    #Retornar.
    return render_template('locs/Ciudad Bolivar.html')

@app.route('/localidad_Usaquen')
def casos_por_localidad_Usaquen():
    #Retornar.
    return render_template('locs/Usaquen.html')

@app.route('/localidad_Fontibon')
def casos_por_localidad_Fontibon():
    #Retornar.
    return render_template('locs/Fontibon.html')

@app.route('/localidad_Rafael Uribe Uribe')
def casos_por_localidad_Rafael_Uribe_Uribe():
    #Retornar.
    return render_template('locs/Rafael Uribe Uribe.html')

@app.route('/localidad_San Cristobal')
def casos_por_localidad_San_Cristobal():
    #Retornar.
    return render_template('locs/San Cristobal.html')

@app.route('/localidad_Puente Aranda')
def casos_por_localidad_Puente_Aranda():
    #Retornar.
    return render_template('locs/Puente Aranda.html')

@app.route('/localidad_Usme')
def casos_por_localidad_Usme():
    #Retornar.
    return render_template('locs/Usme.html')

@app.route('/localidad_Chapinero')
def casos_por_localidad_Chapinero():
    #Retornar.
    return render_template('locs/Chapinero.html')

@app.route('/localidad_Teusaquillo')
def casos_por_localidad_Teusaquillo():
    #Retornar.
    return render_template('locs/Teusaquillo.html')

@app.route('/localidad_Tunjuelito')
def casos_por_localidad_Tunjuelito():
    #Retornar.
    return render_template('locs/Tunjuelito.html')

@app.route('/localidad_Antonio Narino')
def casos_por_localidad_Antonio_Narino():
    #Retornar.
    return render_template('locs/Antonio Narino.html')

@app.route('/localidad_Santa Fe')
def casos_por_localidad_Santa_Fe():
    #Retornar.
    return render_template('locs/Santa Fe.html')

@app.route('/localidad_Los Martires')
def casos_por_localidad_Los_Martires():
    #Retornar.
    return render_template('locs/Los Martires.html')

@app.route('/localidad_Barrios Unidos')
def casos_por_localidad_Barrios_Unidos():
    #Retornar.
    return render_template('locs/Barrios Unidos.html')

@app.route('/localidad_La Candelaria')
def casos_por_localidad_La_Candelaria():
    #Retornar.
    return render_template('locs/La Candelaria.html')

@app.route('/localidad_Sumapaz')
def casos_por_localidad_Sumapaz():
    #Retornar.
    return render_template('locs/Sumapaz.html')

@app.route('/localidad_Fuera De Bogota')
def casos_por_localidad_Fuera_De_Bogota():
    #Retornar.
    return render_template('locs/Fuera De Bogota.html')

@app.route('/localidad_Sin Dato')
def casos_por_localidad_Sin_Dato():
    #Retornar.
    return render_template('locs/Sin Dato.html')

if __name__ == '__main__':
    app.run(debug=True)

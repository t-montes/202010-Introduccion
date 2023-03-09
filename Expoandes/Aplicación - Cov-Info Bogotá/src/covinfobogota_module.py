"""FUNCIONES RECURRENTES"""
def converse_month_to_num(mes: str) -> str:
    if mes.lower() == 'enero':
        return '01'
    elif mes.lower() == 'febrero':
        return '02'
    elif mes.lower() == 'marzo':
        return '03'
    elif mes.lower() == 'abril':
        return '04'
    elif mes.lower() == 'mayo':
        return '05'
    elif mes.lower() == 'junio':
        return '06'
    elif mes.lower() == 'julio':
        return '07'
    elif mes.lower() == 'agosto':
        return '08'
    elif mes.lower() == 'septiembre':
        return '09'
    elif mes.lower() == 'octubre':
        return '10'
    elif mes.lower() == 'noviembre':
        return '11'
    elif mes.lower() == 'diciembre':
        return '12'
    else:
        return '-1'

def caracteres_especiales_html(elemento) -> list:
    """
    Retorna la lista de diccionarios dada por parámetro con todas las tildes y virgulillas reemplazadas a código html.
    """
    c_e = {
            'á':'&aacute',
            'é':'&eacute',
            'í':'&iacute',
            'ó':'&oacute',
            'ú':'&uacute',
            'ñ':'&ntilde',
            'Á':'&Aacute',
            'É':'&Eacute',
            'Í':'&Iacute',
            'Ó':'&Oacute',
            'Ú':'&Uacute',
            'Ñ':'&Ntilde',
            }
    if type(elemento) is list:
        #Casos.
        nuevo_cases = []
        for i in elemento:
            nuevo_dict = {}
            k_dc = list(i.keys())
            v_dc = list(i.values())
            for j in range(len(i)):
                for char in c_e:
                    if type(k_dc[j]) is str:
                        k_dc[j] = k_dc[j].replace(char, c_e[char])
                    if type(v_dc[j]) is str:
                        v_dc[j] = v_dc[j].replace(char, c_e[char])
            for j in range(len(i)):
                nuevo_dict[k_dc[j]] = v_dc[j]
            nuevo_cases.append(nuevo_dict)
        return nuevo_cases
    
    if type(elemento) is str:
        for char in c_e:
            elemento = elemento.replace(char,c_e[char])
        return elemento

def quitar_caracteres_especiales(elemento) -> list:
    """
    Si el tipo del elemento es una lista:
        Retorna la lista de diccionarios dada por parámetro sin tildes ni virgulillas.
    Si ek tipo es un str:
        Se retorna el str sin tildes ni virgulillas.
    """
    c_e = {
            'á':'a',
            'é':'e',
            'í':'i',
            'ó':'o',
            'ú':'u',
            'ñ':'n',
            'Á':'A',
            'É':'E',
            'Í':'I',
            'Ó':'O',
            'Ú':'U',
            'Ñ':'N',
            }
    if type(elemento) is list:
        #Casos.
        nuevo_cases = []
        for i in elemento:
            nuevo_dict = {}
            k_dc = list(i.keys())
            v_dc = list(i.values())
            for j in range(len(i)):
                for char in c_e:
                    if type(k_dc[j]) is str:
                        k_dc[j] = k_dc[j].replace(char, c_e[char])
                    if type(v_dc[j]) is str:
                        v_dc[j] = v_dc[j].replace(char, c_e[char])
            for j in range(len(i)):
                nuevo_dict[k_dc[j]] = v_dc[j]
            nuevo_cases.append(nuevo_dict)
        return nuevo_cases
    
    if type(elemento) is str:
        for char in c_e:
            elemento = elemento.replace(char,c_e[char])
        return elemento
    
"""FIN FUNCIONES RECURRENTES"""

def casos_y_fecha(file_name: str, file_type: str, separator: str, key_line_num: int) -> tuple:
    """
    Retorna una tupla de dos elementos:
    1. list of dict -> casos.
    2. str -> última fecha de reporte, separada por '/'.
    """
    #Lineas.
    file = open(f'{file_name}.{file_type}', 'r')
    lines = file.readlines()
    file.close()
    
    for i in range(len(lines)):
        lines[i] = lines[i].rstrip().split(separator)

    #Casos y llaves.
    keys = lines[key_line_num]
    cases = []
    for i in range(key_line_num + 1, len(lines)):
        each_case = {}
        if lines[i][0] == '':
            break
        for j in range(len(keys)):
            if lines[i][j].isdigit():
                each_case[keys[j].lower()] = int(lines[i][j])
            else:
                b = ''
                x = 0
                cont = 0
                while 1:
                    if lines[i][j][len(lines[i][j]) - cont - 1] == ' ':
                        x += 1
                        b = lines[i][j][:-x]
                    else:
                        b = lines[i][j] if b == '' else b
                        break
                    cont+= 1
                each_case[keys[j].lower().rstrip()] = lines[i][j].lower().rstrip()
        cases.append(each_case)
    
    #Fecha de reporte.
    for i in range(len(cases) + key_line_num + 1, len(lines)):
        if lines[i][0] != '':
            last_date = lines[i][0][lines[i][0].find('Corte') + 7:-1].split()
    if int(last_date[1]) < 10:
        last_date[1] = f'0{last_date[1]}'
    last_date = f'{last_date[1]}/{converse_month_to_num(last_date[0])}/{last_date[3]}'
    
    return (cases, last_date)

"""FUNCIONES DE CASOS SEGÚN PROPIEDADES"""

def cases_c_r_f(cases: list) -> dict:

    ccrf = {'confirmado':0, 'recuperado':0, 'fallecido':0}
    for i in cases:
        if i['estado'] == 'recuperado':
            ccrf['recuperado'] += 1
        elif i['estado'] == 'fallecido':
            ccrf['fallecido'] += 1
        ccrf['confirmado'] += 1
    return ccrf

def cases_per(cases: list, key:str) -> dict:
    """
    Retorna el diccionario de casos según el parámetro especificado (key).
    Dicho diccionario es retornado en orden de mayor número de casos a menor.
    """
    copy_cases = cases.copy()
    dic_num = {}
    for i in copy_cases:
        dic_num[i[key]] = dic_num.get(i[key], 0) + 1
    
    c_pl = {}    
    for i in range(len(dic_num)):
        mayor = 0
        loc = ''
        for j in dic_num:
            if dic_num[j] > mayor:
                mayor = dic_num[j]
                loc = j
        del dic_num[loc]
        c_pl[loc] = []
    
    for i in cases:
        c_pl[i[key]].append(i)
    return c_pl

def cases_per_age(cases: list) -> dict:
    key = 'edad'
    c_pa = cases_per(cases, key)
    return c_pa

def cases_per_age_range(cases: list) -> dict:
    key = 'edad'
    c_par = {'0 a 9':[], '10 a 19':[], '20 a 29':[], '30 a 39':[], '40 a 49':[], '50 a 59':[],
             '60 a 69':[], '70 a 79':[], '80 a 89':[], '90 a 99':[], '100 o mas':[]}
    for i in cases:
        if i[key] < 10:
            c_par['0 a 9'].append(i)
        elif i[key] < 20:
            c_par['10 a 19'].append(i)
        elif i[key] < 30:
            c_par['20 a 29'].append(i)
        elif i[key] < 40:
            c_par['30 a 39'].append(i)
        elif i[key] < 50:
            c_par['40 a 49'].append(i)
        elif i[key] < 60:
            c_par['50 a 59'].append(i)
        elif i[key] < 70:
            c_par['60 a 69'].append(i)
        elif i[key] < 80:
            c_par['70 a 79'].append(i)
        elif i[key] < 90:
            c_par['80 a 89'].append(i)
        elif i[key] < 100:
            c_par['90 a 99'].append(i)
        else:
            c_par['100 o mas'].append(i)
    
    return c_par

def cases_per_date(cases: list) -> dict:
    key = 'fecha de diagnóstico'
    key_2 = 'fecha de diagn&oacutestico'
    key_3 = 'fecha de diagnostico'
    c_pd = {}
    for i in cases:
        try:
            c_pd[i[key]] = c_pd.get(i[key], [])
            c_pd[i[key]].append(i)
        except:
            try:
                c_pd[i[key_2]] = c_pd.get(i[key_2], [])
                c_pd[i[key_2]].append(i)
            except:
                c_pd[i[key_3]] = c_pd.get(i[key_3], [])
                c_pd[i[key_3]].append(i)
    
    new_cpd_keys = []
    cont_d = 1
    cont_m = 1
    cont_a = 2020
    while 1:
        cont_m_str = '0' + str(cont_m) if cont_m < 10 else str(cont_m)
        new_cpd_keys.append(f'{cont_d}/{cont_m_str}/{cont_a}')
        if cont_m == 1:
            if cont_d == 31:
                cont_m += 1
                cont_d = 1
            else:
                cont_d += 1
        elif cont_m == 2:
            if cont_d == 29:
                cont_m += 1
                cont_d = 1
            else:
                cont_d += 1
        elif cont_m == 3:
            if cont_d == 31:
                cont_m += 1
                cont_d = 1
            else:
                cont_d += 1
        elif cont_m == 4:
            if cont_d == 30:
                cont_m += 1
                cont_d = 1
            else:
                cont_d += 1
        elif cont_m == 5:
            if cont_d == 31:
                cont_m += 1
                cont_d = 1
            else:
                cont_d += 1
        elif cont_m == 6:
            if cont_d == 30:
                cont_m += 1
                cont_d = 1
            else:
                cont_d += 1
        elif cont_m == 7:
            if cont_d == 31:
                cont_m += 1
                cont_d = 1
            else:
                cont_d += 1
        elif cont_m == 8:
            if cont_d == 31:
                cont_m += 1
                cont_d = 1
            else:
                cont_d += 1
        elif cont_m == 9:
            if cont_d == 30:
                cont_m += 1
                cont_d = 1
            else:
                cont_d += 1
        elif cont_m == 10:
            if cont_d == 31:
                cont_m += 1
                cont_d = 1
            else:
                cont_d += 1
        elif cont_m == 11:
            if cont_d == 30:
                cont_m += 1
                cont_d = 1
            else:
                cont_d += 1
        elif cont_m == 12:
            if cont_d == 31:
                break
            else:
                cont_d += 1
    final_cpd = {}
    for i in new_cpd_keys:
        if i in c_pd:
            final_cpd[i] = c_pd[i]
    
    return final_cpd

def cases_per_locality(cases: list) -> dict:
    key = 'localidad de residencia'
    c_pl = cases_per(cases, key)
    return c_pl

def cases_per_sex(cases: list) -> dict:
    key = 'sexo'
    c_pg = cases_per(cases, key)
    return c_pg

def cases_per_type_of_case(cases: list) -> dict:
    key = 'tipo de caso'
    c_ptoc = cases_per(cases, key)
    return c_ptoc

def cases_per_ubication(cases: list) -> dict:
    key = 'ubicación'
    key_2 = 'ubicaci&oacuten'
    key_3 = 'ubicacion'
    try:
        c_pu = cases_per(cases, key)
    except:
        try:
            c_pu = cases_per(cases, key_2)
        except:
            c_pu = cases_per(cases, key_3)
            
    return c_pu

def cases_per_state(cases: list) -> dict:
    key = 'estado'
    c_ps = cases_per(cases, key)
    return c_ps

"""FIN FUNCIONES DE CASOS SEGÚN PROPIEDADES"""

cases = casos_y_fecha('../OSB_EnfTransm-COVID-19', 'csv', ';', 4)[0]
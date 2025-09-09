import os
import pandas as pd
import pdfplumber
import requests
#-----------------

## Obtener ODM provisorio (con nombres separados de apellidos)
"""(Solo necesito las columnas DNI, Nombre, Apellido. 
Para que a partir del nombre habia hecho el join con ns_def.csv 
donde le asigno el sexo segun el nombre. Esto es asi porque luego 
en el orden definitivo, pusieron Apellido y Nombre junto, 
siendo dificil y quizas imposible separar los nombres compuestos 
y apellidos compuestos para poder obtener solo los nombres y asi estimar 
si es Femenino o Masculino)
"""
def obtener_odm_provisorio(url_pdf: str, nombre_archivo: str = "odm_provisorio.pdf") -> pd.DataFrame:
    """
    Descarga, extrae y limpia datos de un PDF en un DataFrame listo para análisis.
    Args: url_pdf (str): URL del archivo PDF a descargar.
          nombre_archivo (str): Nombre con que se guardará el PDF localmente.
    Returns:  pd.DataFrame: DataFrame
    """
    # Descargar PDF si no existe localmente
    if not os.path.isfile(nombre_archivo):
        r = requests.get(url_pdf)
        if r.status_code == 200:
            with open(nombre_archivo, "wb") as f:
                f.write(r.content)
        else:
            print(f"Error downloading PDF from {url_pdf}. Status code: {r.status_code}")
            return None

    # Extraer tablas del PDF
    data = []
    try:
        with pdfplumber.open(nombre_archivo) as pdf:
            for page in pdf.pages:
                table = page.extract_table()
                if table:
                    data.extend(table)
    except Exception as e:
        print(f"Error opening or reading PDF file {nombre_archivo}: {e}")
        return None

    dfodmp = pd.DataFrame(data[1:], columns=data[1])
    dfodmp.columns = dfodmp.columns.str.replace("\n", " ", regex=True)
    rename_dict = {
        "Número de documento": "DNI",
        "Apellido": "APELLIDO",
        "Nombre": "NOMBRE" }
    dfodmp = dfodmp.rename(columns=rename_dict)
    dfodmp['DNI'] = dfodmp['DNI'].astype(str)
    
    return dfodmp

## Obtener ODM definitivo
def obtener_ODM2025(url_pdf: str, nombre_archivo: str = "ODM2025.pdf") -> pd.DataFrame:
    """
    Descarga, extrae y limpia datos de un PDF en un DataFrame listo para análisis.
    Args: url_pdf (str): URL del archivo PDF a descargar.
          nombre_archivo (str): Nombre con que se guardará el PDF localmente.
    Returns:  pd.DataFrame: DataFrame
    """
    # Descargar PDF si no existe localmente
    if not os.path.isfile(nombre_archivo):
        r = requests.get(url_pdf)
        if r.status_code == 200:
            with open(nombre_archivo, "wb") as f:
                f.write(r.content)
        else:
            print(f"Error downloading PDF from {url_pdf}. Status code: {r.status_code}")
            return None

    # Extraer tablas del PDF
    data = []
    try:
        with pdfplumber.open(nombre_archivo) as pdf:
            for page in pdf.pages:
                table = page.extract_table()
                if table:
                    data.extend(table)
    except Exception as e:
        print(f"Error opening or reading PDF file {nombre_archivo}: {e}")
        return None

    dfODM2025 = pd.DataFrame(data[1:], columns=data[1])
    dfODM2025.columns = dfODM2025.columns.str.replace("\n", " ", regex=True)
    columnas_a_eliminar = ['Apellido y Nombre']
    dfODM2025.drop(columns=columnas_a_eliminar, inplace=True)

    return dfODM2025
#-----------------

## Join odm (Nombre, Apellido) con ODM, a partir del DNI
def mergeODFS (df1, df2):
  # df1 con columnas: DNI, NOMBRE, APELLIDO (dfodm)
  # df2 con columnas incluyendo DNI, PUNTAJE_CRUDO, ODM_CRUDO, PROMEDIO, ESPECIALIDAD (dfODM2025)
  # Hacer merge con df1 para traer NOMBRE y APELLIDO
  df = df2.merge(df1[['DNI', 'NOMBRE', 'APELLIDO']], on='DNI', how='left')

  faltantes = pd.DataFrame([
    {"DNI": "41459766", "NOMBRE": "Valentina", "APELLIDO": "Basiglio Godoy",
     "Institución formadora": "UNIVERSIDAD NACIONAL DE LA MATANZA",
        "Promedio": 6.39,
        "Fecha de Expedición de Título": "20-02-2025",
        "Especialidad": "Terapia intensiva",
        "Puntaje obtenido en el examen": 73,
        "Tipo Uni": "N",
        "Componente": 5,
        "Puntaje Final": 47.89, "ODM": 17},
    {"DNI": "33004858", "NOMBRE": "José Luis", "APELLIDO": "Rodriguez",
     "Institución formadora": "UNIVERSIDAD NACIONAL ARTURO JAURETCHE",
        "Promedio": 7.18,
        "Fecha de Expedición de Título": "20-03-2025",
        "Especialidad": "Anestesiología",
        "Puntaje obtenido en el examen": 66,
        "Tipo Uni": "N",
        "Componente": "5",
        "Puntaje Final": 45.18, "ODM": 421}])
  df = pd.concat([df, faltantes], ignore_index=True)

  return df
#-----------------

## Limpiar el df
def limpiar_df(df):

    # Renombrar columnas
    rename_dict = {
        "Institución formadora": "UNIVERSIDAD",
        "Promedio": "PROMEDIO_CARRERA",
        "Apellido": "APELLIDO",
        "Nombre": "NOMBRE",
        "Fecha de Expedición de Título": "FECHA_TITULO",
        "Especialidad": "ESPECIALIDAD",
        "Puntaje obtenido en el examen": "NOTA_EXAMEN",
        "Tipo Uni": "TIPO_UNI",
        "Componente": "COMPONENTE",
        "Puntaje Final": "PUNTAJE"
    }
    df = df.rename(columns=rename_dict)

    # Eliminar filas no deseadas
    df = df[~df.isin(["DNI"]).any(axis=1)] # filas donde se repite el encabezado
    df = df[df['DNI'].str.strip().astype(bool)]  # elimina filas vacías (con la celda de apellido vacio)
    df = df.dropna().reset_index(drop=True) # reindexar

    # Reemplazos globales en todas las celdas
    df = df.replace({r'\n': ' ', "En trámite": "30-06-2025"}, regex=True) #crear el espacio entre los nombres en vez de "\n" y poner la fecha que elegi 30 junio 2025 en vez de "en tramite"
    # Tiempo entre recibido y el examen (1 julio 2025)
    # Definir la fecha cero
    fecha_cero = pd.to_datetime("2025-07-01")

    # Ajustes de formato
    df["FECHA_TITULO"] = pd.to_datetime(df["FECHA_TITULO"], format="%d-%m-%Y", errors="coerce")

    # Floats
    cols_f = ["PROMEDIO_CARRERA", "PUNTAJE"]
    df[cols_f] = df[cols_f].replace(",", ".", regex=True).replace("", float('nan')).astype(float)
    # Enteros
    cols_i = ['NOTA_EXAMEN', 'COMPONENTE', 'ODM']
    for col in cols_i:
        df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")

    df["COMPONENTE"] = df["COMPONENTE"].fillna(0)

    df['PUNTAJE_CRUDO'] = df['PUNTAJE']-df['COMPONENTE']

    

    # Asegurar que FECHA_TITULO es datetime
    df["FECHA_TITULO"] = pd.to_datetime(df["FECHA_TITULO"], format="%d-%m-%Y", errors="coerce")
    # Calcular diferencia en días
    df["DIAS_DESDE_TITULO"] = (fecha_cero - df["FECHA_TITULO"]).dt.days

    return df
#-----------------

## Mapeo de SEXO segun NOMBRE
def mapear_sexo_por_primer_nombre(df, url, nombre_col_original='NOMBRE', sexo_col='SEXO'):

    # Descargar y leer el archivo CSV si no existe localmente
    # Nombre del archivo local
    file_name = url.split("/")[-1]

    if not os.path.isfile(file_name):
        r = requests.get(url)
        with open(file_name, "wb") as f:
            f.write(r.content)

    ns_def = pd.read_csv(file_name)

    # Renombrar columna del archivo descargado para homogeneizar
    rename_dict = {"primer_nombre": "NOMBRE"}
    ns_def = ns_def.rename(columns=rename_dict)

    # Extraer primer nombre, limpiar y pasar a mayúscula
    df['primer_nombre'] = df[nombre_col_original].apply(lambda x: x.split()[0] if isinstance(x, str) else "")
    df['primer_nombre'] = df['primer_nombre'].str.strip().str.upper()
    ns_def['NOMBRE'] = ns_def['NOMBRE'].str.strip().str.upper()

    # Crear diccionario para mapeo de sexo
    dic_sexo = dict(zip(ns_def['NOMBRE'], ns_def[sexo_col]))

    # Mapear sexo usando el primer nombre
    df['SEXO'] = df['primer_nombre'].map(dic_sexo)

    # Marcar como 'ND' los casos sin coincidencia
    df['SEXO'] = df['SEXO'].fillna('ND')

    # Eliminar columna auxiliar
    df.drop(columns=['primer_nombre'], inplace=True)

    return df
#-----------------

## ORIGEN de postulante segun DNI >/<50millones
def asignar_origen(df, columna_dni='DNI'):
    # Crear columna ORIGEN según condición del DNI
    df['DNI'] = pd.to_numeric(df['DNI'], errors='coerce').astype('Int64')
    df['ORIGEN'] = df[columna_dni].apply(lambda x: 'arg' if x < 50000000 else 'extr')

    return df


## ODM alternativos
 
## ODM_CRUDO: sin los 5 puntos mas a TIPO_UNI == N (o sea con puntaje crudo)
def ODM_crudo(df):
    df = df.sort_values(
        by=['ESPECIALIDAD', 'PUNTAJE_CRUDO', 'NOTA_EXAMEN', 'PROMEDIO_CARRERA', 'DNI'],
        ascending=[True, False, False, False, True]).reset_index(drop=True
    )
    df['ODM_CRUDO'] = df.groupby('ESPECIALIDAD').cumcount() + 1
    return df

## ODM_GLOBAL_CRUDO sin agrupar especialidades, con puntaje crudo
def ODM_global_crudo(df):
    df = df.sort_values(
        by=['PUNTAJE_CRUDO', 'NOTA_EXAMEN', 'PROMEDIO_CARRERA', 'DNI'],
        ascending=[False, False, False,True]).reset_index(drop=True)
    df['ODM_GLOBAL_CRUDO'] = df.index + 1
    return df

## ODM_GLOBAL con puntaje que se usi con 5 puntos nacionales, sin agrupar especialidades
def ODM_global(df):
    df = df.sort_values(
        by=['PUNTAJE', 'NOTA_EXAMEN', 'PROMEDIO_CARRERA', 'DNI'],
        ascending=[False, False, False, True]).reset_index(drop=True)
    df['ODM_GLOBAL'] = df.index + 1
    return df

#-----------------

## Mapeo de UNIVERSIDADES
"""(En un primer momento identifique en el odm provisorio que los 
nombres de UNIVERSIDADES no estaban normalizado y tambien que habia 
hosptales entre esos nombres: hospitales argentinos sin universidad 
de medicina. A estos los asigne a la UBA.)
Ademas, con ayuda de perplexity.ai, agregue las coordenadas de latitud
y longitud de cada localidad, para luego poder graficarlas en un mapa."""
def mapear_universidades(df, file_name, nombre_col_original='UNIVERSIDAD'):

    # Descargar y leer el archivo CSV si no existe localmente
    # Nombre del archivo local
   
    universidades = pd.read_csv(file_name)

    # Hacer merge con el df original usando la columna UNIVERSIDAD como clave
    df = df.merge(universidades[['UNIVERSIDAD','UNI', 'CLASE_UNI', 'PAIS_UNI', 'CIUDAD_UNI','lat','long']],
                         left_on = nombre_col_original, right_on = 'UNIVERSIDAD', how='left')

    # Eliminar la columna original de universidad
    df = df.drop(columns=[nombre_col_original])

    return df

#-----------------
""" Como el ODM original tiene valores repetidos en varias especialidades, por mismo puntaje, 
misma nota de examen, mismo promedio; y necesito desempatarlos para el analisis posterior. Para los casos con 
estos hallazgos dentro del rango de oferta de cargos:
Clinica medica (185), 
Pediatria y pediatricas articuladas (254), 
Tocoginecología (107), 
Psiquiatria (79) Intensiva,
Procedo a desempatarlos con la siguiente funcion: """

import pandas as pd

import pandas as pd
import numpy as np

def desempate_ODM(df):
    """
    Reescribe la columna ODM para eliminar empates, por especialidad.

    Parámetros:
    df (pd.DataFrame): DataFrame de entrada que contiene las columnas 'ODM' y 'ESPECIALIDAD'.

    Retorna:
    pd.DataFrame: DataFrame con la columna 'ODM' actualizada con posiciones únicas por especialidad.
    """
    # 1. Agrega una columna temporal con el índice original para usarla como desempate.
    df['indice_original'] = df.index
    
    # 2. Ordena y reasigna el ranking dentro de cada grupo de especialidad.
    df_ordenado = df.sort_values(by=['ESPECIALIDAD', 'ODM', 'indice_original'], ascending=[True, True, True])
    
    # 3. Reescribe la columna 'ODM' utilizando `cumcount()` para asignar un ranking único
    #    dentro de cada grupo de especialidad.
    df_ordenado['ODM'] = df_ordenado.groupby('ESPECIALIDAD').cumcount() + 1
    
    # 4. Elimina la columna temporal.
    df_ordenado = df_ordenado.drop('indice_original', axis=1)
    df = df_ordenado
    
    return df
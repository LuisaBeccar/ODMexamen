import os
import pandas as pd
import pdfplumber
import requests

def limpiar_df2(df):

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
      
    # Reemplazos globales en todas las celdas
    df = df.replace({r'\n': ' ', "en tramite": "01-07-2025"}, regex=True) #crear el espacio entre los nombres en vez de "\n" y poner la fecha que elegi en vez de "en tramite"
    # Tiempo entre recibido y el examen (1 julio 2025)
    # Definir la fecha cero
    fecha_cero = pd.to_datetime("2025-07-01")

    # Asegurar que FECHA_TITULO es datetime
    df["FECHA_TITULO"] = pd.to_datetime(df["FECHA_TITULO"], format="%d-%m-%Y", errors="coerce")
    # Calcular diferencia en días
    df["DIAS_DESDE_TITULO"] = (fecha_cero - df["FECHA_TITULO"]).dt.days

    return df


"""
def limpiar_df(url_pdf: str, nombre_archivo: str = "odm.pdf") -> pd.DataFrame:
    
    #Descarga, extrae y limpia datos de un PDF en un DataFrame listo para análisis.
    #Args:
        #url_pdf (str): URL del archivo PDF a descargar.
        #nombre_archivo (str): Nombre con que se guardará el PDF localmente.
    #Returns:
        #pd.DataFrame: DataFrame limpio y transformado.
    

    # Descargar PDF si no existe localmente
    if not os.path.isfile(nombre_archivo):
        r = requests.get(url_pdf)
        with open(nombre_archivo, "wb") as f:
            f.write(r.content)


    # Extraer tablas del PDF
    data = []
    with pdfplumber.open(nombre_archivo) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                data.extend(table)

    # -----------------
    # Crear DataFrame y limpiar encabezados
    df = pd.DataFrame(data[1:], columns=data[1])
    df.columns = df.columns.str.replace("\n", " ", regex=True)
 
    # Renombrar columnas
    rename_dict = {
        "Número de documento": "DNI",
        "Apellido": "APELLIDO",
        "Nombre": "NOMBRE",
        "Institución formadora": "UNIVERSIDAD",
        "Promedio de la carrera con aplazos": "PROMEDIO_CARRERA",
        "Fecha de expedicion de titulo": "FECHA_TITULO",
        "Especialidad en la que se inscribe": "ESPECIALIDAD",
        "Puntaje obtenido en el examen": "NOTA_EXAMEN",
        "TIPO UNI": "TIPO_UNI",
        "PUNTAJE FINAL": "PUNTAJE"
    }
    df = df.rename(columns=rename_dict)

    # Eliminar filas no deseadas
    df = df[~df.isin(["DNI"]).any(axis=1)] # filas donde se repite el encabezado
    df = df[df['APELLIDO'].str.strip().astype(bool)]  # elimina filas vacías (con la celda de apellido vacio)
    df = df.dropna().reset_index(drop=True) # reindexar

    
    # Ajustes de formato
    df["NOMBRE"] = df["NOMBRE"].str.upper()
    df["APELLIDO"] = df["APELLIDO"].str.upper()
    df["FECHA_TITULO"] = pd.to_datetime(df["FECHA_TITULO"], format="%d-%m-%Y", errors="coerce")
    # Floats
    cols_f = ["PROMEDIO_CARRERA", "PUNTAJE"]
    df[cols_f] = df[cols_f].replace(",", ".", regex=True).replace("", float('nan')).astype(float)
    # Enteros
    cols_i = ['NOTA_EXAMEN', 'COMPONENTE', 'ODM']
    for col in cols_i:
        df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")
    df['PUNTAJE_CRUDO'] = df['PUNTAJE']-df['COMPONENTE']
    df["COMPONENTE"] = df["COMPONENTE"].replace("", 0) # que en vez de vacio diga cero
    
    # Reemplazos globales en todas las celdas
    df = df.replace({r'\n': ' ', "en tramite": "01-07-2025"}, regex=True) #crear el espacio entre los nombres en vez de "\n" y poner la fecha que elegi en vez de "en tramite"
    # Tiempo entre recibido y el examen (1 julio 2025)
    # Definir la fecha cero
    fecha_cero = pd.to_datetime("2025-07-01")

    # Asegurar que FECHA_TITULO es datetime
    df["FECHA_TITULO"] = pd.to_datetime(df["FECHA_TITULO"], format="%d-%m-%Y", errors="coerce")
    # Calcular diferencia en días
    df["DIAS_DESDE_TITULO"] = (fecha_cero - df["FECHA_TITULO"]).dt.days

    return df
"""

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


def asignar_origen(df, columna_dni='DNI'):
    # Crear columna ORIGEN según condición del DNI
    df['DNI'] = pd.to_numeric(df['DNI'], errors='coerce').astype('Int64')
    df['ORIGEN'] = df[columna_dni].apply(lambda x: 'arg' if x < 50000000 else 'extr')
    
    return df

def asignar_ranking(df):
    df['ODM_CRUDO'] = df.sort_values(
        by=['ESPECIALIDAD', 'PUNTAJE_CRUDO', 'ODM_CRUDO', 'PROMEDIO', 'DNI'],
        ascending=[True, False, False, False, True]
    ).groupby('ESPECIALIDAD').cumcount() + 1
    return df

def mapear_universidades(df, url, nombre_col_original='UNIVERSIDAD'):

    # Descargar y leer el archivo CSV si no existe localmente
    # Nombre del archivo local
    file_name = url.split("/")[-1]

    if not os.path.isfile(file_name):
        r = requests.get(url)
        with open(file_name, "wb") as f:
            f.write(r.content)

    universidades = pd.read_csv(file_name)

    # Hacer merge con el df original usando la columna UNIVERSIDAD como clave
    df_merged = df.merge(universidades[['UNIVERSIDAD', 'CLASE_UNI', 'PAIS_UNI', 'UNI']],
                         left_on=nombre_col_original, right_on='UNIVERSIDAD', how='left')

    # Eliminar la columna original de universidad
    df_merged = df_merged.drop(columns=[nombre_col_original])

    return df_merged

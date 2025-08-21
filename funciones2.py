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
        with open(nombre_archivo, "wb") as f:
            f.write(r.content)

    # Extraer tablas del PDF
    data = []
    with pdfplumber.open(nombre_archivo) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                data.extend(table)
    dfODM2025 = pd.DataFrame(data[1:], columns=data[1])
    dfODM2025.columns = dfODM2025.columns.str.replace("\n", " ", regex=True)
    return dfODM2025

def obtener_odm(url_pdf: str, nombre_archivo: str = "odm.pdf") -> pd.DataFrame:
    """
    Descarga, extrae y limpia datos de un PDF en un DataFrame listo para análisis.
    Args: url_pdf (str): URL del archivo PDF a descargar.
          nombre_archivo (str): Nombre con que se guardará el PDF localmente.
    Returns: pd.DataFrame: DataFrame 
    """

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
    # 
    # Crear DataFrame y limpiar encabezados
    dfodm = pd.DataFrame(data[1:], columns=data[1])
    dfodm.columns = dfodm.columns.str.replace("\n", " ", regex=True)
    # Renombrar columnas
    rename_dict = {
        "Número de documento": "DNI",
        "Apellido": "APELLIDO",
        "Nombre": "NOMBRE" }
    dfodm = dfodm.rename(columns=rename_dict)
    return dfodm

def mergeODFS (df1, df2):
  # Supongamos que ya tienes los DataFrames:
  # df1 con columnas: DNI, NOMBRE, APELLIDO (dfodm) 
  # df2 con columnas incluyendo DNI, NOMBRE, APELLIDO, PUNTAJE_CRUDO, ODM_CRUDO, PROMEDIO, ESPECIALIDAD (dfODM2025)

  # 1. Eliminar columnas NOMBRE y APELLIDO de df2 para evitar duplicados
  df2_sin_nombre = df2.drop(columns=['NOMBRE', 'APELLIDO'], errors='ignore')

  # 2. Hacer merge con df1 para traer NOMBRE y APELLIDO
  df = df2_sin_nombre.merge(df1[['DNI', 'NOMBRE', 'APELLIDO']], on='DNI', how='left')

  return df









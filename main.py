from funciones import limpiar_df, limpiar_df2, mapear_sexo_por_primer_nombre, asignar_origen, asignar_ranking, mapear_universidades, limpiar_ODM2025
from funciones2 import  obtener_odm, obtener_ODM2025

if __name__ == "__main__":
    # Lógica principal
    print("Iniciando análisis")
   
    # Llamar funciones
    """
    #primera obtencion del PDF y limpieza con creacion de variable ODM sin puntos Nacionales
    urlPDFgh = "https://raw.githubusercontent.com/LuisaBeccar/ODMexamen/main/generar_data/odm.pdf"
    df = limpiar_df(urlPDFgh)

    urlPDFODM2025gh = "https://raw.githubusercontent.com/LuisaBeccar/ODMexamen/main/generar_data/ODM2025.pdf"
    df = limpiar_df(urlPDFODM2025gh)
    """
    
    urlPDFgh = "https://raw.githubusercontent.com/LuisaBeccar/ODMexamen/main/generar_data/odm.pdf"
    dfodm = obtener_odm(urlPDFgh)

    urlPDFODM2025gh = "https://raw.githubusercontent.com/LuisaBeccar/ODMexamen/main/generar_data/ODM2025.pdf"
    dfODM2025 = obtener_ODM2025(urlPDFODM2025gh)
    
    df = mergeODFS(dfodm, dfODM2025)
    df = limpiar_df(df)

    
    # creacion de variable sexo
    url = "https://raw.githubusercontent.com/LuisaBeccar/ODMexamen/main/generar_data/ns_def.csv"
    #df.columns = df.columns.str.strip().str.upper()
    df = mapear_sexo_por_primer_nombre(df, url, nombre_col_original='NOMBRE', sexo_col='SEXO')

    # creacion de variable origen
    df = asignar_origen(df, columna_dni='DNI')

    # creacion de variable ranking
    df = asignar_ranking(df)

    # creacion de variables universidad
    url = "https://raw.githubusercontent.com/LuisaBeccar/ODMexamen/main/generar_data/universidades.csv"
    df = mapear_universidades(df, url, nombre_col_original='UNIVERSIDAD')


    print(df)
    df.to_csv("odm_2.2.csv", index=False)
    print("Análisis finalizado. Archivo 'odm_2.0.csv' creado.")


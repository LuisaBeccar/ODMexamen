from funciones import obtener_odm_provisorio, obtener_ODM2025, mergeODFS, limpiar_df, mapear_sexo_por_primer_nombre, asignar_origen, asignar_ODM_crudo, mapear_universidades

if __name__ == "__main__":
    # Lógica principal
    print("Iniciando análisis")
   
    urlodm = "https://raw.githubusercontent.com/LuisaBeccar/ODMexamen/main/generar_data/odm_provisorio.pdf"
    dfodmp = obtener_odm_provisorio(urlodm)

    urlODM2025 = "https://raw.githubusercontent.com/LuisaBeccar/ODMexamen/main/generar_data/ODM2025.pdf"
    dfODM2025 = obtener_ODM2025(urlODM2025)

    df = mergeODFS(dfodmp, dfODM2025)
    df = limpiar_df(df)

    urlsexo = "https://raw.githubusercontent.com/LuisaBeccar/ODMexamen/main/generar_data/ns_def.csv"
    df = mapear_sexo_por_primer_nombre(df, urlsexo, nombre_col_original='NOMBRE', sexo_col='SEXO')

    df = asignar_origen(df, columna_dni='DNI')

    df = asignar_ODM_crudo(df)

    urluni = "https://raw.githubusercontent.com/LuisaBeccar/ODMexamen/main/generar_data/universidades.csv"
    df = mapear_universidades(df, urluni, nombre_col_original='UNIVERSIDAD')

    nuevo_orden = ['DNI', 'NOMBRE', 'APELLIDO', 'SEXO', 'ORIGEN',
               'UNI','TIPO_UNI', 'PAIS_UNI','CIUDAD_UNI', 'lat','long', 'CLASE_UNI',
               'FECHA_TITULO', 'DIAS_DESDE_TITULO', 'PROMEDIO_CARRERA', 'ESPECIALIDAD',
               'NOTA_EXAMEN', 'COMPONENTE', 'PUNTAJE', 'PUNTAJE_CRUDO', 'ODM', 'ODM_CRUDO']

 
    df = df[nuevo_orden]
    df.to_csv('BaseODM2025.csv', index=False)
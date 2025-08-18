from funciones import limpiar_df, mapear_sexo_por_primer_nombre

if __name__ == "__main__":
    # Lógica principal
    print("Iniciando análisis")
   
    # Llamar funciones
    
    #primera obtencion del PDF y limpieza con creacion de variable ODM sin puntos Nacionales
    urlPDFgh = "https://raw.githubusercontent.com/LuisaBeccar/ODMexamen/main/odm.pdf"
    df = limpiar_df(urlPDFgh)

    # creacion de variable sexo
    url = "https://raw.githubusercontent.com/LuisaBeccar/ODMexamen/main/ns_def.csv"
    df = mapear_sexo_por_primer_nombre(df, url, nombre_col_original='NOMBRE', sexo_col='SEXO')

    print(df)

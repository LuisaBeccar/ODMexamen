from funciones import limpiar_df, mapear_sexo_por_primer_nombre

urlPDFgh = "https://raw.githubusercontent.com/LuisaBeccar/ODMexamen/main/odm.pdf"
df = limpiar_df(urlPDFgh)

url = "https://raw.githubusercontent.com/LuisaBeccar/ODMexamen/main/ns_def.csv"
df = mapear_sexo_por_primer_nombre(df, url, nombre_col_original='NOMBRE', sexo_col='SEXO')


df
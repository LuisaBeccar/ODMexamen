# URL de la página con la tabla
url = 'https://buenosaires.gob.ar/areas/registrocivil/nombres/busqueda/imprimir.php'

# Hacer la petición HTTP
response = requests.get(url)
response.raise_for_status()  # para asegurarse que la petición fue exitosa

# Parsear el contenido HTML
soup = BeautifulSoup(response.text, 'html.parser')

# Encontrar la tabla (observa que la tabla tiene etiqueta <table>)
table = soup.find('table')

# Extraer filas de la tabla
rows = table.find_all('tr')

# Listas para almacenar los datos
nombres = []
sexos = []

# Iterar sobre las filas (excepto encabezado)
for row in rows[1:]:
    cols = row.find_all('td')
    if len(cols) >= 2:
        nombre = cols[0].get_text(strip=True)
        sexo = cols[1].get_text(strip=True)
        nombres.append(nombre)
        sexos.append(sexo)

# Crear DataFrame
df_civil = pd.DataFrame({'NOMBRE': nombres, 'SEXO': sexos})
df_civil['NOMBRE'] = df_civil['NOMBRE'].str.upper()
df_civil['SEXO'] = df_civil['SEXO'].replace("A", "F") # mire todos los A y eran de mujer
df_civil
df_civil.SEXO.value_counts()



!wget "https://raw.githubusercontent.com/LuisaBeccar/ODMexamen/main/nombres_raros_sexo.csv"
nombres_raros_sexo = pd.read_csv("nombres_raros_sexo.csv")
nombres_raros_sexo
nombres_raros_sexo.info()
nombres_raros_sexo.SEXO = nombres_raros_sexo.SEXO.replace('F','F')
nombres_raros_sexo.SEXO.value_counts()
nombres = pd.concat([df_civil, nombres_raros_sexo])
nombres.drop_duplicates(subset=['NOMBRE'], inplace=True)
nombres['SEXO'] = nombres['SEXO'].str.strip().str.upper()

nombres.SEXO.value_counts()

# Extraer el primer nombre del nombre compuesto DF
df['primer_nombre'] = df['NOMBRE'].apply(lambda x: x.split()[0])
df['primer_nombre'] = df['primer_nombre'].str.strip().str.upper()
nombres['NOMBRE'] = nombres['NOMBRE'].str.strip().str.upper()

# Crear un diccionario a partir del df nombres para mapeo rápido
dic_sexo = dict(zip(nombres['NOMBRE'], nombres['SEXO']))

# Mapear sexo usando el primer nombre
df['SEXO'] = df['primer_nombre'].map(dic_sexo)

# Opcional: marcar como 'ND' (No determinado) los casos sin coincidencia
df['SEXO'] = df['SEXO'].fillna('ND')

# Eliminar columna auxiliar si no quieres mantenerla
#df.drop(columns=['primer_nombre'], inplace=True)
df['SEXO'].value_counts()

df['SEXO'][df['SEXO']=='ND'] # quedaba 1 registro MARÍA con la tilde el reves, LO PASO A FEMENINO
df.loc[df['SEXO'] == 'ND', 'SEXO'] = 'F'

ns_definitivo = df[['primer_nombre','SEXO']]
ns_definitivo.to_csv("ns_def.csv", index=False)
nombres_raros = df[df['SEXO']=='ND']
nombres_raros = nombres_raros['NOMBRE']
nombres_raros.to_csv("nombres_raros.csv", index=False)

#df_ND = df1[df1['SEXO'].isin(['ND'])]
#df_ND = df_ND[['NOMBRE']]
# le pase la lista a perplexity para que me busque los nombres y asigne M o F segun nombres latinoamericanos
# luego cargue ese csv al repo de github y aca lo traigo

!wget "https://raw.githubusercontent.com/LuisaBeccar/ODMexamen/main/nombres_raros_sexo.csv"
DN = pd.read_csv("nombres_raros_sexo.csv")
DN.SEXO.value_counts() # todos los nombres estan clasificados
# DN.NOMBRE.value_counts() # hay nombres que se repiten, los elimino
DN = DN.drop_duplicates(subset=['NOMBRE'])
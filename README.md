
# EXAMEN UNICO DE RESIDENCIAS MEDICAS 2025
En este trabajo me propongo analizar la informacion que se puede recabar a partir del orden de merito establecido a partir del examen de residencias médicas. <br>
[Un poco de contexto](https://docs.google.com/document/d/1e26gSZ5d6f15_OUe8-Te_XGt8p-8-QilXmxNJ96a44c/edit?usp=sharing)

## Base de datos: Base_ODM2025.csv

- odm_provisorio.pdf
- ODM2025.pdf
- ns_def.csv 
- universidades.csv 

En los archivos fuente de orden de mérito se encuentran datos categoricos: dni, nombre, apellido, universidad, tipo de universidad, especialidad elegida, y datos numericos: promedio de carrera, nota de examen, puntos extra, orden de merito. También se encuentra la fecha de titulo.

Dichas bases fueron enriquecidas con la creación de nuevas variables: cantidad de dias entre el titulo y el examen (en caso de tener titulo en tramite a la fehca del examen, se considerará el dia previo al examen como fecha de titulo). Se crea un puntaje crudo, sin los extra 5 puntos por universidad argentina, y con ello un orden de merito crudo. Ademas se crea orden de merito global y orden de merito global crudo (sin el puntaje extra). En estos casos se considera para los casos de empate de puntaje, primero la mejor nota de examen, luego de carrera y luego el menor numero de dni (segun vi casos en ODM definitivo).

Se crea la variable ORIGEN para estimar si el postulante es argentino (tomando como parámetro el número de DNI, y arbitrariamente asignando que si el numero es menor a 50 millones, probablemente sea alguien nacido y nacionalizado en el país antes de 2010 aproximadamente).

Para asignar el sexo a cada postulante, creé *ns_def.csv*, una base de datos con nombres (primer nobre) para asignar el sexo Masculino o Femenino. Utilicé una base de nombres del registro civil argentina y luego la completé con nombres que no se hallaban en la misma, consultando a distintas inteligencias artificiales que me asignaran el uso más común para esos nombres.

De manera similar cree *universidades.csv*. Fue todo un desafío ya que no solo no estaba normalizado sino que también había instituciones que no corresponden a universidades. Por ejemplo se encontraba el Hospital Lanari de Buenos Aires, que no es institución con carrera de medicina. Asi terminé corrigiendo artesanalamente, normalizando en un google sheets. Luego se indagué qué clase de universidad era cada una: privada o pública, el país, la ciudad donde se localiza y sus coordenadas geoespaciales. En un proceso a parte se tomo el dataset casi limpio y se utilizó esas variables de latitud y longitud para transfomrar el archivo en geo.


## Analisis

# enfoque original: 
- Comparar el orden de merito definitivo ODM vs como hubiera quedado si no se hubiera asignado los 5 puntos a universidades argentinas ODM_CRUDO. Solo visualizando la posicion de los postulantes de universidad argentina o extranjera. para eso se creo la variable PUNTAJE_CRUDO, restandole el COMPONENTE al PUNTAJE. Para cad aespecialidad se uso ese PUNTAJE_CRUDO para crear ODM_CRUDO y luego el puntaje se uso para crar el ODM_GLOBAL y el puntaje crudo para el ODM_GLOBAL_CRUDO.
Se creo un indicador que mide cuanto se separa el orden de merito definitivo con el odm crudo y que tan cerca está del odm extremo (que seria el igual a poner a todos los que estudiaron en universidades argentinas arriba en el orden de los que estudiaron en universidades extranjeras)

## tradicional
Del archivo geoespacial se crea un mapa donde se puede ver cuantos postulantes hay en cada región. 

En cuanto a los datos **cualitativos**, querremos caracterizar en orden jerarquico: 

- Cuántos postulantes totales hubo. 
- Clasificarlos por país donde estudio (PAIS_UNI)
- Clasificar dentro de los que estudiaron en Argentina cuantos son argentinos y cuantos extranjeros.
- Cuántos postulantes hubo para cada especialidad, y su proporción del total
- Para cada especialidad: proporcion de 
  + varones y mujeres, 
  + argentinos y extranjeros, 
  + universidad en argentina vs universidad extranjera 



Para datos **cuantitativos** podrían ser varios enfoques: 

- Analisis basico de distribucion de *notas de promedio de carrera*, *notas de examen* totales, y segun cada variable categorica de interés.

Luego
- Hay distribución normal ?
- Hay diferencia estadisticamente significativa entre el promedio de varones y mujeres ? 
- Hay diferencia estadísticamente significativa entre la nota media de quienes estudiaron en argentina vs quienes estudiaron en el exterior ?

- Hay relación entre la cantidad de días desde el titulo hasta el examen y la nota obtenida en el mismo? 
- Hay alguna tendencia entre la eleccion de especialidad y la fecha de título ?

  ## Geo
  Con los archivos *CrearGeoDF.py* se genera *datos.gpkg* y a partir de este archivo con coordenadas geolocalizables, con *mapa.py* se genera el mapa interactivo: *mapa_registros.html*

  # [INCONCISTENCIAS EN DATOS FUENTE](https://docs.google.com/document/d/1XMWdNzBpl-Tw5Lj3P3snbjPwlDUCqnMgbz2sC459_pA/edit?usp=sharing)

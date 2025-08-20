<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  
</head>
<body>
  <h1>Examen Unico Orden de Merito</h1>
  <p>Analisis de los postulantes a las residencias medicas a traves del exámen unico</p>
  
  <h2>Base de datos: df</h2>

  <p>Como punto de partida se toma el pdf público del orden de merito provisorio (Y por qué no el definitivo? pues habia empezado con el provisorio antes de que publicaran el definitivo, y luego cuando subieron el definitivo el 20 de agosto, el nombre y apellido estaba todo junto en una misma celda, entonces) ((FUTUROS PASOS, HACER UN JOIN CON EL DNI ENTRE odm y ODM2025 que es el definitivo para que si hubo algun cambio en los puntajes de las notas, se use para el analisis las notas y puntajes definitivos, pero conservar las columnas creadas (sexo a partir del nombre) y las funciones que definen de donde es cada universidad y si es publica o privada, quizas aplicado a la nueva lista que podria llegar a tener corecciones?)). A este se le realizan ciertos pasos de limpieza de datos.</p>

  <p>Uso archivos que dejo dentro de la carpeta generar_data: registro_civil y prompts en perplexity.ia, especificamente para:</p>
    <li>Para buscar el sexo de los nombres: </li>
    <li>Para buscar si las universidades eran privadas o publicas: </li>
      <tr>"para cada institucion educativa donde se dicta la carrera de medicina de la lista quiero que busques si es universidad "publica" (ejemplo: UNIVERSIDAD DE BUENOS AIRES: donde es gratis ya que depende del Estado) o "privada" (ejemplo: PONTIFICIA UNIVERSIDAD CATOLICA ARGENTINA SANTA MARIA DE LOS BUENOS AIRES, donde el alumno debe pagar una matricula y cuota mensual). Puedes separar la lista en dos (primeros 82 y segundos 81) para optimizar la tarea. Devuelvemelo en fomra de tabla UNIVERSIDAD, TIPO. Lista de instituciones educativas en medicina: ...(lista de universidades filtrdas como unicos de la tabla)" </tr>
      <tr>Descubro que hay Hospitales nacionaes en lugar de universidades. Y universidades con distintos nombres. Los normalizo creando una tabla manualmente en google sheets </tr>
    <li>Para buscar el país al que pertenece cada universidad:</li>
      <tr>"ahora con la misma metodologia en tandas y devolviendo una tabla quiero que busques el pais a donde pertenece cada institucion"</tr>
    <li> Para estimar si el postulante es argentino o extranjero, mas alla de si estudio en una universidad en argentina o en el exterior, creo la variable ORIGEN donde a modo arbitrario pero pensando en la edad de los postulantes, si el DNI es menor a 50millones sera arg (argentino) y si es mayor, extr (extranjero).</li>

    Columna ODM_CRUDO: columna en mi dataframe df a partir de la columna PUNTAJE_CRUDO que para cada categoria de ESPECIALIDAD ordene de 1 (el mayor) a n° el menor valor de la columna ODM_CRUDO. En caso de que tengan el mismo Puntaje_crudo, que tenga puesto con nuemero mas bajo aquel con mejor nota de examen, en caso de que tengan tambien misma nota de examen, mejor puntaje el que tenga mejor promedio, y en caso de que tengan tambien igual promedio, que se ranquee mejor a aquel con dni con numeno menor.

  
  <h2>Analisis</h2>
  <p>A partir de odm_2.0.csv procedere a realizar el analisis</p>
    <li>Descriptivo de cada variable</li>
    <li>Buscar correlaciones y ver si son estadisticamente significativas</li>

</body>
</html>

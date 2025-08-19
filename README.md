<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  
</head>
<body>
  <h1>Examen Unico Orden de Merito</h1>
  <p>Analisis de los postulantes a las residencias medicas a traves del exámen unico</p>
  
  <h2>La Data: df</h2>
  <p>Como punto de partida se toma el pdf público de orden de merito provisorio. A este se le realizan ciertos pasos de limpieza de datos.</p>
  <p>Generado con los archivos dentro de generar_data: registro_civil y prompts en perplexity.ia, especificamente para ciertos datos</p>
    <li>Para buscar el sexo de los nombres: </li>
    <li>Para buscar si las universidades eran privadas o publicas: </li>
      <tr>para cada institucion educativa donde se dicta la carrera de medicina de la lista quiero que busques si es universidad "publica" (ejemplo: UNIVERSIDAD DE BUENOS AIRES: donde es gratis ya que depende del Estado) o "privada" (ejemplo: PONTIFICIA UNIVERSIDAD CATOLICA ARGENTINA SANTA MARIA DE LOS BUENOS AIRES, donde el alumno debe pagar una matricula y cuota mensual). Puedes separar la lista en dos (primeros 82 y segundos 81) para optimizar la tarea. Devuelvemelo en fomra de tabla UNIVERSIDAD, TIPO
lista de instituciones educativas en medicina: ...(lista de universidades filtrdas como unicos de la tabla) </tr>
      <tr>Descubro que hay Hospinales nacionaes en lugar de universidades. Y universidades con distintos nombres. Los normalizo creando una tabla manualmente en google sheets </tr>
    <li>Para buscar el país al que pertenece cada universidad:</li>
      <tr>ahora con la misma metodologia en tandas y devolviendo tabla quiero que busques el pais a donde pertenece cada institucion</tr>
    <li>Se creara una variable para marcar que los DNI que comienzan con 93, 94 o 95 millones corresponden a extranjeros con residencia temporal o permanente en Argentina, mientras que los que rondan los 40 millones son probablemente argentinos </li>

  
  <h2>Analisis</h2>
  <p>A partir de odm_limpio.csv procedere a realizar el analisis</p>
    <li>Descriptivo de cada variable</li>
    <li>Buscar correlaciones y ver si son estadisticamente significativas</li>

</body>
</html>

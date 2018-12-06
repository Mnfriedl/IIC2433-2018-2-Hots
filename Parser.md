# Como mejorar el *parser*

## Funcionamiento actual del *parser*

Actualmente, nuestro *parser* de replays tiene cuatro etapas importantes, las cuales son actividades bloqueantes, y lentas. Estas cuatro son: 
- Descargar el archivo `.StormReplay`.
- *Parsear* el archivo, y obtener la información relevante.
- Eliminar el archivo del disco dico (para no acumular una gran cantidad de archivos, ya que cada `.StormReplay` pesa entre 1MB y 2MB).
- Insertar los datos relevantes obtenidos a la base de datos.

Por el momento, el parser está obteniendo aproximadamente 1.000 *replays* por hora, lo cual es bastante lento, considerando que la API completa contiene más de 12 millones de *replays*. Por este motivo es que a continuación se propondrán dos métodos distintos (propuestos como trabajo futuro, ya que no fueron implementados) de como este se podría mejorar para aumentar su eficiencia.

## Primera propuesta: *threads* y *queues*

Claramente, el problema de nuestro parser actual es que tiene demasiadas tareas lentas, las cuales no se están ejecutando de forma continua cada una. La primera depende de la velocidad de descarga, la segunda depende de la velocidad de la CPU, mientras que la tercera y cuarta dependen de la velocidad del disco duro, por lo que facilmente estas podrían separarse, para poder ejecutarlas todas al mismo tiempo.

Nuestra primera propuesta es utilizar un *thread* para cada tarea. Para lograr una comunicación entre cada *thread*, se utilizan *queues*, donde, cada *thread* al terminar de trabajar en una *replay*, inserta esta, junto con la información necesaria para los pasos siguientes a una cola, y el *thread* del siguiente paso puede comenzar a trabajar en esta, mientras los otros *threads* pueden seguir ejecutando sus tareas, con sus propios *queues*, sin bloquearse entre sí.

En este método, el único factor bloqueante es que la velocidad de descarga de los archivos *replay* sea más lento que los demás pasos del *parser*.

## Segunda propuesta: múltiples *cores* de la CPU

Esta segunda propuesta, no es independiente de la primera, si no que una extensión. Se mencionó anteriormente que la velocidad puede ser un factor bloqueante. Ahora, ¿qué sucede si nuestro cuello de botella resultara ser la velocidad de la CPU?

En este caso, podríamos aprovecharnos de los múltiples *cores* que tienen las CPUs modernas, e implementar el segundo paso del *parser*¨en más de un *core*, disminuyendo, e incluso eliminando, el cuello de botella formado.

Utilizando estos métodos, se podría incrementar considerablemente la eficiencia de nuestro *parser*, y así poder obtener una masa mucho mayor de datos en comparación a lo que somos capaces de obtener en este momento.

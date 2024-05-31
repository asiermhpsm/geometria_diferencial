# API REST de Geometría Diferencial de superficies parametrizadas e implícitas.

## Instalación

Utilizar una versión de Python 3.11. Otras versiones pueden llegar a dar problemas con la librería Flassger, como es el caso de las versiones 3.12.

Crear un entorno vitual para instalar las dependencias del proyecto.

Consultar versión de entorno virtual: 

            virtualenv --version

Si salta un error, instalar:

            pip install virtualenv

Crear un entorno virtual (venv: nombre del entotno):

            virtualenv -p python venv

Activar el entorno vitual:

            source venv/bin/activate (Para Mac o Linux)

            venv\Scripts\activate (Para Windows)

Instalar requirements.txt con el comando:

            pip install -r requirements.txt

o utilizando el IDE que se esté usando.

Desactivar entorno virtual:

            deactivate

## Ramas
-   main: Rama con el código de la librería.
-   Desarrollo: Rama de desarrollo donde se han realizado todas las pruebas en el desarrollo del sistema. La única diferencia actual con la main es el archivo interfaz.py que contiene una interfaz rudimentaria desarrollada en Flask.


## Estructura
-  Archivo app.py: Archivo que levanta el servidor. Este es el archivo que se debe ejecutar para realizar peticiones HTTP a la librería.
-  (Archivo interface.py: Archivo con el diseño de la interfaz gráfica. Se debe ejecutar para utilizar la interfaz)
-  Archivo README.md: Archivo con la información necesaria para el uso del proyecto.
-  Archivo requirements.txt: Archivo con las librerías utilizadas en el proyecto y sus versiones.
-  Carpeta utils: Carpeta donde se implementan todos los métodos que se usan para realizar los cálculos necesarios.
    - Archivo calc_imp.py: Archivo con todos los métodos que se usan para realizar los cálculos relacionados con superficies implícitas a excepción de las representaciones gráficas.
    - Archivo calc_param.py: Archivo con todos los métodos que se usan para realizar los cálculos relacionados con superficies parametrizadas a excepción de las representaciones gráficas.
    - Archivo graph.py: Archivo con todos los métodos usados para la representación gráfica, tanto de superficies implícitas como parametrizadas.
    - Archivo utils.py: Archivo que contiene métodos de utilidad general.
    - Carpeta Latex: Carpeta con distintos archivos que se usan para almacenar taanto constantes con la teoría de los distintos elementos de las superficies como métodos que presentan los resultados en formato LaTex.


## Documentación Swagger
Para acceder a la documentación Swagger:

1) Ejecutar el archivo app.py

        python app.py

2) Acceder a la URL: http://localhost:{puerto}/apidocs


## Uso de la interfaz
Para utilizar la interfaz gráfica:

1)  Moverse a la rama Desarrollo

        git checkout Desarrollo

2) Ejecutar el archivo interface.py

        python interface.py

3) Aparecerá en la pantalla una ventana con la interfaz gráfica.


## Levantar el servidor Flask
Para levantar el servidor Flask:

2) Ejecutar el archivo app.py

        python app.py

3) El servidor se levanta en local, dependiendo de los recursos del ordenador en ese momento se levanta en un puerto u otro. Los más comunes son 8080 o 5000. Para hacer peticiones poner en el navegador:

        localhost:{puerto}/{endpoint}

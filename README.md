# Descripción

En este repositorio de brindan las herramientas para la automatización de la generación de reportes a partir de DWH.

En el directorio principal existen dos carpetas principales: Python Scripts y R Scripts. Ambas se dividen a su vez en carpetas secundarias cuyo nombre es ilustrativo del reporte que se puede generar a partir de ellas, y contienen un manual de uso propio.

# Requerimientos previos:

* Contar con un ambiente de python (Anaconda sugerido)
* Installar librería pyodbc mediante 
```
pip install pyodbc
```
* Descargar e instalar Microsoft® ODBC Driver 13.1 for SQL Server® desde:

> https://www.microsoft.com/en-us/download/details.aspx?id=53339

* Configurar un origen de datos ODBC, como sugerencia utilizar el videotutorial:

> https://www.youtube.com/watch?v=2xQX76nEdvo

Y sustituyendo lo parámetros por los correctos.

# Método de Uso

1. Copiar todos los archivos contenidos en el repositorio a la ubicación de la PC en la que se desea almacenar los reportes.
2. Editar los parámetros en el archivo "connection_parameter.txt" para poder acceder al origen de datos SQL configurado anteriormente.
3. En un ambiente de Python, ejecutar el comando:

```
python ".\MiCarpeta\connect_sql_dwh_git.py" .\Micarpeta\connection_parameters.txt
```


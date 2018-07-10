# Descripción

En este repositorio de brindan las herramientas para la automatización de la generación de reportes a partir de DWH.

En el directorio principal existen dos carpetas principales: Python Scripts y R Scripts. Ambas se dividen a su vez en carpetas secundarias cuyo nombre es ilustrativo del reporte que se puede generar a partir de ellas, y contienen un manual de uso propio.

# Método de Uso

1- Copiar todos los archivos contenidos en el repositorio a la ubicación de la PC en la que se desea almacenar los reportes.
2- En un ambiente de Python, ejecutar el comando:

python ".\MiCarpeta\connect_sql_dwh_git.py" .\Micarpeta\connection_parameters.txt


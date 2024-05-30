# FastAPI 

FastAPI es un framework web para Python que destaca por su velocidad, facilidad de uso y código limpio. Es uno de los frameworks Python más rápidos, con un rendimiento comparable al de Node.js y Go. Nos permite desarrollar funciones hasta un 300% más rápido y reduce errores en un 40%. Es intuitivo, fácil de aprender y usar, gracias a su excelente soporte para editores y completado automático. Además, genera documentación interactiva y se basa en estándares abiertos para APIs.

## Marco de trabajo para la integración:

1. **Objetivo:**  Establecer una conexión estratégica entre un Data Warehouse (DW) y un Cuadro de Mando Integral (CMI) para que este último pueda realizar consultas sobre metas específicas, obtener información del DW y generar resultados visualizados y analíticos.

2. **Funcionamiento** :

    - Extracción de datos: El CMI extrae datos relevantes del DW para calcular los KPIs asociados a las metas seleccionadas.

    - Cálculo de KPIs: El CMI procesa los datos extraídos y calcula los valores de los KPIs.

## Características 

- __*FastAPI*__: Un marco web de alto rendimiento para Python.
- __*Pydantic*__: Una biblioteca para la validación de datos y la creación de modelos de datos
- __*SQLAlchemy*__ : Una biblioteca de Object Relational Mapper (ORM) para Python.


## Configuración

Para configurar el framework, siga estos pasos:

1. Cree un archivo .env en la raíz del proyecto. Este archivo debe contener las siguientes variables de entorno:

```py 
DATA_WAREHOUSE_DATABASE_URL="mssql+pyodbc://USER:PASSWORD@LOCALHOST:PORT/DATABASE?driver=ODBC+Driver+17+for+SQL+Server" 

CMI_DATABASE_URL="mssql+pyodbc://USER:PASSWORD@LOCALHOST:PORT/DATABASE?driver=ODBC+Driver+17+for+SQL+Server"
```

2. Instale las dependencias del proyecto:

```bash
pip install -r requirements.txt
```

## Ejecución de la aplicación

Para ejecutar la aplicación, ejecute el siguiente comando:

```bash
uvicorn app.main:app --reload
```
## Instalación

Sigue este paso para instalar y configurar el framework en tu entorno local:

1. Clona el repositorio desde GitHub:

```bash 
git clone https://github.com/Carlos-vargs/cube-api-python.git
```
## Consideraciones adicionales

1. Esta es solo una API de ejemplo simple. Puede ampliarla para incluir más funcionalidad, como la capacidad de buscar cubos por nombre o dimensiones.

2. Puede usar una base de datos diferente a Microsoft SQL Server
, como PostgreSQL o MySQL.

## Recursos adicionales

- Documentación de [FastAPI](https://fastapi.tiangolo.com/tutorial/first-steps/) utlizada en este proyecto.
## Soporte

Si encuentras algún problema o tienes alguna pregunta sobre el uso de este framework, puedes crear un issue en el repositorio de GitHub o contactarnos a través de [nuestra página web](https://carlosvargas.vercel.app/).



---
¡Gracias por tu interés! Esperamos que estae framework te ayude a mejorar la eficiencia de tus procesos. Si tienes alguna pregunta adicional, no dudes en contactarnos.

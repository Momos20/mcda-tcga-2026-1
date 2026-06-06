# Ejecución en Databricks — Proyecto TCGA/RNA-Seq

Este documento describe cómo ejecutar en **Databricks** el proyecto de clasificación de tipos de cáncer a partir de perfiles de expresión génica derivados de RNA-Seq.

La versión Databricks está orientada a representar una arquitectura **lakehouse** con separación por capas, uso de **Volumes**, procesamiento con **PySpark/SparkSQL** y almacenamiento de salidas en formatos escalables como **Delta** y **Parquet**.

---

## Propósito de la versión Databricks

Esta versión permite mostrar cómo el proyecto puede implementarse en un entorno cloud distribuido, manteniendo una organización clara de datos, procesamiento y salidas analíticas.

En particular, la versión Databricks sirve para:

- Organizar los datos en una arquitectura por capas.
- Procesar archivos RNA-Seq usando Spark.
- Construir datasets trusted y refined.
- Ejecutar análisis exploratorio con PySpark y SparkSQL.
- Entrenar modelos de clasificación usando SparkML.
- Generar tablas de métricas, predicciones y visualizaciones.
- Dejar evidencia de una posible implementación productiva.

---

## Consideración sobre limitaciones

Aunque Databricks es adecuado para procesamiento distribuido, en este proyecto pueden aparecer limitaciones prácticas por:

- Tamaño de los archivos RNA-Seq.
- Alta dimensionalidad de la matriz muestra-gen.
- Consumo de memoria durante transformaciones ancho/largo.
- Costos o restricciones del clúster.
- Tiempos de entrenamiento y validación de modelos.
- Disponibilidad de librerías específicas en el runtime.

Por esta razón, el proyecto mantiene también una versión local. La versión local permite validar lógica, depurar notebooks y ejecutar escenarios controlados cuando Databricks resulte costoso o limitado.

---

## Archivos de la versión Databricks

```text
databricks/
├── 00_configuracion_databricks.py
├── 02_preparacion_trusted_databricks.ipynb
├── 03_eda_sparksql_databricks.ipynb
├── 04_feature_selection_rfecv_databricks.ipynb
├── 05_modelo_sparkml_multiclase_databricks.ipynb
├── 06_aplicacion_visualizacion_refined_databricks.ipynb
├── 07_negocio_databricks.ipynb
└── README_DATABRICKS.md
```

El archivo `00_configuracion_databricks.py` es el único archivo `.py`, porque funciona como configuración reutilizable para los demás notebooks mediante `%run`.

---

## Ruta base utilizada

La configuración está pensada para trabajar sobre un Volume en Databricks:

```text
/Volumes/workspace/default/tcga_cancer_ml
```

Desde esta ruta se organizan las capas del proyecto:

```text
/Volumes/workspace/default/tcga_cancer_ml/
├── raw/
│   ├── metadata/
│   └── rnaseq/
├── trusted/
├── refined/
│   ├── eda_outputs/
│   ├── model_metrics/
│   ├── predictions/
│   ├── visualizations/
│   ├── tables/
│   ├── exports/
│   └── app_exports/
└── models/
```

---

## Capa Raw

La capa `raw` contiene los insumos originales:

```text
raw/
├── metadata/
│   └── metadatos_tcga_oficial_18_clases.csv
└── rnaseq/
    └── archivos RNA-Seq / STAR Counts
```

Esta capa no debe modificarse manualmente después de la ingesta. Su objetivo es conservar trazabilidad sobre los archivos originales.

---

## Capa Trusted

La capa `trusted` contiene datos limpios y estructurados:

```text
trusted/
├── rnaseq_long/
├── rnaseq_matrix/
├── samples_18_clases/
└── gene_dictionary/
```

En esta etapa se realizan tareas como:

- Lectura de archivos RNA-Seq.
- Normalización de columnas.
- Control de duplicados.
- Construcción de llaves técnicas.
- Unión con metadatos.
- Filtrado de clases principales.
- Construcción de datasets analíticos confiables.

---

## Capa Refined

La capa `refined` contiene salidas listas para análisis, visualización o consumo:

```text
refined/
├── eda_outputs/
├── model_metrics/
├── predictions/
├── visualizations/
├── tables/
├── exports/
└── app_exports/
```

Esta capa recibe:

- Tablas EDA.
- Resultados de selección de características.
- Métricas de modelos.
- Predicciones.
- Reportes de clasificación.
- Visualizaciones.
- Tablas para prototipo de aplicación o dashboard.
- Salidas de análisis de negocio.

---

## Orden de ejecución

Ejecute los notebooks en este orden:

1. `00_configuracion_databricks.py`
2. `02_preparacion_trusted_databricks.ipynb`
3. `03_eda_sparksql_databricks.ipynb`
4. `04_feature_selection_rfecv_databricks.ipynb`
5. `05_modelo_sparkml_multiclase_databricks.ipynb`
6. `06_aplicacion_visualizacion_refined_databricks.ipynb`
7. `07_negocio_databricks.ipynb`

Los notebooks `02` a `07` deben iniciar cargando la configuración:

```python
%run ./00_configuracion_databricks
```

Todos los archivos deben estar en la misma carpeta del Workspace o se debe ajustar la ruta del `%run`.

---

## Descripción de notebooks

| Notebook | Descripción |
|---|---|
| `00_configuracion_databricks.py` | Define rutas, clases, mapas de cáncer, funciones de lectura/escritura y estructura de carpetas en Volumes. |
| `02_preparacion_trusted_databricks.ipynb` | Procesa datos raw y genera datasets trusted. |
| `03_eda_sparksql_databricks.ipynb` | Ejecuta análisis exploratorio con SparkSQL y PySpark. |
| `04_feature_selection_rfecv_databricks.ipynb` | Realiza selección de características para reducir dimensionalidad. |
| `05_modelo_sparkml_multiclase_databricks.ipynb` | Entrena y evalúa modelos de clasificación multiclase. |
| `06_aplicacion_visualizacion_refined_databricks.ipynb` | Genera tablas refinadas, exportaciones y visualizaciones para comunicación. |
| `07_negocio_databricks.ipynb` | Construye escenarios de negocio para estimar valor operativo en EPS/IPS. |

---

## Configuración del clúster

Se recomienda usar un runtime compatible con Spark 3.5 o superior. Las librerías principales requeridas son:

```text
pandas
numpy
matplotlib
scikit-learn
xgboost
pyarrow
joblib
requests
optuna
openTSNE
```

En Databricks, varias librerías ya pueden venir instaladas según el runtime. Si alguna falta, puede instalarse desde la pestaña **Libraries** del clúster o mediante `%pip install`.

Ejemplo:

```python
%pip install xgboost optuna openTSNE
```

Después de instalar librerías con `%pip`, reinicie el intérprete si Databricks lo solicita.

---

## Tablas y persistencia

La configuración está preparada para guardar salidas como:

- Archivos en Volumes.
- Tablas Delta.
- Exportaciones CSV cuando el tamaño lo permite.
- Figuras en `refined/visualizations`.

Las funciones principales son:

```python
save_trusted(df, path)
read_trusted(path)

save_spark_table(df, nombre_tabla)
load_spark_table(nombre_tabla)

guardar_figura(nombre_archivo)
```

---

## Recomendaciones de ejecución

Para evitar fallos por memoria o tiempo:

- Ejecute primero con subconjuntos de datos.
- Reduzca temporalmente el número de genes seleccionados.
- Controle el número de particiones Spark.
- Evite convertir grandes DataFrames completos a pandas.
- Guarde resultados intermedios después de cada etapa.
- Revise que las rutas del Volume existan antes de ejecutar notebooks pesados.
- Use la versión local para depurar código antes de escalarlo en Databricks.

---

## Relación con la versión local

La versión Databricks y la versión local son complementarias:

| Entorno | Uso recomendado |
|---|---|
| Local | Desarrollo, pruebas, depuración, visualizaciones, análisis de negocio y ejecución controlada. |
| Databricks | Arquitectura lakehouse, procesamiento distribuido, evidencia de ingeniería de datos y escenario productivo. |

Debido a las restricciones de recursos, no todo el flujo necesariamente debe ejecutarse de forma completa en Databricks. Lo importante es conservar la arquitectura, demostrar la trazabilidad por capas y validar las etapas principales.

---

## Resultado esperado

Al finalizar la ejecución, se deben obtener:

- Datasets trusted.
- Tablas EDA.
- Matriz analítica refinada.
- Genes seleccionados.
- Métricas de modelos.
- Predicciones.
- Visualizaciones.
- Tablas de negocio.
- Evidencia de arquitectura lakehouse.

---

## Nota final

Esta implementación no corresponde a una solución clínica validada. Es un ejercicio académico de analítica avanzada, ingeniería de datos y aprendizaje automático aplicado a datos biomédicos abiertos.

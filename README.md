<p align="center">
  <img src="https://latimpacto.org/wp-content/uploads/2023/11/Eafit.png" width="40%">
</p>

Este repositorio contiene el desarrollo del proyecto **Clasificación de tipos de cáncer mediante aprendizaje automático a partir de perfiles de expresión génica derivados de RNA-Seq**, construido por el equipo **Sigma Analytics**.

El proyecto integra dos formas de ejecución:

1. **Ejecución local**, pensada para desarrollo, validación, pruebas controladas y ejecución en equipos personales.
2. **Ejecución en Databricks**, pensada para una arquitectura lakehouse, procesamiento distribuido y organización por capas.

Debido a limitaciones prácticas de recursos en Databricks, especialmente por el volumen de datos, la alta dimensionalidad de la matriz génica y los tiempos de entrenamiento, se conserva también una versión local del flujo. Esta versión permite validar la lógica del proyecto, depurar notebooks, ajustar visualizaciones y ejecutar escenarios de negocio sin depender completamente del entorno cloud.

---

## Descripción del proyecto

El cáncer es una enfermedad altamente heterogénea. Tumores que parecen similares desde el punto de vista clínico pueden presentar diferencias moleculares profundas que influyen en su progresión, tratamiento y pronóstico.

Por esta razón, el proyecto utiliza perfiles de expresión génica derivados de **RNA-Seq** para construir modelos de aprendizaje automático capaces de clasificar distintos tipos de cáncer. La información proviene de fuentes abiertas y desidentificadas de **The Cancer Genome Atlas (TCGA)** y **Genomic Data Commons (GDC)**.

La unidad de análisis es la muestra tumoral. Cada muestra se representa mediante valores de expresión génica, y la variable objetivo corresponde al tipo de cáncer asociado.

---

## Objetivo general

Construir una solución analítica reproducible que permita clasificar tipos de cáncer a partir de datos RNA-Seq, integrando preparación de datos, análisis exploratorio, selección de características, modelado supervisado, visualización de resultados y análisis de valor para actores del sistema de salud.

---

## Objetivos específicos

- Ingerir y organizar datos abiertos de TCGA/GDC.
- Construir una matriz analítica muestra-gen.
- Explorar la distribución de clases, genes y muestras.
- Seleccionar genes relevantes para reducir dimensionalidad.
- Entrenar modelos de clasificación multiclase.
- Evaluar el desempeño mediante métricas globales y por clase.
- Generar salidas refinadas para visualización y comunicación.
- Construir un análisis de negocio orientado a EPS e IPS.
- Comparar la ejecución local frente a la ejecución en Databricks.

---

## Estructura general del repositorio

```text
proyecto/
├── local/
│   ├── 00_configuracion.py
│   ├── 01_descarga_ingesta_gdc_raw.ipynb
│   ├── 02_preparacion_trusted.ipynb
│   ├── 03_eda_sparksql.ipynb
│   ├── 04_feature_selection_rfecv.ipynb
│   ├── 05_modelo_sparkml_multiclase.ipynb
│   ├── 06_aplicacion_visualizacion_refined.ipynb
│   ├── 07_negocio.ipynb
│   ├── requirements.txt
│   └── README_LOCAL.md
│
├── databricks/
│   ├── 00_configuracion_databricks.py
│   ├── 02_preparacion_trusted_databricks.ipynb
│   ├── 03_eda_sparksql_databricks.ipynb
│   ├── 04_feature_selection_rfecv_databricks.ipynb
│   ├── 05_modelo_sparkml_multiclase_databricks.ipynb
│   ├── 06_aplicacion_visualizacion_refined_databricks.ipynb
│   ├── 07_negocio_databricks.ipynb
│   └── README_DATABRICKS.md
│
├── raw/
│   ├── metadata/
│   └── rnaseq/
│
├── data_local/
│   ├── trusted/
│   ├── refined/
│   └── models/
│
└── README.md
```

La estructura puede adaptarse si los notebooks locales y de Databricks se mantienen en carpetas separadas o si se conservan en una única carpeta. Lo importante es mantener claro qué archivos pertenecen a cada entorno.

---

## Flujo metodológico

El proyecto sigue una arquitectura por capas:

```text
Raw → Trusted → Refined → Models / Visualizations / Business outputs
```

### 1. Raw

Contiene archivos originales descargados desde GDC/TCGA:

- Archivos RNA-Seq.
- Metadatos clínicos y técnicos.
- Manifiestos de descarga.
- Insumos sin transformación analítica profunda.

### 2. Trusted

Contiene datos limpios, estructurados y validados:

- Tabla larga de expresión génica.
- Tabla de muestras.
- Diccionario de genes.
- Matriz muestra-gen.
- Llaves técnicas de unión.
- Validaciones de muestras, genes y clases.

### 3. Refined

Contiene salidas listas para análisis, modelado, visualización y comunicación:

- Tablas EDA.
- Métricas de modelos.
- Predicciones.
- Reportes de clasificación.
- Visualizaciones.
- Exportaciones para prototipo o presentación.

### 4. Models

Contiene objetos asociados al entrenamiento:

- Modelos ajustados.
- Encoders.
- Selectores de características.
- Resultados de evaluación.

---

## Ambientes de ejecución

### Ejecución local

La versión local permite ejecutar el proyecto en un computador personal o entorno Jupyter. Esta versión es útil para:

- Depurar notebooks.
- Probar transformaciones.
- Validar visualizaciones.
- Ejecutar subconjuntos de datos.
- Hacer pruebas de negocio.
- Evitar costos o restricciones de cómputo cloud.

Más detalles en:

```text
README_LOCAL.md
```

### Ejecución en Databricks

La versión Databricks organiza el proyecto como una arquitectura lakehouse sobre Volumes, tablas Delta y procesamiento distribuido con Spark. Esta versión es útil para:

- Representar una arquitectura cloud escalable.
- Usar PySpark y SparkSQL.
- Registrar salidas en capas.
- Simular un escenario productivo de ingeniería de datos.
- Documentar una implementación tipo lakehouse.

Más detalles en:

```text
README_DATABRICKS.md
```

---

## Datos utilizados

El proyecto usa datos abiertos y desidentificados de:

- **The Cancer Genome Atlas (TCGA)**
- **Genomic Data Commons (GDC)**

Clases principales consideradas:

```text
BRCA, KIRC, LUAD, UCEC, THCA, HNSC,
LUSC, PRAD, LGG, COAD, SKCM, STAD,
OV, BLCA, LIHC, GBM, KIRP, CESC
```

---

## Modelos y evaluación

El problema se aborda como una clasificación multiclase. Los modelos se comparan mediante métricas globales y por clase, entre ellas:

- Accuracy.
- Balanced accuracy.
- Precision macro.
- Recall macro.
- F1-score macro.
- Matriz de confusión.
- Errores por clase.

La métrica principal recomendada es **F1-score macro**, porque permite evaluar el desempeño promedio entre clases y reduce el sesgo hacia clases con mayor número de muestras.

---

## Visualización y comunicación

El proyecto genera salidas para interpretación técnica y comunicación ejecutiva:

- Distribución de muestras por clase.
- Resultados de análisis exploratorio.
- Comparación de modelos.
- Métricas por clase.
- Visualizaciones de resultados.
- Tablas refinadas para consumo.
- Escenarios de valor para EPS e IPS.

---

## Análisis de negocio

El notebook `07_negocio` traduce los resultados técnicos a un escenario de valor operativo. El objetivo es mostrar cómo una solución analítica basada en expresión génica y aprendizaje automático podría apoyar a EPS e IPS en:

- Reducción de tiempos de ruta diagnóstica.
- Disminución de reprocesos.
- Priorización de casos.
- Estimación de ahorros.
- Comparación de escenarios por EPS.
- Comunicación del valor potencial de la solución.

Este análisis es una aproximación académica y debe validarse con datos reales antes de cualquier uso operativo.

---

## Consideraciones importantes

- El proyecto utiliza datos abiertos y desidentificados.
- El modelo no reemplaza el criterio médico.
- Los resultados no constituyen una herramienta clínica validada.
- Para uso real se requiere validación clínica, ética, regulatoria y operativa.
- Algunas ejecuciones completas pueden ser costosas en tiempo y recursos, especialmente en Databricks.
- La versión local y la versión Databricks cumplen propósitos complementarios.

---

## Autores

**Equipo Sigma Analytics**

- Juan Manuel Agudelo Olarte
- Miguel Roldan Yepes
- Carlos José Muñoz Cabrera
- Juan Camilo Cataño Zuleta

---

## Uso académico

Este repositorio fue desarrollado con fines académicos en el marco de un proyecto integrador de analítica, aprendizaje automático, visualización e ingeniería de datos.

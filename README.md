# Clasificación de tipos de cáncer con RNA-Seq y aprendizaje automático

Este repositorio contiene el flujo completo del proyecto **Clasificación de tipos de cáncer mediante aprendizaje automático a partir de perfiles de expresión génica derivados de RNA-Seq**. El objetivo es construir una solución analítica reproducible que permita clasificar muestras tumorales de TCGA/GDC a partir de datos transcriptómicos, integrando preparación de datos, análisis exploratorio, selección de características, modelado supervisado, visualización y análisis de valor para negocio.

El proyecto trabaja con datos abiertos y desidentificados de **The Cancer Genome Atlas (TCGA)**, descargados desde **Genomic Data Commons (GDC)**. La unidad de análisis corresponde a muestras tumorales, representadas mediante perfiles de expresión génica. La variable objetivo es el tipo de cáncer asociado a cada muestra.

---

## Objetivo del proyecto

Desarrollar un flujo analítico capaz de:

- Ingerir y organizar datos RNA-Seq y metadatos clínicos de TCGA/GDC.
- Construir una matriz analítica muestra-gen para clasificación multiclase.
- Explorar la distribución de clases, genes, muestras y calidad de los datos.
- Seleccionar genes relevantes para reducir dimensionalidad y mejorar eficiencia.
- Entrenar y evaluar modelos de aprendizaje automático para clasificación de cáncer.
- Generar salidas refinadas para visualización, comunicación y análisis de impacto.
- Estimar escenarios de valor operativo para EPS e IPS, asociados a tiempos, costos y reprocesos de la ruta diagnóstica.

---

## Estructura general del repositorio

```text
proyecto/
├── 00_configuracion.py
├── 01_descarga_ingesta_gdc_raw.ipynb
├── 02_preparacion_trusted.ipynb
├── 03_eda_sparksql.ipynb
├── 04_feature_selection_rfecv.ipynb
├── 05_modelo_sparkml_multiclase.ipynb
├── 06_aplicacion_visualizacion_refined.ipynb
├── 07_negocio.ipynb
├── requirements.txt
├── README.md
├── raw/
│   ├── metadata/
│   └── rnaseq/
└── data_local/
    ├── trusted/
    ├── refined/
    │   ├── tables/
    │   ├── exports/
    │   └── visualizations/
    └── models/
```

---

## Descripción de los notebooks

| Archivo | Descripción |
|---|---|
| `00_configuracion.py` | Define rutas, parámetros globales, clases principales, funciones auxiliares de lectura, escritura, visualización y carga de tablas. |
| `01_descarga_ingesta_gdc_raw.ipynb` | Descarga, organiza e ingesta los archivos originales provenientes de GDC/TCGA. Genera insumos raw y metadatos base. |
| `02_preparacion_trusted.ipynb` | Limpia, transforma y estructura los datos crudos. Construye datasets trusted con muestras, genes y matriz base. |
| `03_eda_sparksql.ipynb` | Realiza análisis exploratorio usando PySpark y SparkSQL: distribución de clases, conteo de genes, muestras, validaciones y salidas EDA. |
| `04_feature_selection_rfecv.ipynb` | Aplica selección de características para reducir dimensionalidad y conservar genes relevantes para el modelado. |
| `05_modelo_sparkml_multiclase.ipynb` | Entrena y evalúa modelos de clasificación multiclase usando SparkML y modelos compatibles. Compara métricas globales y por clase. |
| `06_aplicacion_visualizacion_refined.ipynb` | Prepara tablas refinadas, visualizaciones y archivos de salida para comunicación de resultados y prototipos de consulta. |
| `07_negocio.ipynb` | Construye un análisis de valor orientado a EPS/IPS, estimando impacto potencial en tiempos de atención, costos y reprocesos. |

---

## Flujo metodológico

El flujo sigue una arquitectura por capas:

```text
Raw → Trusted → Refined → Models / Visualizations / Business outputs
```

### 1. Capa Raw

Contiene los archivos originales descargados desde GDC/TCGA:

- Archivos RNA-Seq.
- Metadatos clínicos y técnicos.
- Manifiestos de descarga.
- Insumos sin transformación analítica profunda.

### 2. Capa Trusted

Contiene datos limpios, validados y estructurados:

- Tabla larga de expresión génica.
- Tabla de muestras.
- Diccionario de genes.
- Matriz muestra-gen.
- Llaves técnicas de unión.
- Validaciones de clases, muestras y genes.

### 3. Capa Refined

Contiene salidas listas para análisis, modelado y comunicación:

- Tablas EDA.
- Métricas de modelos.
- Predicciones.
- Reportes de clasificación.
- Archivos exportables.
- Figuras y visualizaciones.

### 4. Capa Models

Contiene objetos serializados y salidas relacionadas con los modelos entrenados:

- Modelos ajustados.
- Encoders.
- Selectores de características.
- Resultados de evaluación.

---

## Datos utilizados

El proyecto utiliza datos de acceso abierto de:

- **The Cancer Genome Atlas (TCGA)**
- **Genomic Data Commons (GDC)**

Las clases principales consideradas son 18 tipos de cáncer:

```text
BRCA, KIRC, LUAD, UCEC, THCA, HNSC,
LUSC, PRAD, LGG, COAD, SKCM, STAD,
OV, BLCA, LIHC, GBM, KIRP, CESC
```

La matriz analítica se construye a partir de perfiles de expresión génica RNA-Seq, donde:

- Cada fila representa una muestra tumoral.
- Cada columna representa un gen o característica derivada.
- La variable objetivo corresponde al tipo de cáncer.

---

## Instalación del entorno

Se recomienda crear un entorno virtual antes de ejecutar los notebooks.

### En macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
jupyter lab
```

### En Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
jupyter lab
```

---

## Requisitos principales

El archivo `requirements.txt` incluye librerías para procesamiento distribuido, análisis, modelado y visualización:

```text
pyspark
pandas
numpy
matplotlib
scikit-learn
xgboost
pyarrow
joblib
jupyterlab
ipykernel
```

---

## Preparación de carpetas

Antes de ejecutar el flujo, ubique los datos crudos en la siguiente estructura:

```text
raw/
├── metadata/
│   └── metadatos_tcga_oficial_18_clases.csv
└── rnaseq/
    └── archivos RNA-Seq / STAR Counts
```

Las salidas se crearán automáticamente en:

```text
data_local/
├── trusted/
├── refined/
│   ├── tables/
│   ├── exports/
│   └── visualizations/
└── models/
```

---

## Orden de ejecución

Ejecute los notebooks en este orden:

1. `00_configuracion.py`
2. `01_descarga_ingesta_gdc_raw.ipynb`
3. `02_preparacion_trusted.ipynb`
4. `03_eda_sparksql.ipynb`
5. `04_feature_selection_rfecv.ipynb`
6. `05_modelo_sparkml_multiclase.ipynb`
7. `06_aplicacion_visualizacion_refined.ipynb`
8. `07_negocio.ipynb`

En los notebooks, la configuración debe cargarse con:

```python
%run ./00_configuracion.py
```

---

## Variables de entorno opcionales

Si las carpetas de datos están en una ubicación diferente, puede configurar rutas manualmente:

```bash
export TCGA_PROJECT_DIR="/ruta/al/proyecto"
export TCGA_RAW_DIR="/ruta/al/proyecto/raw"
export TCGA_RAW_RNASEQ_DIR="/ruta/al/proyecto/raw/rnaseq"
```

En Windows PowerShell:

```powershell
$env:TCGA_PROJECT_DIR="C:\ruta\al\proyecto"
$env:TCGA_RAW_DIR="C:\ruta\al\proyecto\raw"
$env:TCGA_RAW_RNASEQ_DIR="C:\ruta\al\proyecto\raw\rnaseq"
```

---

## Modo de prueba

Para validar el flujo en un computador personal sin ejecutar todo el volumen de datos, puede usar un modo de prueba:

```bash
export TCGA_MODO_PRUEBA_LOCAL=1
```

Para una ejecución más completa:

```bash
export TCGA_MODO_PRUEBA_LOCAL=0
export TCGA_TOP_N_GENES=500
export TCGA_N_FEATURES_RFE=100
export TCGA_MAX_GENES_SPARKML=100
```

Estos valores pueden ajustarse según la memoria disponible y el tamaño del clúster o equipo.

---

## Modelado

El componente de modelado aborda un problema de clasificación multiclase. El desempeño se evalúa mediante métricas globales y por clase, entre ellas:

- Accuracy.
- Balanced accuracy.
- Precision macro.
- Recall macro.
- F1-score macro.
- Matriz de confusión.
- Errores por clase.

La métrica principal recomendada es **F1-score macro**, porque permite evaluar el desempeño promedio entre clases y reduce el sesgo hacia las clases con mayor número de muestras.

---

## Visualización y comunicación

El proyecto genera salidas orientadas a la interpretación técnica y ejecutiva:

- Distribución de muestras por clase.
- Resultados de EDA.
- Métricas comparativas de modelos.
- Predicciones y errores por clase.
- Visualizaciones exportables.
- Insumos para reporte y presentación.
- Análisis de valor potencial para EPS e IPS.

---

## Análisis de negocio

El notebook `07_negocio.ipynb` traduce los resultados técnicos a un escenario de valor operativo en salud. Su objetivo no es reemplazar la validación clínica, sino construir una aproximación analítica para estimar cómo una solución basada en expresión génica y aprendizaje automático podría apoyar:

- Priorización diagnóstica.
- Reducción de reprocesos.
- Disminución de tiempos en la ruta diagnóstica.
- Estimación de ahorros potenciales.
- Comparación de escenarios por EPS.
- Comunicación del valor de la solución a actores de salud.

---

## Consideraciones

- El proyecto usa datos abiertos y desidentificados.
- El modelo no constituye una herramienta clínica validada.
- Los resultados deben interpretarse como un ejercicio académico y analítico.
- Para uso real, sería necesaria validación clínica, regulatoria, operativa y ética.
- El análisis de negocio usa supuestos simulados o parametrizados y debe ajustarse con datos reales de EPS/IPS antes de una implementación productiva.

---

## Autores

**Equipo Sigma Analytics**

- Juan Manuel Agudelo Olarte
- Miguel Roldan Yepes
- Carlos José Muñoz Cabrera
- Juan Camilo Cataño Zuleta

---

## Licencia y uso

Este repositorio se desarrolla con fines académicos. Los datos utilizados provienen de fuentes abiertas de investigación biomédica y deben usarse respetando las condiciones de uso de TCGA/GDC.

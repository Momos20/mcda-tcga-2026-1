# Ejecución local — Proyecto TCGA/RNA-Seq

Este documento describe la ejecución local del proyecto de clasificación de tipos de cáncer con datos RNA-Seq.

La versión local permite ejecutar, probar y depurar el flujo completo en un entorno Jupyter sin depender de Databricks. Es especialmente útil cuando existen restricciones de cómputo cloud, costos, tiempos de ejecución o problemas de configuración del clúster.

---

## Archivos principales

```text
00_configuracion.py
01_descarga_ingesta_gdc_raw.ipynb
02_preparacion_trusted.ipynb
03_eda_sparksql.ipynb
04_feature_selection_rfecv.ipynb
05_modelo_sparkml_multiclase.ipynb
06_aplicacion_visualizacion_refined.ipynb
07_negocio.ipynb
requirements.txt
README_LOCAL.md
```

---

## Instalación

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
jupyter lab
```

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
jupyter lab
```

---

## Dependencias

El archivo `requirements.txt` recomendado es:

```text
pyspark>=3.5,<4
pandas>=2.0
numpy>=1.24,<2.0
matplotlib>=3.7
scikit-learn>=1.3
xgboost>=2.0
pyarrow>=12
joblib>=1.3
requests>=2.31
optuna>=3.5
openTSNE>=1.0
jupyterlab>=4
ipykernel>=6
```

---

## Estructura esperada

```text
proyecto/
├── raw/
│   ├── metadata/
│   │   └── metadatos_tcga_oficial_18_clases.csv
│   └── rnaseq/
│       └── archivos RNA-Seq / STAR Counts
├── data_local/
│   ├── trusted/
│   ├── refined/
│   │   ├── tables/
│   │   ├── exports/
│   │   └── visualizations/
│   └── models/
├── 00_configuracion.py
├── 01_descarga_ingesta_gdc_raw.ipynb
├── 02_preparacion_trusted.ipynb
├── 03_eda_sparksql.ipynb
├── 04_feature_selection_rfecv.ipynb
├── 05_modelo_sparkml_multiclase.ipynb
├── 06_aplicacion_visualizacion_refined.ipynb
└── 07_negocio.ipynb
```

---

## Orden de ejecución

1. `00_configuracion.py`
2. `01_descarga_ingesta_gdc_raw.ipynb`
3. `02_preparacion_trusted.ipynb`
4. `03_eda_sparksql.ipynb`
5. `04_feature_selection_rfecv.ipynb`
6. `05_modelo_sparkml_multiclase.ipynb`
7. `06_aplicacion_visualizacion_refined.ipynb`
8. `07_negocio.ipynb`

Los notebooks deben cargar la configuración con:

```python
%run ./00_configuracion.py
```

---

## Variables de entorno opcionales

Si las carpetas están en otra ubicación:

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

Para validar el flujo sin consumir demasiados recursos:

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

---

## Salidas generadas

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

## Recomendaciones

- Ejecute primero en modo prueba.
- No convierta DataFrames grandes completos a pandas.
- Revise la memoria disponible antes del modelado.
- Mantenga las carpetas `raw`, `trusted`, `refined` y `models` ordenadas.
- Use la versión local para depurar antes de llevar cambios a Databricks.

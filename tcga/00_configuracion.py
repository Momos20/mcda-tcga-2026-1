# 00_configuracion_local.py
# Espejo de 00_configuracion_local.ipynb (mismo contenido en .py para %run local)
# Usar con: %run ./00_configuracion_local.py

# Entorno para Spark en Windows local; en Databricks/Linux se omite y no pisa lo ya definido
import os, sys
if os.name == "nt":
    os.environ.setdefault("JAVA_HOME",   r"C:\Program Files\Microsoft\jdk-17.0.19.10-hotspot")
    os.environ.setdefault("HADOOP_HOME", r"C:\hadoop")
    os.environ["PATH"] = os.path.join(os.environ["HADOOP_HOME"], "bin") + os.pathsep + os.environ.get("PATH", "")
    _python = sys.executable
    if " " in _python:
        import subprocess
        _python = subprocess.check_output(
            f'for %I in ("{_python}") do @echo %~sI', shell=True
        ).decode().strip()
    os.environ.setdefault("PYSPARK_PYTHON", _python)
    os.environ.setdefault("PYSPARK_DRIVER_PYTHON", _python)
os.environ.setdefault("SPARK_LOCAL_IP", "127.0.0.1")


from pathlib import Path
import os, shutil, warnings, gc
import pandas as pd
import numpy as np

try:
    display
except NameError:
    from IPython.display import display

PROJECT_DIR = Path(os.getenv("TCGA_PROJECT_DIR", Path.cwd())).resolve()
RAW_DIR = Path(os.getenv("TCGA_RAW_DIR", PROJECT_DIR / "raw")).resolve()
LOCAL_DATA_DIR = Path(os.getenv("TCGA_LOCAL_DATA_DIR", PROJECT_DIR / "data_local")).resolve()

TRUSTED_PATH = LOCAL_DATA_DIR / "trusted"
REFINED_PATH = LOCAL_DATA_DIR / "refined"
MODELS_PATH = LOCAL_DATA_DIR / "models"
REFINED_TABLES_PATH = REFINED_PATH / "tables"
REFINED_EXPORTS_PATH = REFINED_PATH / "exports"
REFINED_VISUALIZATIONS_PATH = REFINED_PATH / "visualizations"

TRUSTED_LONG_PATH = TRUSTED_PATH / "trusted_tcga_rnaseq_long_18_clases"
TRUSTED_SAMPLES_PATH = TRUSTED_PATH / "trusted_tcga_samples_18_clases"
TRUSTED_GENES_PATH = TRUSTED_PATH / "trusted_tcga_gene_dictionary"

for p in [TRUSTED_PATH, REFINED_TABLES_PATH, REFINED_EXPORTS_PATH, REFINED_VISUALIZATIONS_PATH, MODELS_PATH]:
    p.mkdir(parents=True, exist_ok=True)

def first_existing(candidates):
    for c in candidates:
        c = Path(c)
        if c.exists():
            return c.resolve()
    return None

RAW_METADATA_FILE = first_existing([
    RAW_DIR / "metadata" / "metadatos_tcga_oficial_18_clases.csv",
    RAW_DIR / "metadatos_tcga_oficial_18_clases.csv",
])

RAW_RNASEQ_PATH = (
    Path(os.getenv("TCGA_RAW_RNASEQ_DIR")).resolve()
    if os.getenv("TCGA_RAW_RNASEQ_DIR")
    else first_existing([RAW_DIR / "rnaseq", RAW_DIR / "RNASeq", RAW_DIR / "rna_seq", RAW_DIR])
)

CLASES_PRINCIPALES = [
    "BRCA", "KIRC", "LUAD", "UCEC", "THCA", "HNSC",
    "LUSC", "PRAD", "LGG", "COAD", "SKCM", "STAD",
    "OV", "BLCA", "LIHC", "GBM", "KIRP", "CESC"
]
SEED = 42

print("PROJECT_DIR:", PROJECT_DIR)
print("RAW_DIR:", RAW_DIR)
print("RAW_METADATA_FILE:", RAW_METADATA_FILE)
print("RAW_RNASEQ_PATH:", RAW_RNASEQ_PATH)
print("LOCAL_DATA_DIR:", LOCAL_DATA_DIR)


from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = (
    SparkSession.builder
    .appName("tcga-cancer-ml-local")
    .master(os.getenv("SPARK_MASTER", "local[*]"))
    .config("spark.sql.shuffle.partitions", os.getenv("SPARK_SQL_SHUFFLE_PARTITIONS", "64"))
    .config("spark.driver.memory", os.getenv("SPARK_DRIVER_MEMORY", "8g"))
    .config("spark.driver.host", os.getenv("SPARK_DRIVER_HOST", "127.0.0.1"))
    .config("spark.driver.bindAddress", os.getenv("SPARK_DRIVER_BIND_ADDRESS", "127.0.0.1"))
    .config("spark.driver.maxResultSize", os.getenv("SPARK_DRIVER_MAX_RESULT_SIZE", "2g"))
    .config("spark.network.timeout", os.getenv("SPARK_NETWORK_TIMEOUT", "800s"))
    .config("spark.executor.heartbeatInterval", os.getenv("SPARK_EXECUTOR_HEARTBEAT_INTERVAL", "60s"))
    .config("spark.sql.execution.arrow.pyspark.enabled", os.getenv("SPARK_ARROW_ENABLED", "true"))
    .getOrCreate()
)
spark.sparkContext.setLogLevel(os.getenv("SPARK_LOG_LEVEL", "WARN"))
print("Spark:", spark.version)


def path_str(path):
    return str(Path(path).resolve())

def mostrar(obj, n=10):
    if hasattr(obj, "limit") and hasattr(obj, "toPandas"):
        return display(obj.limit(n).toPandas())
    return display(obj)

def table_path(nombre_tabla):
    return REFINED_TABLES_PATH / nombre_tabla

def table_exists_local(nombre_tabla):
    return table_path(nombre_tabla).exists()

def save_spark_table(df, nombre_tabla, partition_by=None, export_csv=True, csv_max_rows=200000):
    ruta = table_path(nombre_tabla)
    if ruta.exists():
        shutil.rmtree(ruta)

    writer = df.write.mode("overwrite")
    if partition_by:
        writer.partitionBy(*partition_by).parquet(path_str(ruta))
    else:
        writer.parquet(path_str(ruta))

    if export_csv:
        try:
            n = df.count()
            if n <= csv_max_rows:
                df.toPandas().to_csv(REFINED_EXPORTS_PATH / f"{nombre_tabla}.csv", index=False)
        except Exception as e:
            print(f"No se exportó CSV para {nombre_tabla}: {e}")

    print("Tabla local guardada:", ruta)
    return ruta

def load_spark_table(nombre_tabla):
    ruta = table_path(nombre_tabla)
    if not ruta.exists():
        raise FileNotFoundError(f"No existe la tabla local: {ruta}")
    return spark.read.parquet(path_str(ruta))

def save_trusted(df, path, partition_by=None):
    path = Path(path)
    if path.exists():
        shutil.rmtree(path)

    writer = df.write.mode("overwrite")
    if partition_by:
        writer.partitionBy(*partition_by).parquet(path_str(path))
    else:
        writer.parquet(path_str(path))

    print("Dataset trusted guardado:", path)
    return path

def read_trusted(path):
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"No existe el dataset trusted: {path}")
    return spark.read.parquet(path_str(path))

def guardar_figura(nombre_archivo, dpi=300):
    import matplotlib.pyplot as plt
    ruta = REFINED_VISUALIZATIONS_PATH / nombre_archivo
    plt.savefig(ruta, dpi=dpi, bbox_inches="tight")
    print("Figura guardada:", ruta)
    return ruta

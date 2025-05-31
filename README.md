Aquí tienes un `README.md` diseñado para tu proyecto `TALLER_AHH1`, orientado a análisis de encuestas con codificación, validación y exploración:

```markdown
# TALLER_AHH1

Este proyecto tiene como objetivo el procesamiento, codificación y análisis exploratorio de una encuesta aplicada a estudiantes, con foco en su relación con la intención de cambiarse o retirarse de su carrera.

---

## 📁 Estructura del Proyecto

```

TALLER\_AHH1/
├── data/                   # Datos en distintas fases del procesamiento
│   ├── raw/               # Datos originales (CSV, JSON, YAML)
│   ├── interim/           # Datos procesados parcialmente
│   └── processed/         # Datos listos para análisis
├── notebooks/
│   └── exploracion.marimo.py   # Exploración por pregunta usando Marimo
├── scripts/
│   └── run\_pipeline.py    # Ejecución principal del pipeline
├── src/
│   └── taller\_utils/      # Funciones reutilizables (ETL, análisis, visualización)
│       ├── encoding.py
│       ├── analysis.py
│       ├── helpers.py
│       └── visuals.py
├── tests/                 # Tests unitarios
├── pyproject.toml         # Configuración del entorno (uv + editable install)
└── README.md              # Este archivo

````

---

## ⚙️ Instalación

```bash
uv venv .venv
source .venv/bin/activate
uv pip install -e .
uv pip install pytest marimo
````

---

## 🚀 Ejecutar el procesamiento

```bash
python scripts/run_pipeline.py
```

Esto:

* Carga los datos desde `data/raw/encuesta.csv`
* Aplica codificación definida en `encodings.yaml` o `.json`
* Genera el archivo codificado: `data/processed/encuesta_codificada.csv`

---

## 🔬 Exploración con Marimo

El análisis exploratorio se realiza mediante `notebooks/exploracion.marimo.py`.

Para ejecutarlo:

```bash
marimo run notebooks/exploracion.marimo.py
```

Incluye:

* Comparaciones por pregunta respecto al target
* Test estadísticos (Mann–Whitney, Chi²)
* Visualizaciones automáticas

---

## 🧪 Ejecutar tests

```bash
pytest
```

Incluye tests para funciones como:

* `process_survey_data`
* `load_yaml_encodings`
* Manejo de valores no mapeados

---

## ✍️ Autor

Desarrollado por Iair Linker para el análisis de hábitos y motivaciones estudiantiles.

```
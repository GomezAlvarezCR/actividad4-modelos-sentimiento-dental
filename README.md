# Actividad 4 — Comparación de modelos para análisis de sentimiento dental

Proyecto académico del curso **Gestión de Proyectos de Inteligencia Artificial** (Universidad Tecmilenio, octubre de 2026). Se compararon **tres modelos preentrenados de Hugging Face** para clasificar 120 reseñas simuladas de atención odontológica en español como positivas (`POS`), neutrales (`NEU`) o negativas (`NEG`).

> **Alcance:** prototipo de análisis de opiniones; las reseñas fueron elaboradas para esta actividad y **no provienen de pacientes reales**. El sistema no se ha validado para uso clínico o comercial.

## Ecosistema Hugging Face y selección

- **Models:** repositorio de checkpoints y tokenizadores usados para realizar inferencia.
- **Datasets:** herramientas de gestión de conjuntos de datos; aquí se evaluó un CSV propio, no un dataset publicado en el Hub.
- **Spaces:** servicio de demostraciones interactivas; no se implementó un Space porque se solicitó un prototipo en Colab.

Se compararon tres modelos de clasificación triclase, considerando compatibilidad con español, métricas de calidad, recursos y licencia:

1. **RoBERTuito:** [`pysentimiento/robertuito-sentiment-analysis`](https://huggingface.co/pysentimiento/robertuito-sentiment-analysis), especializado en español.
2. **XLM-RoBERTa:** [`cardiffnlp/twitter-xlm-roberta-base-sentiment`](https://huggingface.co/cardiffnlp/twitter-xlm-roberta-base-sentiment), multilingüe.
3. **DistilBERT:** [`lxyuan/distilbert-base-multilingual-cased-sentiments-student`](https://huggingface.co/lxyuan/distilbert-base-multilingual-cased-sentiments-student), alternativa destilada.

Se normalizaron las etiquetas originales de los tres modelos a `NEG`, `NEU` y `POS` antes de calcular métricas. **No se realizó fine-tuning.**

## Datos y estructura

- **Dataset:** [`resenas_dentales_simuladas.csv`](resenas_dentales_simuladas.csv) con 120 reseñas en español, 40 por clase y 10 temáticas.
- **Diccionario y procedencia:** [`docs/DICCIONARIO_DATOS.md`](docs/DICCIONARIO_DATOS.md).
- **Reproducción del CSV:** `python src/generar_dataset.py` (semilla fija 42). El script reescribe el CSV de la raíz con el mismo contenido de origen; si se modifica el CSV manualmente, guardar una copia antes.
- Las columnas son `id`, `texto`, `etiqueta`, `tema` y `origen` (`simulado`).

## Resultados medidos en Google Colab (GPU Tesla T4)

| Modelo | Accuracy | Precision macro | Recall macro | F1 macro | ms/reseña en lote | GPU pico MB |
|---|---:|---:|---:|---:|---:|---:|
| **XLM-RoBERTa** | **87.50%** | **90.38%** | **87.50%** | **87.73%** | 1.689 | 1,087 |
| RoBERTuito | 84.17% | 88.73% | 84.17% | 84.18% | 4.048 | **435** |
| DistilBERT | 47.50% | 36.88% | 47.50% | 40.91% | **1.168** | 543 |

La inferencia se midió en **lotes de 16 reseñas**, con tres repeticiones cronometradas tras un calentamiento; los tiempos excluyen descarga/carga del modelo y **no son latencias de una solicitud individual**.

**Hallazgos:** XLM-RoBERTa obtuvo el mayor F1 macro y es el candidato principal para este prototipo supervisado. RoBERTuito tuvo mayor recall de comentarios negativos (87.5% frente a 82.5% de XLM-RoBERTa) y menor consumo de memoria. DistilBERT no clasificó correctamente **ninguna de las 40 reseñas neutrales**, por lo que no se recomienda bajo estas condiciones.

Ver [`results/comparacion_modelos.csv`](results/comparacion_modelos.csv), [`results/tradeoff_f1_latencia.png`](results/tradeoff_f1_latencia.png), matrices de confusión y las predicciones individuales en la carpeta [`results/`](results/).

## Cómo ejecutar el notebook

1. Abrir [Google Colab](https://colab.research.google.com/) y cargar **`Actividad_4.ipynb`**, ubicado en la raíz del repositorio.
2. En **Entorno de ejecución → Cambiar tipo de entorno de ejecución**, elegir **GPU T4** (o la GPU disponible).
3. Ejecutar las celdas en orden: comprobación de GPU, instalación, autenticación opcional y lectura de datos. Si Colab solicita reinicio del entorno después de la instalación, reiniciar antes de continuar.
4. Los modelos son públicos: **no hace falta un token**. Si se emplea uno, introducirlo mediante **Secrets (`HF_TOKEN`)**; nunca publicar el token en GitHub.
5. Cuando el notebook lo solicite, subir **`resenas_dentales_simuladas.csv`** (archivo de la raíz).
6. Esperar la evaluación de tres modelos y revisar gráficos, matrices de confusión y reporte por clases. El notebook descarga un ZIP de resultados y guarda archivos en `results/`.

Para consultar versiones, entorno, semilla, parámetros y revisiones de los modelos utilizados en el experimento realizado, ver [`results/entorno_y_reproducibilidad.json`](results/entorno_y_reproducibilidad.json). Entorno registrado: Python 3.13.15, PyTorch 2.11.0+cu130, Transformers 4.57.6 y scikit-learn 1.6.1. Las versiones que Colab proporcione en futuras sesiones podrían variar.

## Archivos principales

```text
actividad4-modelos-sentimiento-dental/
├── README.md
├── requirements.txt
├── Actividad_4.ipynb
├── resenas_dentales_simuladas.csv
├── Actividad 4 - Christopher Gomez.pdf
├── docs/
│   └── DICCIONARIO_DATOS.md
├── src/
│   └── generar_dataset.py
└── results/
    ├── comparacion_modelos.csv
    ├── entorno_y_reproducibilidad.json
    ├── tradeoff_f1_latencia.png
    ├── comparacion_metricas.png
    ├── matriz_*.png
    ├── predicciones_*.csv
    └── errores_*.csv
```

## Limitaciones, riesgos y mantenimiento

El dataset es sintético y pequeño; puede no representar ironía, regionalismos o la distribución de sentimientos de pacientes reales. Antes de implementar, es imprescindible evaluar reseñas externas representativas, anonimizar cualquier dato personal, establecer revisión humana de quejas, y revisar licencias. El Hub no reportó licencia para XLM-RoBERTa ni RoBERTuito en los metadatos descargados, por lo que la posibilidad de uso comercial **no está confirmada**. No sustituye decisiones clínicas.

Para mantener reproducibilidad: conservar los checkpoints identificados por SHA en el manifiesto de resultados, documentar versiones de dependencias y reevaluar tras cualquier actualización. El código está dividido en celdas y guarda predicciones y errores por clase.

## Referencias

- [Hugging Face — Models](https://huggingface.co/models), [Datasets](https://huggingface.co/datasets) y [Spaces](https://huggingface.co/spaces).
- [Documentación de Google Colab](https://colab.research.google.com/notebooks/intro.ipynb).
- Universidad Tecmilenio (2026). *Tema 9: Selección de modelos preentrenados* y *Tema 10: Prototipado rápido y documentación técnica* (materiales del curso).

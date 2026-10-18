# Dataset: reseñas dentales simuladas

- **Archivo:** `resenas_dentales_simuladas.csv`
- **Origen:** elaboración propia mediante redacción manual de ejemplos simulados para fines educativos, no recopilados de Google, Facebook ni de pacientes reales.
- **Cobertura:** 120 textos originales en español; 40 `POS`, 40 `NEU` y 40 `NEG`.
- **Temáticas:** atención, tiempos, resultados, explicaciones, costos, instalaciones, citas, molestias, seguimiento y pagos. Cada tema tiene 4 textos de cada clase.
- **Fecha de elaboración:** octubre de 2026.
- **Reproducción:** ejecutar `python src/generar_dataset.py` desde el directorio raíz del proyecto (o ejecutar el script directamente). La semilla fija 42 produce el mismo orden.

## Esquema

| Campo | Tipo | Definición |
| --- | --- | --- |
| `id` | texto | Identificador consecutivo `R001` a `R120` (sin vínculo con personas). |
| `texto` | texto UTF-8 | Opinión o descripción simulada de una experiencia odontológica. |
| `etiqueta` | categoría | Sentimiento global anotado manualmente: `POS` positivo, `NEU` neutral, `NEG` negativo. |
| `tema` | categoría | Aspecto principal de la reseña para análisis de errores. |
| `origen` | categoría | Valor constante `simulado` para indicar procedencia sintética. |

## Criterios de anotación

- **POS:** la valoración global del servicio o experiencia es favorable; puede mencionar pequeños inconvenientes.
- **NEU:** describe procedimientos, fechas o información sin una valoración general clara.
- **NEG:** expresa insatisfacción o preocupación respecto a la experiencia; puede reconocer un aspecto positivo secundario.
- Las etiquetas son **referencias de evaluación** del proyecto, no predicciones del modelo.

## Limitaciones y consideraciones éticas

No se incluyen nombres, fechas exactas de consulta, expedientes ni datos reales de pacientes. El dataset es un conjunto ilustrativo pequeño, redactado manualmente, y no representa la distribución real de reseñas clínicas. Puede contener regularidades léxicas y estilos de escritura que sobreestimen el rendimiento. No debe emplearse para evaluar calidad clínica, diagnosticar, automatizar decisiones odontológicas ni reclamar generalización real sin validación en comentarios consentidos y anonimizados. No hay datos de entrenamiento: se usa exclusivamente para **evaluar inferencia zero-shot/transferencia sin fine-tuning** de tres modelos preentrenados.

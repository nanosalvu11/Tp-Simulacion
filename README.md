# TP 1.1 - Simulación de una Ruleta

Repositorio del TP 1 de la materia Simulación - Universidad Tecnológica Nacional FRRO

## Descripción

Programa en Python que simula el funcionamiento del plato de una ruleta y realiza análisis estadístico mediante simulaciones repetidas. Genera gráficas de frecuencia relativa, media, varianza y desvío estándar comparando los valores observados con los teóricos.

## Requisitos

- Python 3.x
- matplotlib
- argparse (incluido en Python)

### Instalación de dependencias

```bash
pip install matplotlib
```

## Ejecución

### Sintaxis básica

```bash
python Simulacion.py -t TIRADAS -c CORRIDAS -n NUMERO_ELEGIDO
```

### Parámetros

- `-t, --tiradas`: Cantidad de tiradas por corrida (número entero positivo)
- `-c, --corridas`: Cantidad de corridas a realizar (número entero positivo)
- `-n, --numero`: Número elegido de la ruleta (0-36)

### Ejemplos de uso

**Ejemplo 1: Simulación simple**
```bash
python Simulacion.py -t 1000 -c 3 -n 15
```
Ejecuta 3 corridas de 1000 tiradas cada una, apostando al número 15.

**Ejemplo 2: Simulación con más corridas**
```bash
python Simulacion.py -t 500 -c 5 -n 0
```
Ejecuta 5 corridas de 500 tiradas cada una, apostando al número 0 (cero).

**Ejemplo 3: Simulación extendida**
```bash
python Simulacion.py -t 2000 -c 10 -n 27
```
Ejecuta 10 corridas de 2000 tiradas cada una para un análisis más profundo.

## Salida del programa

El programa genera:

1. **Resumen en consola** con estadísticas de cada corrida:
   - Cantidad de aciertos
   - Frecuencia relativa final
   - Media, Varianza y Desvío estándar

2. **8 gráficas en formato PNG** guardadas en la carpeta `graficas/`:
   - `01_FR_Corrida*.png` - Frecuencia Relativa por corrida
   - `02_Media_Corrida*.png` - Media por corrida
   - `03_Varianza_Corrida*.png` - Varianza por corrida
   - `04_Desvio_Corrida*.png` - Desvío Estándar por corrida
   - `05_FR_Comparativa.png` - Comparativa de Frecuencia Relativa
   - `06_Media_Comparativa.png` - Comparativa de Media
   - `07_Varianza_Comparativa.png` - Comparativa de Varianza
   - `08_Desvio_Comparativa.png` - Comparativa de Desvío

3. **Resumen final** con estadísticas generales

## Conceptos teóricos

### Parámetros de la ruleta simulada

- **Rango de números**: 0 a 36 (37 posibilidades)
- **Probabilidad teórica de acertar**: 1/37 ≈ 2.7027%
- **Media teórica**: 18
- **Varianza teórica**: 114
- **Desvío estándar teórico**: √114 ≈ 10.677

### Estadísticos calculados

- **Frecuencia relativa**: Proporción de aciertos acumulada
- **Media**: Promedio acumulado de los números obtenidos
- **Varianza**: Medida de dispersión alrededor de la media
- **Desvío estándar**: Raíz cuadrada de la varianza

## Archivos

- `Simulacion.py` - Programa principal
- `README.md` - Este archivo
- `graficas/` - Carpeta donde se guardan las gráficas generadas

## Nota

Este es un trabajo educativo que implementa conceptos de simulación, probabilidad y estadística.

import random
import numpy as np
import math
import pandas as pd
import matplotlib.pyplot as plt

# --- 1. GENERADORES PSEUDOALEATORIOS ---

# Generador Congruencial Lineal (GCL)
def gcl(semilla, a, c, m, n):
    x = semilla
    return [((x := (a * x + c) % m) / m) for _ in range(n)]

# Método de los Cuadrados Medios
def cuadrados_medios(semilla, n):
    x = semilla
    res = []
    for _ in range(n):
        s = str(x**2).zfill(8)
        x = int(s[2:6])  # Toma los 4 dígitos centrales
        res.append(x / 9999) # Normaliza entre 0 y 1
    return res

# --- 2. TESTS ESTADÍSTICOS ---

# Test de Chi-Cuadrado (Uniformidad)
def test_chi_cuadrado(datos, k=10):
    frec_obs, _ = np.histogram(datos, bins=k, range=(0, 1))
    frec_esp = len(datos) / k
    chi2 = sum((o - frec_esp)**2 / frec_esp for o in frec_obs)
    return round(chi2, 3)

# Test de Rachas (Independencia)
def test_rachas(datos):
    rachas = 1
    for i in range(1, len(datos)):
        # Compara si la tendencia (sube/baja) cambió
        if (datos[i] > datos[i-1]) != (datos[i-1] > datos[i-2] if i > 1 else True):
            rachas += 1
    n = len(datos)
    esperado = (2 * n - 1) / 3
    varianza = (16 * n - 29) / 90
    z = (rachas - esperado) / math.sqrt(varianza)
    return round(abs(z), 3)

# Test de Medias (Z-score)
def test_medias(datos):
    media = np.mean(datos)
    z = (media - 0.5) * math.sqrt(12 * len(datos))
    return round(abs(z), 3)

# Test de Varianza (Chi-Cuadrado)
def test_varianza(datos):
    var = np.var(datos, ddof=1)
    n = len(datos)
    chi2 = ((n - 1) * var) / (1/12)
    return round(chi2, 3)

# --- 3. EJECUCIÓN Y COMPARACIÓN ---

N = 1000 # Cantidad de números a generar

# Generar secuencias
nums_gcl = gcl(12345, 1103515245, 12345, 2**31, N)
nums_cm = cuadrados_medios(5432, N)
nums_py = [random.random() for _ in range(N)]

# Armar tabla de resultados
resultados = {
    "Generador": ["GCL", "Cuadrados Medios", "Python (Mersenne)"],
    "Tipo de Generador": ["Pseudoaleatorio", "Pseudoaleatorio", "Pseudoaleatorio"],
    "Chi2 (Uniformidad)": [test_chi_cuadrado(nums_gcl), test_chi_cuadrado(nums_cm), test_chi_cuadrado(nums_py)],
    "Rachas (Z)": [test_rachas(nums_gcl), test_rachas(nums_cm), test_rachas(nums_py)],
    "Medias (Z)": [test_medias(nums_gcl), test_medias(nums_cm), test_medias(nums_py)],
    "Varianza (Chi2)": [test_varianza(nums_gcl), test_varianza(nums_cm), test_varianza(nums_py)]
}

df = pd.DataFrame(resultados)

print("\n--- RESULTADOS DE LOS TESTS ---")
print(df.to_string(index=False))
print("-------------------------------\n")

# --- 4. GRÁFICOS COMPARATIVOS ---

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

# Gráfico para GCL
ax1.scatter(nums_gcl[:-1], nums_gcl[1:], s=1, color='black', alpha=0.5)
ax1.set_title('Generador GCL')
ax1.axis('off')

# Gráfico para Python (Mersenne Twister)
ax2.scatter(nums_py[:-1], nums_py[1:], s=1, color='black', alpha=0.5)
ax2.set_title('Python random()')
ax2.axis('off')

plt.tight_layout()
plt.show()
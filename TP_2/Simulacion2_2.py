import math
import random
import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# GENERADOR BASE U(0,1)
# ==========================================
def u():
    return random.random()

# ==========================================
# 1. UNIFORME (Continua)
# ==========================================
def generar_uniforme(a, b):
    return a + (b - a) * u()

# ==========================================
# 2. EXPONENCIAL (Continua)
# ==========================================
def generar_exponencial(lambd):
    return -(1.0 / lambd) * math.log(u())

# ==========================================
# 3. GAMMA (Continua)
# ==========================================
def generar_gamma(k, theta):
    """Generador Gamma (para k entero) sumando k exponenciales"""
    suma_exponenciales = 0
    for _ in range(k):
        suma_exponenciales += generar_exponencial(1.0 / theta)
    return suma_exponenciales

# ==========================================
# 4. NORMAL (Continua)
# ==========================================
def generar_normal(mu, sigma):
    u1, u2 = u(), u()
    z0 = math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)
    return z0 * sigma + mu

# ==========================================
# 5. PASCAL / BINOMIAL NEGATIVA (Discreta)
# ==========================================
def generar_pascal(r, p):
    """Cantidad de fracasos antes de obtener 'r' éxitos"""
    exitos = 0
    fracasos = 0
    while exitos < r:
        if u() <= p:
            exitos += 1
        else:
            fracasos += 1
    return fracasos

# ==========================================
# 6. BINOMIAL (Discreta)
# ==========================================
def generar_binomial(n, p):
    exitos = 0
    for _ in range(n):
        if u() <= p:
            exitos += 1
    return exitos

# ==========================================
# 7. HIPERGEOMÉTRICA (Discreta)
# ==========================================
def generar_hipergeometrica(N, K, n):
    """N: Población total, K: Éxitos en la población, n: Muestra a extraer"""
    exitos = 0
    poblacion_restante = N
    exitos_restantes = K
    for _ in range(n):
        probabilidad_exito = exitos_restantes / poblacion_restante
        if u() <= probabilidad_exito:
            exitos += 1
            exitos_restantes -= 1
        poblacion_restante -= 1
    return exitos

# ==========================================
# 8. POISSON (Discreta)
# ==========================================
def generar_poisson(lambd):
    L = math.exp(-lambd)
    k = 0
    p = 1.0
    while p > L:
        k += 1
        p *= u()
    return k - 1

# ==========================================
# 9. EMPÍRICA DISCRETA (Discreta)
# ==========================================
def generar_empirica_discreta(valores, probabilidades):
    numero_aleatorio = u()
    acumulada = 0.0
    for val, prob in zip(valores, probabilidades):
        acumulada += prob
        if numero_aleatorio <= acumulada:
            return val
    return valores[-1]

# ==========================================
# ZONA DE TESTEO Y GRÁFICOS (AL PIE DE LA LETRA)
# ==========================================
print("Generando gráficos. Cerrá cada ventana para ver la siguiente.")

n_muestras = 10000

# --- 1. UNIFORME (Continua con Curva) ---
a, b = 10, 20
muestras_uni = [generar_uniforme(a, b) for _ in range(n_muestras)]
plt.figure(figsize=(8, 5))
plt.hist(muestras_uni, bins=30, color='skyblue', edgecolor='black', density=True, alpha=0.7, label='Empírica (Generador)')
x_uni = np.linspace(a - 1, b + 1, 100)
y_uni = [1/(b-a) if a <= x <= b else 0 for x in x_uni]
plt.plot(x_uni, y_uni, 'r-', lw=2, label='Teórica (Curva)')
plt.title(f"Distribución Uniforme a={a}, b={b}")
plt.legend()
plt.show()

# --- 2. EXPONENCIAL (Continua con Curva) ---
lambd_exp = 0.5
muestras_exp = [generar_exponencial(lambd_exp) for _ in range(n_muestras)]
plt.figure(figsize=(8, 5))
plt.hist(muestras_exp, bins=50, color='lightgreen', edgecolor='black', density=True, alpha=0.7, label='Empírica')
x_exp = np.linspace(0, max(muestras_exp), 100)
y_exp = lambd_exp * np.exp(-lambd_exp * x_exp)
plt.plot(x_exp, y_exp, 'r-', lw=2, label='Teórica (Curva)')
plt.title(f"Distribución Exponencial $\lambda$={lambd_exp}")
plt.legend()
plt.show()

# --- 3. GAMMA (Continua con Curva) ---
k_gamma, theta_gamma = 3, 2.0 
muestras_gamma = [generar_gamma(k_gamma, theta_gamma) for _ in range(n_muestras)]
plt.figure(figsize=(8, 5))
plt.hist(muestras_gamma, bins=50, color='orange', edgecolor='black', density=True, alpha=0.7, label='Empírica')
x_gam = np.linspace(0, max(muestras_gamma), 100)
y_gam = (x_gam**(k_gamma-1) * np.exp(-x_gam/theta_gamma)) / (math.factorial(k_gamma-1) * theta_gamma**k_gamma)
plt.plot(x_gam, y_gam, 'r-', lw=2, label='Teórica (Curva)')
plt.title(f"Distribución Gamma k={k_gamma}, $\\theta$={theta_gamma}")
plt.legend()
plt.show()

# --- 4. NORMAL (Continua con Curva) ---
mu_nor, sigma_nor = 0, 1
muestras_nor = [generar_normal(mu_nor, sigma_nor) for _ in range(n_muestras)]
plt.figure(figsize=(8, 5))
plt.hist(muestras_nor, bins=50, color='salmon', edgecolor='black', density=True, alpha=0.7, label='Empírica')
x_nor = np.linspace(min(muestras_nor), max(muestras_nor), 100)
y_nor = (1/(sigma_nor * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x_nor - mu_nor) / sigma_nor)**2)
plt.plot(x_nor, y_nor, 'r-', lw=2, label='Teórica (Curva)')
plt.title(f"Distribución Normal $\mu$={mu_nor}, $\sigma$={sigma_nor}")
plt.legend()
plt.show()

# --- 5. PASCAL (Discreta - Barras) ---
r_pas, p_pas = 5, 0.5
muestras_pas = [generar_pascal(r_pas, p_pas) for _ in range(n_muestras)]
plt.figure(figsize=(8, 5))
bins_pas = np.arange(0, max(muestras_pas) + 2) - 0.5
plt.hist(muestras_pas, bins=bins_pas, color='purple', edgecolor='black', density=True, alpha=0.7)
plt.title(f"Distribución Pascal (Binomial Negativa) r={r_pas}, p={p_pas}")
plt.xticks(range(max(muestras_pas) + 1))
plt.show()

# --- 6. BINOMIAL (Discreta - Barras) ---
n_bin, p_bin = 10, 0.5
muestras_bin = [generar_binomial(n_bin, p_bin) for _ in range(n_muestras)]
plt.figure(figsize=(8, 5))
bins_bin = np.arange(0, n_bin + 2) - 0.5
plt.hist(muestras_bin, bins=bins_bin, color='gold', edgecolor='black', density=True, alpha=0.7)
plt.title(f"Distribución Binomial n={n_bin}, p={p_bin}")
plt.xticks(range(n_bin + 1))
plt.show()

# --- 7. HIPERGEOMÉTRICA (Discreta - Barras) ---
N_hip, K_hip, n_hip_muestras = 20, 7, 5 
muestras_hip = [generar_hipergeometrica(N_hip, K_hip, n_hip_muestras) for _ in range(n_muestras)]
plt.figure(figsize=(8, 5))
bins_hip = np.arange(0, n_hip_muestras + 2) - 0.5
plt.hist(muestras_hip, bins=bins_hip, color='teal', edgecolor='black', density=True, alpha=0.7)
plt.title(f"Distribución Hipergeométrica N={N_hip}, K={K_hip}, n={n_hip_muestras}")
plt.xticks(range(n_hip_muestras + 1))
plt.show()

# --- 8. POISSON (Discreta - Barras) ---
lambd_poi = 3
muestras_poi = [generar_poisson(lambd_poi) for _ in range(n_muestras)]
plt.figure(figsize=(8, 5))
bins_poi = np.arange(0, max(muestras_poi) + 2) - 0.5
plt.hist(muestras_poi, bins=bins_poi, color='plum', edgecolor='black', density=True, alpha=0.7)
plt.title(f"Distribución Poisson $\lambda$={lambd_poi}")
plt.xticks(range(max(muestras_poi) + 1))
plt.show()

# --- 9. EMPÍRICA DISCRETA (Discreta - Barras) ---
val_emp, prob_emp = [1, 2, 3, 4], [0.1, 0.4, 0.3, 0.2]
muestras_emp = [generar_empirica_discreta(val_emp, prob_emp) for _ in range(n_muestras)]
plt.figure(figsize=(8, 5))
bins_emp = np.arange(min(val_emp), max(val_emp) + 2) - 0.5
plt.hist(muestras_emp, bins=bins_emp, color='cyan', edgecolor='black', density=True, alpha=0.7)
plt.title("Distribución Empírica Discreta")
plt.xticks(val_emp)
plt.show()

print("¡Listo! Tenés las 9 distribuciones programadas con las curvas perfectas para las continuas.")
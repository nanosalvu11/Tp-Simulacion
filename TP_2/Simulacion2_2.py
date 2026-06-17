import math
import random
import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# GENERADOR BASE U(0,1)
# ==========================================
def u():
    return random.random()


def _validar_probabilidad(p, nombre="p"):
    if not (0 <= p <= 1):
        raise ValueError(f"{nombre} debe estar en [0, 1].")

# ==========================================
# 1. UNIFORME (Continua)
# ==========================================
def generar_uniforme(a, b):
    if a >= b:
        raise ValueError("Para Uniforme se requiere a < b.")
    return a + (b - a) * u()


def generar_uniforme_rechazo(a, b, a_prop=None, b_prop=None, devolver_intentos=False):
    """Uniforme(a,b) via rechazo usando propuesta Uniforme(a_prop,b_prop)."""
    if a >= b:
        raise ValueError("Para Uniforme se requiere a < b.")

    if a_prop is None:
        a_prop = a - (b - a)
    if b_prop is None:
        b_prop = b + (b - a)
    if a_prop >= b_prop:
        raise ValueError("Para propuesta Uniforme se requiere a_prop < b_prop.")
    if a < a_prop or b > b_prop:
        raise ValueError("Se requiere [a,b] contenido en [a_prop,b_prop].")

    intentos = 0
    while True:
        intentos += 1
        y = a_prop + (b_prop - a_prop) * u()
        if a <= y <= b:
            if devolver_intentos:
                return y, intentos
            return y

# ==========================================
# 2. EXPONENCIAL (Continua)
# ==========================================
def generar_exponencial(lambd):
    if lambd <= 0:
        raise ValueError("Para Exponencial se requiere lambda > 0.")
    # Inversa estable: X = -ln(1-U)/lambda, evitando log(0).
    return -(1.0 / lambd) * math.log(1.0 - u())


def generar_exponencial_rechazo(lambd, lambd_prop=None, devolver_intentos=False):
    """Exponencial(lambda) por rechazo usando propuesta Exponencial(lambda_prop)."""
    if lambd <= 0:
        raise ValueError("Para Exponencial se requiere lambda > 0.")

    if lambd_prop is None:
        lambd_prop = 0.5 * lambd
    if lambd_prop <= 0 or lambd_prop > lambd:
        raise ValueError("Se requiere 0 < lambda_prop <= lambda para acotar f/g.")

    m = lambd / lambd_prop
    intentos = 0
    while True:
        intentos += 1
        y = generar_exponencial(lambd_prop)
        # f(y)/(M g(y)) = exp(-(lambda - lambda_prop) y)
        prob_aceptar = math.exp(-(lambd - lambd_prop) * y)
        if u() <= prob_aceptar:
            if devolver_intentos:
                return y, intentos
            return y

# ==========================================
# 3. GAMMA (Continua)
# ==========================================
def generar_gamma(k, theta):
    """Generador Gamma(k, theta) para k entero positivo sumando exponenciales."""
    if not isinstance(k, int) or k <= 0:
        raise ValueError("Para Gamma se requiere k entero positivo.")
    if theta <= 0:
        raise ValueError("Para Gamma se requiere theta > 0.")
    suma_exponenciales = 0
    for _ in range(k):
        suma_exponenciales += generar_exponencial(1.0 / theta)
    return suma_exponenciales

# ==========================================
# 4. NORMAL (Continua)
# ==========================================
def generar_normal(mu, sigma):
    if sigma <= 0:
        raise ValueError("Para Normal se requiere sigma > 0.")
    u1, u2 = u(), u()
    u1 = max(u1, 1e-12)
    z0 = math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)
    return z0 * sigma + mu


def _generar_laplace_estandar():
    v = u()
    if v < 0.5:
        return math.log(2.0 * v)
    return -math.log(2.0 * (1.0 - v))


def generar_normal_rechazo(mu, sigma, devolver_intentos=False):
    """Normal(mu,sigma) por rechazo con propuesta Laplace(0,1) escalada."""
    if sigma <= 0:
        raise ValueError("Para Normal se requiere sigma > 0.")

    intentos = 0
    while True:
        intentos += 1
        y = _generar_laplace_estandar()
        # Para propuesta Laplace, criterio equivalente a f/(M g).
        prob_aceptar = math.exp(-0.5 * (abs(y) - 1.0) ** 2)
        if u() <= prob_aceptar:
            x = mu + sigma * y
            if devolver_intentos:
                return x, intentos
            return x

# ==========================================
# 5. PASCAL / BINOMIAL NEGATIVA (Discreta)
# ==========================================
def generar_pascal(r, p):
    """Cantidad de fracasos antes de obtener 'r' éxitos"""
    if not isinstance(r, int) or r <= 0:
        raise ValueError("Para Pascal se requiere r entero positivo.")
    if not (0 < p <= 1):
        raise ValueError("Para Pascal se requiere p en (0, 1].")
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
    if not isinstance(n, int) or n < 0:
        raise ValueError("Para Binomial se requiere n entero no negativo.")
    _validar_probabilidad(p)
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
    if not isinstance(N, int) or not isinstance(K, int) or not isinstance(n, int):
        raise ValueError("Para Hipergeométrica N, K y n deben ser enteros.")
    if N <= 0:
        raise ValueError("Para Hipergeométrica se requiere N > 0.")
    if not (0 <= K <= N):
        raise ValueError("Para Hipergeométrica se requiere 0 <= K <= N.")
    if not (0 <= n <= N):
        raise ValueError("Para Hipergeométrica se requiere 0 <= n <= N.")

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
    if lambd < 0:
        raise ValueError("Para Poisson se requiere lambda >= 0.")
    if lambd == 0:
        return 0
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
    if len(valores) == 0:
        raise ValueError("La distribución empírica debe tener al menos un valor.")
    if len(valores) != len(probabilidades):
        raise ValueError("valores y probabilidades deben tener la misma longitud.")
    if any(prob < 0 for prob in probabilidades):
        raise ValueError("Las probabilidades no pueden ser negativas.")

    suma_prob = sum(probabilidades)
    if suma_prob <= 0:
        raise ValueError("La suma de probabilidades debe ser mayor a 0.")
    probabilidades = [prob / suma_prob for prob in probabilidades]

    numero_aleatorio = u()
    acumulada = 0.0
    for val, prob in zip(valores, probabilidades):
        acumulada += prob
        if numero_aleatorio <= acumulada:
            return val
    return valores[-1]


def _resumen_momentos(nombre, muestras, media_teorica, var_teorica):
    media_emp = float(np.mean(muestras))
    var_emp = float(np.var(muestras))
    print(
        f"{nombre}: media emp={media_emp:.4f} | media teo={media_teorica:.4f} | "
        f"var emp={var_emp:.4f} | var teo={var_teorica:.4f}"
    )


def _plot_discreta_con_pmf(muestras, soporte, pmf, color, titulo, xticks=None):
    soporte = list(soporte)
    if not soporte:
        raise ValueError("El soporte discreto no puede ser vacío.")

    plt.figure(figsize=(8, 5))
    bins = np.arange(min(soporte), max(soporte) + 2) - 0.5
    plt.hist(
        muestras,
        bins=bins,
        color=color,
        edgecolor="black",
        density=True,
        alpha=0.65,
        label="Empírica",
    )

    y_pmf = [pmf(x) for x in soporte]
    plt.plot(soporte, y_pmf, "ro", label="Teórica (PMF)")
    plt.vlines(soporte, [0], y_pmf, colors="red", linewidth=1.5, alpha=0.9)

    plt.title(titulo)
    if xticks is None:
        plt.xticks(soporte)
    else:
        plt.xticks(xticks)
    plt.legend()
    plt.show()

# ==========================================
# ZONA DE TESTEO Y GRÁFICOS (AL PIE DE LA LETRA)
# ==========================================
if __name__ == "__main__":
    print("Generando gráficos. Cerrá cada ventana para ver la siguiente.")
    n_muestras = 10000

    # ==========================================
    # TESTEO DE METODO DE RECHAZO (tabla TP)
    # ==========================================
    print("\n--- Testeo de Metodo de Rechazo (Uniforme, Exponencial, Normal) ---")

    a_r, b_r = 10, 20
    muestras_uni_r = []
    intentos_uni = 0
    for _ in range(n_muestras):
        x_r, it_r = generar_uniforme_rechazo(a_r, b_r, devolver_intentos=True)
        muestras_uni_r.append(x_r)
        intentos_uni += it_r
    tasa_uni = n_muestras / intentos_uni
    _resumen_momentos("Uniforme (Rechazo)", muestras_uni_r, (a_r + b_r) / 2, ((b_r - a_r) ** 2) / 12)
    print(f"Uniforme (Rechazo): tasa de aceptacion={tasa_uni:.4f}")

    lambd_exp_r = 0.5
    muestras_exp_r = []
    intentos_exp = 0
    for _ in range(n_muestras):
        x_r, it_r = generar_exponencial_rechazo(lambd_exp_r, devolver_intentos=True)
        muestras_exp_r.append(x_r)
        intentos_exp += it_r
    tasa_exp = n_muestras / intentos_exp
    _resumen_momentos("Exponencial (Rechazo)", muestras_exp_r, 1 / lambd_exp_r, 1 / (lambd_exp_r ** 2))
    print(f"Exponencial (Rechazo): tasa de aceptacion={tasa_exp:.4f}")

    mu_nor_r, sigma_nor_r = 0, 1
    muestras_nor_r = []
    intentos_nor = 0
    for _ in range(n_muestras):
        x_r, it_r = generar_normal_rechazo(mu_nor_r, sigma_nor_r, devolver_intentos=True)
        muestras_nor_r.append(x_r)
        intentos_nor += it_r
    tasa_nor = n_muestras / intentos_nor
    _resumen_momentos("Normal (Rechazo)", muestras_nor_r, mu_nor_r, sigma_nor_r ** 2)
    print(f"Normal (Rechazo): tasa de aceptacion={tasa_nor:.4f}\n")

    # --- 1. UNIFORME (Continua con Curva) ---
    a, b = 10, 20
    muestras_uni = [generar_uniforme(a, b) for _ in range(n_muestras)]
    plt.figure(figsize=(8, 5))
    plt.hist(muestras_uni, bins=30, color="skyblue", edgecolor="black", density=True, alpha=0.7, label="Empírica")
    x_uni = np.linspace(a - 1, b + 1, 300)
    y_uni = [1 / (b - a) if a <= x <= b else 0 for x in x_uni]
    plt.plot(x_uni, y_uni, "r-", lw=2, label="Teórica (PDF)")
    plt.title(f"Distribución Uniforme a={a}, b={b}")
    plt.legend()
    plt.show()
    _resumen_momentos("Uniforme", muestras_uni, (a + b) / 2, ((b - a) ** 2) / 12)

    # --- 2. EXPONENCIAL (Continua con Curva) ---
    lambd_exp = 0.5
    muestras_exp = [generar_exponencial(lambd_exp) for _ in range(n_muestras)]
    plt.figure(figsize=(8, 5))
    plt.hist(muestras_exp, bins=50, color="lightgreen", edgecolor="black", density=True, alpha=0.7, label="Empírica")
    x_exp = np.linspace(0, max(muestras_exp), 300)
    y_exp = lambd_exp * np.exp(-lambd_exp * x_exp)
    plt.plot(x_exp, y_exp, "r-", lw=2, label="Teórica (PDF)")
    plt.title(f"Distribución Exponencial $\\lambda$={lambd_exp}")
    plt.legend()
    plt.show()
    _resumen_momentos("Exponencial", muestras_exp, 1 / lambd_exp, 1 / (lambd_exp ** 2))

    # --- 3. GAMMA (Continua con Curva) ---
    k_gamma, theta_gamma = 3, 2.0
    muestras_gamma = [generar_gamma(k_gamma, theta_gamma) for _ in range(n_muestras)]
    plt.figure(figsize=(8, 5))
    plt.hist(muestras_gamma, bins=50, color="orange", edgecolor="black", density=True, alpha=0.7, label="Empírica")
    x_gam = np.linspace(0, max(muestras_gamma), 300)
    y_gam = (
        (x_gam ** (k_gamma - 1))
        * np.exp(-x_gam / theta_gamma)
        / (math.factorial(k_gamma - 1) * (theta_gamma ** k_gamma))
    )
    plt.plot(x_gam, y_gam, "r-", lw=2, label="Teórica (PDF)")
    plt.title(f"Distribución Gamma k={k_gamma}, $\\theta$={theta_gamma}")
    plt.legend()
    plt.show()
    _resumen_momentos("Gamma", muestras_gamma, k_gamma * theta_gamma, k_gamma * (theta_gamma ** 2))

    # --- 4. NORMAL (Continua con Curva) ---
    mu_nor, sigma_nor = 0, 1
    muestras_nor = [generar_normal(mu_nor, sigma_nor) for _ in range(n_muestras)]
    plt.figure(figsize=(8, 5))
    plt.hist(muestras_nor, bins=50, color="salmon", edgecolor="black", density=True, alpha=0.7, label="Empírica")
    x_nor = np.linspace(min(muestras_nor), max(muestras_nor), 300)
    y_nor = (1 / (sigma_nor * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x_nor - mu_nor) / sigma_nor) ** 2)
    plt.plot(x_nor, y_nor, "r-", lw=2, label="Teórica (PDF)")
    plt.title(f"Distribución Normal $\\mu$={mu_nor}, $\\sigma$={sigma_nor}")
    plt.legend()
    plt.show()
    _resumen_momentos("Normal", muestras_nor, mu_nor, sigma_nor ** 2)

    # --- 5. PASCAL (Discreta con PMF) ---
    r_pas, p_pas = 5, 0.5
    muestras_pas = [generar_pascal(r_pas, p_pas) for _ in range(n_muestras)]
    max_pas = max(muestras_pas)
    soporte_pas = range(0, max_pas + 1)

    def pmf_pascal(x):
        return math.comb(x + r_pas - 1, x) * ((1 - p_pas) ** x) * (p_pas ** r_pas)

    _plot_discreta_con_pmf(
        muestras_pas,
        soporte_pas,
        pmf_pascal,
        color="purple",
        titulo=f"Distribución Pascal (Binomial Negativa) r={r_pas}, p={p_pas}",
    )
    _resumen_momentos("Pascal", muestras_pas, r_pas * (1 - p_pas) / p_pas, r_pas * (1 - p_pas) / (p_pas ** 2))

    # --- 6. BINOMIAL (Discreta con PMF) ---
    n_bin, p_bin = 10, 0.5
    muestras_bin = [generar_binomial(n_bin, p_bin) for _ in range(n_muestras)]
    soporte_bin = range(0, n_bin + 1)

    def pmf_binomial(x):
        return math.comb(n_bin, x) * (p_bin ** x) * ((1 - p_bin) ** (n_bin - x))

    _plot_discreta_con_pmf(
        muestras_bin,
        soporte_bin,
        pmf_binomial,
        color="gold",
        titulo=f"Distribución Binomial n={n_bin}, p={p_bin}",
        xticks=range(n_bin + 1),
    )
    _resumen_momentos("Binomial", muestras_bin, n_bin * p_bin, n_bin * p_bin * (1 - p_bin))

    # --- 7. HIPERGEOMÉTRICA (Discreta con PMF) ---
    N_hip, K_hip, n_hip = 20, 7, 5
    muestras_hip = [generar_hipergeometrica(N_hip, K_hip, n_hip) for _ in range(n_muestras)]
    x_min_hip = max(0, n_hip - (N_hip - K_hip))
    x_max_hip = min(n_hip, K_hip)
    soporte_hip = range(x_min_hip, x_max_hip + 1)

    def pmf_hipergeometrica(x):
        return (math.comb(K_hip, x) * math.comb(N_hip - K_hip, n_hip - x)) / math.comb(N_hip, n_hip)

    _plot_discreta_con_pmf(
        muestras_hip,
        soporte_hip,
        pmf_hipergeometrica,
        color="teal",
        titulo=f"Distribución Hipergeométrica N={N_hip}, K={K_hip}, n={n_hip}",
    )
    media_hip = n_hip * (K_hip / N_hip)
    var_hip = n_hip * (K_hip / N_hip) * (1 - K_hip / N_hip) * ((N_hip - n_hip) / (N_hip - 1))
    _resumen_momentos("Hipergeométrica", muestras_hip, media_hip, var_hip)

    # --- 8. POISSON (Discreta con PMF) ---
    lambd_poi = 3
    muestras_poi = [generar_poisson(lambd_poi) for _ in range(n_muestras)]
    max_poi = max(muestras_poi)
    soporte_poi = range(0, max_poi + 1)

    def pmf_poisson(x):
        return math.exp(-lambd_poi) * (lambd_poi ** x) / math.factorial(x)

    _plot_discreta_con_pmf(
        muestras_poi,
        soporte_poi,
        pmf_poisson,
        color="plum",
        titulo=f"Distribución Poisson $\\lambda$={lambd_poi}",
    )
    _resumen_momentos("Poisson", muestras_poi, lambd_poi, lambd_poi)

    # --- 9. EMPÍRICA DISCRETA (Discreta con PMF conocida) ---
    val_emp, prob_emp = [1, 2, 3, 4], [0.1, 0.4, 0.3, 0.2]
    muestras_emp = [generar_empirica_discreta(val_emp, prob_emp) for _ in range(n_muestras)]
    prob_emp_norm = [p / sum(prob_emp) for p in prob_emp]
    mapa_prob = {v: p for v, p in zip(val_emp, prob_emp_norm)}

    def pmf_empirica(x):
        return mapa_prob.get(x, 0.0)

    _plot_discreta_con_pmf(
        muestras_emp,
        val_emp,
        pmf_empirica,
        color="cyan",
        titulo="Distribución Empírica Discreta",
        xticks=val_emp,
    )
    media_emp_teo = sum(v * p for v, p in zip(val_emp, prob_emp_norm))
    var_emp_teo = sum(((v - media_emp_teo) ** 2) * p for v, p in zip(val_emp, prob_emp_norm))
    _resumen_momentos("Empírica discreta", muestras_emp, media_emp_teo, var_emp_teo)

    print("Listo: 9 generadores con validación de parámetros y testeo empírico vs teórico.")
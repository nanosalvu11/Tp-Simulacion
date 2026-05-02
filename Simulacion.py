import matplotlib.pyplot as plt
import argparse, os, random
from pathlib import Path
import numpy as np
from scipy import stats

# Crear directorio para gráficas
os.makedirs("graficas", exist_ok=True)

muestras_corridas = []
fr_corridas = []
series_fr_acumuladas = []
num_elegido = 2
series_medias_acumuladas = []

series_varianzas_acumuladas = []
series_desvios_acumulados = []
numero_elegido_global = 2
cantidad_corridas_global = 0
cantidad_tiradas_global = 0

def corrida(tiradas,num_elegido):
    muestra_actual = []
    fr_acumuladas = []
    medias_acumuladas = []
    
    varianzas_acumuladas = []
    desvios_acumulados = []
    
    exitos = 0
    suma_acumulada = 0
    suma_cuadrados = 0
    
    for i in range(tiradas):
        num = random.randint(0,36)
        muestra_actual.append(num)
        
        # Frecuencia relativa
        if num == num_elegido:
            exitos += 1
        fr_actual = exitos/(i+1)
        fr_acumuladas.append(fr_actual)
        
        # Media
        suma_acumulada += num
        media_actual = suma_acumulada / (i+1)
        medias_acumuladas.append(media_actual)
        
        # Varianza y desvío
        suma_cuadrados += num**2
        varianza_actual = (suma_cuadrados / (i+1)) - (media_actual ** 2)
        varianza_actual = max(varianza_actual, 0)
        desvio_actual = varianza_actual ** 0.5
        
        varianzas_acumuladas.append(varianza_actual)
        desvios_acumulados.append(desvio_actual)
    
    muestras_corridas.append(muestra_actual)
    fr_corridas.append(fr_actual)
    series_medias_acumuladas.append(medias_acumuladas)
    series_varianzas_acumuladas.append(varianzas_acumuladas)
    series_desvios_acumulados.append(desvios_acumulados)
    
    return fr_acumuladas

def mostrar_corridas(num_elegido,cant_corridas,cant_tiradas,fr_acum):
    ganadas_total = 0
    os.system("cls" if os.name == "nt" else "clear")
    print(f'--- RESULTADOS DE SIMULACIÓN DE RULETA ---\n')
    print(f'Parámetros: {cant_corridas} corridas, {cant_tiradas} tiradas, número elegido: {num_elegido}\n')
    print("=" * 50)
    
    # Mostrar resultados individuales
    for i in range(len(muestras_corridas)):
        print(f'\nCorrida {i+1}:')
        ganadas_actual = muestras_corridas[i].count(num_elegido)  
        if ganadas_actual > 0:
            ganadas_total += 1
        
        print(f'  Aciertos: {ganadas_actual} veces')
        print(f'  Frecuencia relativa final: {round(fr_corridas[i]*100,2)}%')
        print(f'  Media final: {round(series_medias_acumuladas[i][-1],2)}')
        print(f'  Varianza final: {round(series_varianzas_acumuladas[i][-1],2)}')
        print(f'  Desvío final: {round(series_desvios_acumulados[i][-1],2)}')
        
        print(f'  Generando gráficas...', end='\r')
        ver_grafica_fr(series_fr_acumuladas[i], num_elegido, cant_tiradas, i+1)
        ver_grafica_media(series_medias_acumuladas[i], cant_tiradas, i+1)
        ver_grafica_varianza(series_varianzas_acumuladas[i], cant_tiradas, i+1)
        ver_grafica_desvio(series_desvios_acumulados[i], cant_tiradas, i+1)

    # Mostrar gráficas comparativas
    print("\n" + "=" * 50)
    print("Generando gráficas comparativas de todas las corridas...\n")
    
    ver_grafica_fr_comparativa(num_elegido, cant_tiradas, cant_corridas)
    ver_grafica_media_comparativa(cant_tiradas, cant_corridas)
    ver_grafica_varianza_comparativa(cant_tiradas, cant_corridas)
    ver_grafica_desvio_comparativa(cant_tiradas, cant_corridas)

    print(f'\n✓ Gráficas generadas exitosamente en la carpeta "graficas/"\n')
    print(f'RESUMEN FINAL:')
    print(f'  Corridas ganadas: {ganadas_total} de {cant_corridas} ({round((ganadas_total/cant_corridas)*100,2)}%)')
    print(f'  Frecuencia relativa promedio: {round((sum(fr_corridas)/len(fr_corridas))*100,4)}%')
    print(f'  Probabilidad teórica: {round((1/37)*100,4)}%\n')
    
    # Análisis TCL si hay >= 30 corridas
    if cant_corridas >= 30:
        analisis_tcl(cant_corridas, cant_tiradas)
    
    input("Presione Enter para salir...")

def ver_grafica_fr(fr_acum_individual,num_elegido,tiradas, n_corrida):
    fre = 1/37
    plt.figure(figsize=(10, 5))
    eje_x = list(range(1, tiradas + 1))
    plt.plot(eje_x, fr_acum_individual, color='blue', label=f'Corrida {n_corrida}')
    plt.axhline(y=fre, color='red', linestyle='--', linewidth=2, label=f'Prob. Teórica: {round(fre,4)}')
    plt.title(f'Frecuencia Relativa: Corrida {n_corrida} (Número {num_elegido})')
    plt.xlabel('n (Número de tiradas)')
    plt.ylabel('fr')
    plt.ylim(0, fre * 4) 
    plt.legend()
    plt.grid(alpha=0.3)
    plt.savefig(f'graficas/01_FR_Corrida{n_corrida}.png', dpi=100, bbox_inches='tight')
    plt.close()

def ver_grafica_media(media_acum_individual, tiradas, n_corrida):
    media_teorica = 18
    plt.figure(figsize=(10, 5))
    eje_x = list(range(1, tiradas + 1))
    
    plt.plot(eje_x, media_acum_individual, color='green', label='Media Observada')
    plt.axhline(y=media_teorica, color='orange', linestyle='--', label='Media Teórica')
    
    plt.title(f'Media: Corrida {n_corrida}')
    plt.xlabel('n')
    plt.ylabel('Media')
    plt.ylim(0, 36)
    plt.legend()
    plt.grid(alpha=0.3)
    plt.savefig(f'graficas/02_Media_Corrida{n_corrida}.png', dpi=100, bbox_inches='tight')
    plt.close()

def ver_grafica_varianza(varianza, tiradas, n_corrida):
    var_teorica = 114
    
    plt.figure(figsize=(10, 5))
    eje_x = list(range(1, tiradas + 1))
    
    plt.plot(eje_x, varianza, color='purple', label='Varianza Observada')
    plt.axhline(y=var_teorica, color='red', linestyle='--', label='Varianza Teórica')
    
    plt.title(f'Varianza: Corrida {n_corrida}')
    plt.xlabel('n')
    plt.ylabel('Varianza')
    plt.legend()
    plt.grid(alpha=0.3)
    plt.savefig(f'graficas/03_Varianza_Corrida{n_corrida}.png', dpi=100, bbox_inches='tight')
    plt.close()

def ver_grafica_desvio(desvio, tiradas, n_corrida):
    desvio_teorico = 114**0.5
    
    plt.figure(figsize=(10, 5))
    eje_x = list(range(1, tiradas + 1))
    
    plt.plot(eje_x, desvio, color='brown', label='Desvío Observado')
    plt.axhline(y=desvio_teorico, color='red', linestyle='--', label='Desvío Teórico')
    
    plt.title(f'Desvío Estándar: Corrida {n_corrida}')
    plt.xlabel('n')
    plt.ylabel('Desvío')
    plt.legend()
    plt.grid(alpha=0.3)
    plt.savefig(f'graficas/04_Desvio_Corrida{n_corrida}.png', dpi=100, bbox_inches='tight')
    plt.close()

def ver_grafica_fr_comparativa(num_elegido, tiradas, cant_corridas):
    fre_teorica = 1/37
    plt.figure(figsize=(12, 6))
    eje_x = list(range(1, tiradas + 1))
    
    for i in range(cant_corridas):
        plt.plot(eje_x, series_fr_acumuladas[i], label=f'Corrida {i+1}', alpha=0.7)
    
    plt.axhline(y=fre_teorica, color='red', linestyle='--', linewidth=2.5, label=f'Prob. Teórica: {round(fre_teorica,4)}')
    plt.title(f'Comparativa: Frecuencia Relativa - Todas las Corridas (Número {num_elegido})')
    plt.xlabel('n (Número de tiradas)')
    plt.ylabel('Frecuencia Relativa')
    plt.ylim(0, fre_teorica * 4)
    plt.legend()
    plt.grid(alpha=0.3)
    plt.savefig('graficas/05_FR_Comparativa.png', dpi=100, bbox_inches='tight')
    plt.close()

def ver_grafica_media_comparativa(tiradas, cant_corridas):
    media_teorica = 18
    plt.figure(figsize=(12, 6))
    eje_x = list(range(1, tiradas + 1))
    
    for i in range(cant_corridas):
        plt.plot(eje_x, series_medias_acumuladas[i], label=f'Corrida {i+1}', alpha=0.7)
    
    plt.axhline(y=media_teorica, color='orange', linestyle='--', linewidth=2.5, label='Media Teórica: 18')
    plt.title('Comparativa: Media - Todas las Corridas')
    plt.xlabel('n')
    plt.ylabel('Media')
    plt.ylim(0, 36)
    plt.legend()
    plt.grid(alpha=0.3)
    plt.savefig('graficas/06_Media_Comparativa.png', dpi=100, bbox_inches='tight')
    plt.close()

def ver_grafica_varianza_comparativa(tiradas, cant_corridas):
    var_teorica = 114
    plt.figure(figsize=(12, 6))
    eje_x = list(range(1, tiradas + 1))
    
    for i in range(cant_corridas):
        plt.plot(eje_x, series_varianzas_acumuladas[i], label=f'Corrida {i+1}', alpha=0.7)
    
    plt.axhline(y=var_teorica, color='red', linestyle='--', linewidth=2.5, label='Varianza Teórica: 114')
    plt.title('Comparativa: Varianza - Todas las Corridas')
    plt.xlabel('n')
    plt.ylabel('Varianza')
    plt.legend()
    plt.grid(alpha=0.3)
    plt.savefig('graficas/07_Varianza_Comparativa.png', dpi=100, bbox_inches='tight')
    plt.close()

def ver_grafica_desvio_comparativa(tiradas, cant_corridas):
    desvio_teorico = 114**0.5
    plt.figure(figsize=(12, 6))
    eje_x = list(range(1, tiradas + 1))
    
    for i in range(cant_corridas):
        plt.plot(eje_x, series_desvios_acumulados[i], label=f'Corrida {i+1}', alpha=0.7)
    
    plt.axhline(y=desvio_teorico, color='red', linestyle='--', linewidth=2.5, label=f'Desvío Teórico: {round(desvio_teorico,2)}')
    plt.title('Comparativa: Desvío Estándar - Todas las Corridas')
    plt.xlabel('n')
    plt.ylabel('Desvío')
    plt.legend()
    plt.grid(alpha=0.3)
    plt.savefig('graficas/08_Desvio_Comparativa.png', dpi=100, bbox_inches='tight')
    plt.close()

def analisis_tcl(cant_corridas, cant_tiradas):
    """Análisis del Teorema Central del Límite con las medias de todas las corridas"""
    
    if cant_corridas < 30:
        print("\n⚠ Nota: TCL es más confiable con ≥30 corridas. Tienes: " + str(cant_corridas))
        return
    
    print("\n" + "="*60)
    print("ANÁLISIS DEL TEOREMA CENTRAL DEL LÍMITE (TCL)")
    print("="*60)
    
    # Extraer medias de cada corrida
    medias_corridas = [series_medias_acumuladas[i][-1] for i in range(cant_corridas)]
    medias_array = np.array(medias_corridas)
    
    # Calcular estadísticos
    media_de_medias = np.mean(medias_array)
    desvio_de_medias_observado = np.std(medias_array, ddof=1)
    
    # Valores teóricos
    media_teorica = 18
    desvio_teorico_poblacion = 114**0.5
    desvio_tcl_teorico = desvio_teorico_poblacion / np.sqrt(cant_tiradas)
    
    # Mostrar resultados
    print(f"\nCantidad de corridas: {cant_corridas}")
    print(f"Tiradas por corrida: {cant_tiradas}\n")
    
    print(f"MEDIA DE LAS MEDIAS:")
    print(f"  Observada: {media_de_medias:.6f}")
    print(f"  Teórica:  {media_teorica:.6f}")
    print(f"  Diferencia: {abs(media_de_medias - media_teorica):.6f}\n")
    
    print(f"DESVÍO DE LAS MEDIAS:")
    print(f"  Observado: {desvio_de_medias_observado:.6f}")
    print(f"  Teórico (TCL): σ/√n = {desvio_teorico_poblacion:.4f}/√{cant_tiradas} = {desvio_tcl_teorico:.6f}")
    print(f"  Diferencia: {abs(desvio_de_medias_observado - desvio_tcl_teorico):.6f}\n")
    
    # Test de normalidad (Shapiro-Wilk) como apoyo, no como criterio único de TCL
    statistic, p_value = stats.shapiro(medias_array)
    print(f"TEST DE SHAPIRO-WILK (Normalidad):")
    print(f"  Estadístico: {statistic:.6f}")
    print(f"  p-value: {p_value:.6f}")
    if p_value > 0.05:
        print(f"  ✓ La muestra no rechaza normalidad al 5%")
    else:
        print(f"  ⚠ La muestra rechaza normalidad al 5%, pero TCL sigue indicando aproximación normal")
    
    print("\n" + "="*60 + "\n")
    
    # Generar gráficas TCL
    generar_graficas_tcl(medias_array, media_de_medias, desvio_de_medias_observado, 
                        media_teorica, desvio_tcl_teorico)

def generar_graficas_tcl(medias, media_medias, desvio_medias, media_teo, desvio_teo):
    """Genera gráficas de distribución normal para TCL"""
    
    # Gráfica 1: Histograma con curva normal superpuesta
    plt.figure(figsize=(12, 6))
    
    # Histograma
    n, bins, patches = plt.hist(medias, bins=8, density=True, alpha=0.7, 
                                 color='skyblue', edgecolor='black', label='Medias observadas')
    
    # Curva normal teórica
    x = np.linspace(medias.min() - 2*desvio_teo, medias.max() + 2*desvio_teo, 100)
    plt.plot(x, stats.norm.pdf(x, media_teo, desvio_teo), 'r-', linewidth=2.5, 
             label=f'Normal teórica (μ={media_teo}, σ={desvio_teo:.4f})')
    
    # Línea media observada
    plt.axvline(media_medias, color='green', linestyle='--', linewidth=2, 
                label=f'Media observada: {media_medias:.4f}')
    plt.axvline(media_medias + desvio_medias, color='gray', linestyle=':', linewidth=1.5)
    plt.axvline(media_medias - desvio_medias, color='gray', linestyle=':', linewidth=1.5, label=f'Desvío observado: {desvio_medias:.4f}')
    
    plt.title('Distribución de Medias - Aproximación a la Normal (TCL)', fontsize=12, fontweight='bold')
    plt.xlabel('Media de tiradas')
    plt.ylabel('Densidad de probabilidad')
    plt.legend()
    plt.grid(alpha=0.3)
    plt.savefig('graficas/09_TCL_Histograma.png', dpi=100, bbox_inches='tight')
    plt.close()
    
    # Gráfica 2: Q-Q Plot (Quantile-Quantile)
    plt.figure(figsize=(10, 8))
    stats.probplot(medias, dist="norm", plot=plt)
    plt.title('Q-Q Plot - Verificación de Normalidad', fontsize=12, fontweight='bold')
    plt.grid(alpha=0.3)
    plt.savefig('graficas/10_TCL_QQPlot.png', dpi=100, bbox_inches='tight')
    plt.close()

def menu():
    parser = argparse.ArgumentParser(
        description='Simulación de una ruleta con análisis estadístico.',
        usage='python Simulacion.py -t TIRADAS -c CORRIDAS -n NUMERO_ELEGIDO'
    )
    parser.add_argument('-t', '--tiradas', required=True, type=int, help='Cantidad de tiradas por corrida')
    parser.add_argument('-c', '--corridas', required=True, type=int, help='Cantidad de corridas a realizar')
    parser.add_argument('-n', '--numero', required=True, type=int, help='Número elegido (0-36)')
    args = parser.parse_args()

    try: 
        cant_tiradas = args.tiradas
        cant_corridas = args.corridas
        num_elegido_entrada = args.numero
        
        # Validar parámetros
        if cant_tiradas <= 0:
            print("\nError: La cantidad de tiradas debe ser mayor a 0.\n")
            return
        if cant_corridas <= 0:
            print("\nError: La cantidad de corridas debe ser mayor a 0.\n")
            return
        if num_elegido_entrada < 0 or num_elegido_entrada > 36:
            print("\nError: El número elegido debe estar entre 0 y 36.\n")
            return
            
    except ValueError:
        print("\nError: Parámetros inválidos. Use números enteros.\n")
        return

    os.system("cls" if os.name == "nt" else "clear")
    print(f"Iniciando simulación...")
    print(f"Tiradas: {cant_tiradas}, Corridas: {cant_corridas}, Número: {num_elegido_entrada}\n")
    
    for i in range(cant_corridas):
        print(f"Ejecutando corrida {i+1}/{cant_corridas}...", end='\r')
        fr_acum = corrida(cant_tiradas, num_elegido_entrada)
        series_fr_acumuladas.append(fr_acum)

    mostrar_corridas(num_elegido_entrada, cant_corridas, cant_tiradas, fr_acum)

if __name__ == "__main__":
    menu()

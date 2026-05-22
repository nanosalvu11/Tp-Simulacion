import argparse
import random
import matplotlib.pyplot as plt

def jugar_ruleta():
    # Simulamos apostar al color (18 números ganadores sobre 37)
    return random.random() < (18/37)

def simular(capital_inicial, n_tiradas, estrategia, tipo_capital, apuesta_base):
    caja = capital_inicial if tipo_capital == 'f' else 0  # Para infinito, registra cambio neto
    flujo_caja = [capital_inicial]
    victorias = 0
    freq_relativa = []
    historial_apuestas = [] 
    
    # La apuesta_base ahora viene como parámetro
    apuesta = apuesta_base
    fibo = [1, 1]
    fibo_idx = 0
    labouchere = [1, 2, 3, 4, 5]  # Secuencia inicial para Labouchere
    bancarrotas = 0

    for i in range(1, n_tiradas + 1):
        # Chequeo de bancarrota para capital finito
        if tipo_capital == 'f' and caja < apuesta:
            bancarrotas += 1
            caja = capital_inicial # Reseteo para seguir testeando la probabilidad en n tiradas
            apuesta = apuesta_base
            fibo_idx = 0
            labouchere = [1, 2, 3, 4, 5]
            
        historial_apuestas.append(apuesta) # Guardamos el monto antes de jugar
        gana = jugar_ruleta()
        
        if gana:
            caja += apuesta
            victorias += 1
            if estrategia == 'm': 
                apuesta = apuesta_base
            elif estrategia == 'd': 
                apuesta = max(apuesta_base, apuesta - apuesta_base)
            elif estrategia == 'f': 
                fibo_idx = max(0, fibo_idx - 2)
                apuesta = apuesta_base * fibo[fibo_idx]
            elif estrategia == 'l':
                if len(labouchere) > 1:
                    labouchere.pop(0)
                    labouchere.pop()
                    if len(labouchere) == 0:
                        labouchere = [1, 2, 3, 4, 5]
                        apuesta = apuesta_base * 6
                    else:
                        apuesta = apuesta_base * (labouchere[0] + labouchere[-1])
                else:
                    labouchere = [1, 2, 3, 4, 5]
                    apuesta = apuesta_base * 6
        else:
            caja -= apuesta
            if estrategia == 'm': 
                apuesta *= 2
            elif estrategia == 'd': 
                apuesta += apuesta_base
            elif estrategia == 'f':
                fibo_idx += 1
                if fibo_idx >= len(fibo): 
                    fibo.append(fibo[-1] + fibo[-2])
                apuesta = apuesta_base * fibo[fibo_idx]
            elif estrategia == 'l':
                labouchere.append(apuesta // apuesta_base)
                if len(labouchere) > 0:
                    apuesta = apuesta_base * (labouchere[0] + labouchere[-1])
                else:
                    labouchere = [1, 2, 3, 4, 5]
                    apuesta = apuesta_base * 6

        # Registro de datos
        if tipo_capital == 'f':
            flujo_caja.append(caja)
        else:
            flujo_caja.append(capital_inicial + caja)
        freq_relativa.append(victorias / i)

    return flujo_caja, freq_relativa, bancarrotas, historial_apuestas

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', type=float, required=True, help='Capital inicial')
    parser.add_argument('-n', type=int, required=True, help='Cantidad de tiradas')
    parser.add_argument('-e', type=int, default=1, help='Parámetro extra (opcional)')
    # Eliminamos 'o' de las opciones de estrategia
    parser.add_argument('-s', choices=['m', 'd', 'f', 'l'], required=True, help='Estrategia')
    parser.add_argument('-a', choices=['i', 'f'], required=True, help='Tipo de capital')
    parser.add_argument('-b', type=float, default=10, help='Monto de la apuesta base/inicial')
    args = parser.parse_args()

    # Le pasamos el nuevo argumento (args.b) a la función
    flujo, freq, quiebres, apuestas = simular(args.c, args.n, args.s, args.a, args.b)

    if args.a == 'f':
        print(f"Bancarrotas sufridas: {quiebres}")

    # Gráfico 1: Frecuencia Relativa
    fig1 = plt.figure(figsize=(10, 6))
    ax1 = fig1.add_subplot(111)
    ax1.bar(range(1, args.n + 1), freq, color='red', width=0.5)
    ax1.axhline(y=18/37, color='black', linestyle='--', label='Prob. Teórica (18/37)')
    ax1.set_title('Frecuencia Relativa de Apuesta Favorable')
    ax1.set_xlabel('n (número de tiradas)')
    ax1.set_ylabel('frsa')
    ax1.legend()
    plt.tight_layout()
    plt.show()
    
    # Gráfico 2: Flujo de Caja
    fig2 = plt.figure(figsize=(10, 6))
    ax2 = fig2.add_subplot(111)
    ax2.plot(range(args.n + 1), flujo, color='red', label='fc (flujo de caja)')
    ax2.axhline(y=args.c, color='blue', linestyle='-', label='fci (flujo de caja inicial)')
    ax2.set_title('Flujo de Caja vs Tiradas')
    ax2.set_xlabel('n (número de tiradas)')
    ax2.set_ylabel('cc (cantidad de capital)')
    ax2.legend()
    plt.tight_layout()
    plt.show()

    # Gráfico 3: Evolución del Tamaño de la Apuesta
    fig3 = plt.figure(figsize=(10, 6))
    ax3 = fig3.add_subplot(111)
    ax3.plot(range(1, args.n + 1), apuestas, color='green', alpha=0.7, label='Monto apostado')
    ax3.set_title('Evolución del Tamaño de la Apuesta vs Tiradas')
    ax3.set_xlabel('n (número de tiradas)')
    ax3.set_ylabel('Unidades apostadas')
    ax3.legend()
    plt.tight_layout()
    plt.show()
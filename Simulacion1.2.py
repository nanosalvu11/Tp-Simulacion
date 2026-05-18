import argparse
import random
import matplotlib.pyplot as plt

def jugar_ruleta():
    # Simulamos apostar al color (18 números ganadores sobre 37)
    return random.random() < (18/37)

def simular(capital_inicial, n_tiradas, estrategia, tipo_capital):
    caja = capital_inicial if tipo_capital == 'f' else float('inf')
    flujo_caja = [capital_inicial]
    victorias = 0
    freq_relativa = []
    
    apuesta_base = 10
    apuesta = apuesta_base
    fibo = [1, 1]
    fibo_idx = 0
    bancarrotas = 0

    for i in range(1, n_tiradas + 1):
        # Chequeo de bancarrota para capital finito
        if tipo_capital == 'f' and caja < apuesta:
            bancarrotas += 1
            caja = capital_inicial # Reseteo para seguir testeando la probabilidad en n tiradas
            apuesta = apuesta_base
            fibo_idx = 0
            
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
            elif estrategia == 'o': 
                apuesta *= 2 # Paroli
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
            elif estrategia == 'o': 
                apuesta = apuesta_base

        # Registro de datos
        flujo_caja.append(caja if tipo_capital == 'f' else capital_inicial + (caja - float('inf')))
        freq_relativa.append(victorias / i)

    return flujo_caja, freq_relativa, bancarrotas

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', type=float, required=True, help='Capital inicial')
    parser.add_argument('-n', type=int, required=True, help='Cantidad de tiradas')
    parser.add_argument('-e', type=int, default=1, help='Parámetro extra (opcional)')
    parser.add_argument('-s', choices=['m', 'd', 'f', 'o'], required=True, help='Estrategia')
    parser.add_argument('-a', choices=['i', 'f'], required=True, help='Tipo de capital')
    args = parser.parse_args()

    flujo, freq, quiebres = simular(args.c, args.n, args.s, args.a)

    if args.a == 'f':
        print(f"Bancarrotas sufridas: {quiebres}")

    # Gráficos con Matplotlib
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Frecuencia Relativa
    ax1.bar(range(1, args.n + 1), freq, color='red', width=0.5)
    ax1.set_title('Frecuencia Relativa de Apuesta Favorable')
    ax1.set_xlabel('n (número de tiradas)')
    ax1.set_ylabel('frsa')
    
    # Flujo de Caja
    ax2.plot(range(args.n + 1), flujo, color='red', label='fc (flujo de caja)')
    ax2.axhline(y=args.c, color='blue', linestyle='-', label='fci (flujo de caja inicial)')
    ax2.set_title('Flujo de Caja vs Tiradas')
    ax2.set_xlabel('n (número de tiradas)')
    ax2.set_ylabel('cc (cantidad de capital)')
    ax2.legend()

    plt.tight_layout()
    plt.show()
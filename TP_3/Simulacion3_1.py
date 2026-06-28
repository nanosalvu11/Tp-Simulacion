import argparse
import heapq
import random
from collections import deque

MU = 10.0
RATIOS_MM1 = [25, 50, 75, 100, 125]
COLAS_TP = [0, 2, 5, 10, 50]
INVENTARIO = {
    "demanda": 5.0,
    "revision": 1.0,
    "punto_pedido": 20,
    "nivel_objetivo": 50,
    "entrega": 2.0,
    "costo_orden": 75.0,
    "costo_mantenimiento": 1.0,
    "costo_faltante": 10.0,
    "inventario_inicial": 50,
}


def mean(valores):
    valores = list(valores)
    return sum(valores) / len(valores) if valores else 0.0


def exp(rng, rate):
    return float("inf") if rate <= 0 else rng.expovariate(rate)


def acumular(t_actual, t_nuevo, cola, ocupado, area_sistema, area_cola, area_servidor, dist):
    dt = t_nuevo - t_actual
    if dt > 0:
        q = len(cola)
        area_sistema += (q + int(ocupado)) * dt
        area_cola += q * dt
        area_servidor += int(ocupado) * dt
        dist[q] = dist.get(q, 0.0) + dt
    return t_nuevo, area_sistema, area_cola, area_servidor


def simular_mm1(lam, mu, tiempo, cola_maxima, seed):
    rng = random.Random(seed)
    t = 0.0
    cola = deque()
    ocupado = False
    llegada_actual = None
    inicio_servicio = None
    llegada = exp(rng, lam)
    salida = float("inf")
    llegadas = servidos = denegados = 0
    area_sistema = area_cola = area_servidor = 0.0
    distribucion = {}
    tiempos_sistema = []
    tiempos_cola = []

    while True:
        siguiente = min(llegada, salida, tiempo)
        if siguiente >= tiempo:
            t, area_sistema, area_cola, area_servidor = acumular(t, tiempo, cola, ocupado, area_sistema, area_cola, area_servidor, distribucion)
            break
        if salida <= llegada:
            t, area_sistema, area_cola, area_servidor = acumular(t, salida, cola, ocupado, area_sistema, area_cola, area_servidor, distribucion)
            servidos += 1
            tiempos_sistema.append(t - llegada_actual)
            tiempos_cola.append(inicio_servicio - llegada_actual)
            if cola:
                llegada_actual = cola.popleft()
                inicio_servicio = t
                salida = t + exp(rng, mu)
            else:
                ocupado = False
                llegada_actual = inicio_servicio = None
                salida = float("inf")
        else:
            t, area_sistema, area_cola, area_servidor = acumular(t, llegada, cola, ocupado, area_sistema, area_cola, area_servidor, distribucion)
            llegadas += 1
            if not ocupado:
                ocupado = True
                llegada_actual = inicio_servicio = t
                salida = t + exp(rng, mu)
            elif cola_maxima is not None and len(cola) >= cola_maxima:
                denegados += 1
            else:
                cola.append(t)
            llegada = t + exp(rng, lam)

    base = tiempo if tiempo > 0 else 1.0
    return {
        "L": area_sistema / base,
        "Lq": area_cola / base,
        "W": mean(tiempos_sistema),
        "Wq": mean(tiempos_cola),
        "rho": area_servidor / base,
        "p_den": (denegados / llegadas) if cola_maxima is not None and llegadas else None,
        "pq": {n: dur / base for n, dur in distribucion.items()},
    }


def resumir_mm1(resultados):
    resultados = list(resultados)
    estados = sorted({n for r in resultados for n in r["pq"]})
    return {
        "L": mean(r["L"] for r in resultados),
        "Lq": mean(r["Lq"] for r in resultados),
        "W": mean(r["W"] for r in resultados),
        "Wq": mean(r["Wq"] for r in resultados),
        "rho": mean(r["rho"] for r in resultados),
        "p_den": mean(r["p_den"] for r in resultados if r["p_den"] is not None) if any(r["p_den"] is not None for r in resultados) else None,
        "pq": {n: mean(r["pq"].get(n, 0.0) for r in resultados) for n in estados},
    }


def simular_inventario(tiempo, seed):
    rng = random.Random(seed)
    t = 0.0
    inv = float(INVENTARIO["inventario_inicial"])
    on_order = 0.0
    costo_orden = costo_mantenimiento = costo_faltante = 0.0
    ordenes = 0
    recepciones = []
    demanda = exp(rng, INVENTARIO["demanda"])
    revision = INVENTARIO["revision"]

    while True:
        recepcion = recepciones[0][0] if recepciones else float("inf")
        siguiente = min(demanda, revision, recepcion, tiempo)
        dt = siguiente - t
        if dt > 0:
            costo_mantenimiento += max(inv, 0.0) * INVENTARIO["costo_mantenimiento"] * dt
            costo_faltante += max(-inv, 0.0) * INVENTARIO["costo_faltante"] * dt
            t = siguiente
        if t >= tiempo:
            break
        if recepcion <= demanda and recepcion <= revision:
            _, qty = heapq.heappop(recepciones)
            inv += qty
            on_order -= qty
        elif demanda <= revision:
            inv -= 1.0
            demanda = t + exp(rng, INVENTARIO["demanda"])
        else:
            posicion = inv + on_order
            if posicion <= INVENTARIO["punto_pedido"]:
                qty = max(INVENTARIO["nivel_objetivo"] - posicion, 0)
                if qty > 0:
                    costo_orden += INVENTARIO["costo_orden"]
                    ordenes += 1
                    on_order += qty
                    heapq.heappush(recepciones, (t + INVENTARIO["entrega"], qty))
            revision += INVENTARIO["revision"]

    return {"orden": costo_orden, "mantenimiento": costo_mantenimiento, "faltante": costo_faltante, "total": costo_orden + costo_mantenimiento + costo_faltante, "ordenes": ordenes}


def resumir_inventario(resultados):
    resultados = list(resultados)
    return {
        "orden": mean(r["orden"] for r in resultados),
        "mantenimiento": mean(r["mantenimiento"] for r in resultados),
        "faltante": mean(r["faltante"] for r in resultados),
        "total": mean(r["total"] for r in resultados),
        "ordenes": round(mean(r["ordenes"] for r in resultados)),
    }


def imprimir_distribucion(dist):
    return "sin datos" if not dist else ", ".join(f"Q={n}: {p:.4f}" for n, p in sorted(dist.items()))


def ejecutar_mm1(porcentajes, corridas, tiempo, colas):
    print(f"\n=== MM1 | mu fijo = {MU:.2f} ===")
    for porcentaje in porcentajes:
        lam = MU * (porcentaje / 100.0)
        print(f"\n--- Tasa de arribo = {porcentaje:.0f}% de mu -> lambda = {lam:.4f} ---")
        for cola_maxima in colas:
            resumen = resumir_mm1(simular_mm1(lam, MU, tiempo, cola_maxima, 10_000 + i) for i in range(corridas))
            cola_txt = "infinita" if cola_maxima is None else str(cola_maxima)
            p_den = "N/A" if resumen["p_den"] is None else f"{resumen['p_den']:.4f}"
            print(f"Cola {cola_txt:>8} | L={resumen['L']:.4f} | Lq={resumen['Lq']:.4f} | W={resumen['W']:.4f} | Wq={resumen['Wq']:.4f} | rho={resumen['rho']:.4f} | P(deneg)={p_den}")
            print(f"  P(Q=n): {imprimir_distribucion(resumen['pq'])}")


def ejecutar_inventario(corridas, tiempo):
    print("\n=== Inventario ===")
    resumen = resumir_inventario(simular_inventario(tiempo, 50_000 + i) for i in range(corridas))
    print(f"Corridas: {corridas}")
    print(f"Costo de orden: {resumen['orden']:.4f}")
    print(f"Costo de mantenimiento: {resumen['mantenimiento']:.4f}")
    print(f"Costo de faltante: {resumen['faltante']:.4f}")
    print(f"Costo total: {resumen['total']:.4f}")
    print(f"Ordenes promedio por corrida: {resumen['ordenes']}")


def main():
    parser = argparse.ArgumentParser(description="Estudio de simulacion MM1 e Inventario")
    parser.add_argument("-p", "--porcentaje", type=float, default=None)
    parser.add_argument("--corridas", type=int, default=10)
    parser.add_argument("--tiempo", type=float, default=2000.0)
    parser.add_argument("--cola", choices=["infinita", "finita", "ambas"], default="ambas")
    parser.add_argument("--tamano-cola", type=int, default=5)
    parser.add_argument("--modelo", choices=["ambos", "mm1", "inventario"], default="ambos")
    args = parser.parse_args()

    corridas = max(10, args.corridas)
    porcentajes = [args.porcentaje] if args.porcentaje is not None else RATIOS_MM1
    if args.cola == "infinita":
        colas = [None]
    elif args.cola == "finita":
        colas = [max(0, args.tamano_cola)]
    else:
        colas = [None] + COLAS_TP

    if args.modelo in ("ambos", "mm1"):
        ejecutar_mm1(porcentajes, corridas, args.tiempo, colas)
    if args.modelo in ("ambos", "inventario"):
        ejecutar_inventario(corridas, args.tiempo)


if __name__ == "__main__":
    main()

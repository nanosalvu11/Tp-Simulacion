# TP_3 - Simulación MM1 e Inventario

Este directorio contiene el script [Simulacion3_1.py](Simulacion3_1.py) para ejecutar el estudio de simulación de:

- Modelo M/M/1
- Modelo de Inventario

## Requisitos

- Python 3
- Paquetes usados por el script:
  - `numpy`

## Ejecución

Desde esta carpeta (`TP_3`) ejecutar:

```powershell
py .\Simulacion3_1.py --modelo ambos
```

## Opciones del script

- `--modelo ambos` ejecuta MM1 e Inventario.
- `--modelo mm1` ejecuta solo MM1.
- `--modelo inventario` ejecuta solo Inventario.
- `--corridas N` define la cantidad de corridas por experimento. El script usa como mínimo 10.
- `--tiempo T` define el tiempo de simulación por corrida.
- `-p 25` ejecuta solo el escenario MM1 con lambda igual al 25% de mu.
- `--cola infinita` usa cola infinita en MM1.
- `--cola finita --tamano-cola N` usa cola finita y calcula la probabilidad de denegación.
- `--cola ambas` prueba cola infinita y las colas finitas del TP: 0, 2, 5, 10 y 50.

## Ejemplos

### MM1 con todos los escenarios pedidos

```powershell
py .\Simulacion3_1.py --modelo mm1 --cola ambas
```

### MM1 con cola finita de tamaño 5

```powershell
py .\Simulacion3_1.py --modelo mm1 --cola finita --tamano-cola 5
```

### MM1 con cola infinita

```powershell
py .\Simulacion3_1.py --modelo mm1 --cola infinita
```

### MM1 solo para 25% de mu

```powershell
py .\Simulacion3_1.py --modelo mm1 -p 25
```

### Inventario

```powershell
py .\Simulacion3_1.py --modelo inventario
```

## Observaciones

- En el archivo, `mu` queda fijo en 10 por defecto.
- Los parámetros base del inventario están definidos dentro del script en el diccionario `INVENTARIO`.
- Si querés cambiar una política de inventario, modificá esos valores y volvé a ejecutar el script.

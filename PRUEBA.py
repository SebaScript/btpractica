import numpy as np

MAQUINA = "X"
JUGADOR = "O"
INF = float('inf')
TAM_TABLERO = 4

tablero = np.full((TAM_TABLERO, TAM_TABLERO), "_")


def buscar_celdas_vacias(tablero_actual):
    l_celdas_vacias = []
    for indice_1, fila in enumerate(tablero_actual):
        for indice_2, casilla in enumerate(fila):
            if casilla != MAQUINA and casilla != JUGADOR:
                l_celdas_vacias.append((indice_1, indice_2))
    return l_celdas_vacias


def hay_ganador(tablero_actual, jugador):
    for indice_1, fila in enumerate(tablero_actual):
        if indice_1 != 3:
            for indice_2, casilla in enumerate(fila):
                if indice_2 != 3 and casilla == jugador:
                    if tablero_actual[indice_1+1][indice_2] == jugador and tablero_actual[indice_1+1][indice_2+1] == jugador:
                        return True
    return False


def evaluar(tablero_actual):
    if hay_ganador(tablero, MAQUINA) and not hay_ganador(tablero, JUGADOR):
        return INF  # La máquina tiene un patrón "L" y el jugador no.
    elif not hay_ganador(tablero, MAQUINA) and hay_ganador(tablero, JUGADOR):
        return -INF  # El jugador tiene un patrón "L" y la máquina no.

    return 0


def minimax(tablero_actual, jugador, alpha, beta, profundidad):
    if profundidad == 0 or hay_ganador(tablero_actual, JUGADOR) or hay_ganador(tablero_actual, MAQUINA):
        return evaluar(tablero_actual)

    celdas_vacias = buscar_celdas_vacias(tablero_actual)
    print("DENTRO DE EVAL")
    if jugador == MAQUINA:
        max_eval = -INF
        for celda in celdas_vacias:
            tablero_actual[celda] = MAQUINA
            eval = minimax(tablero_actual, JUGADOR, alpha, beta, profundidad - 1)
            tablero_actual[celda] = "_"
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = INF
        for celda in celdas_vacias:
            tablero_actual[celda[0]][celda[1]] = JUGADOR
            eval = minimax(tablero_actual, MAQUINA, alpha, beta, profundidad - 1)
            tablero_actual[celda[0]][celda[1]] = "_"
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval


def mejor_jugada(tablero_actual):
    mejor_eval = -INF
    mejor_mov = None
    alpha = -INF
    beta = INF
    PROFUNDIDAD_MAXIMA = 2

    celdas_vacias = buscar_celdas_vacias(tablero_actual)

    if not celdas_vacias:
        return None  # No hay jugadas disponibles, el juego ha terminado.

    for celda in celdas_vacias:
        tablero_actual[celda[0]][celda[1]] = MAQUINA
        print("SE LLAMO A EVAL")
        eval = minimax(tablero_actual, JUGADOR, alpha, beta, PROFUNDIDAD_MAXIMA)
        tablero_actual[celda[0]][celda[1]] = "_"
        if eval > mejor_eval:
            mejor_eval = eval
            mejor_mov = celda

    return mejor_mov


print("TRIQUI")
for fila in tablero:
    print("  ".join(fila))
while True:
    print("\nTurno del jugador")

    while True:
        fila = int(input("\nFila: "))
        col = int(input("Columna: "))
        if fila > 3 or col > 3:
            print("Fuera de rango\n")
            continue
        elif tablero[fila][col] == MAQUINA or tablero[fila][col] == JUGADOR:
            print("NO PODES JUGAR EN ESA POSICION\n")
            continue
        else:
            break

    tablero[fila][col] = JUGADOR

    if hay_ganador(tablero, JUGADOR):
        print("GANASTE!!!!\n")
        for fila in tablero:
            print("  ".join(fila))
        break

    if len(buscar_celdas_vacias(tablero)) == 0:
        print("EMPATE\n")
        for fila in tablero:
            print("  ".join(fila))
        break

    print("\nTurno de la maquina\n")

    maquina_fila, maquina_columna = mejor_jugada(tablero)
    tablero[maquina_fila][maquina_columna] = MAQUINA

    # Verificar si la máquina ha ganado
    if hay_ganador(tablero, MAQUINA):
        print("MAQUINA >>>> HUMANO\n")
        for fila in tablero:
            print("  ".join(fila))
        break

    # Verificar si hay empate
    if len(buscar_celdas_vacias(tablero)) == 0:
        print("EMPATE\n")
        for fila in tablero:
            print("  ".join(fila))
        break

    for fila in tablero:
        print("  ".join(fila))

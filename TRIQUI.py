import random

MAQUINA = "X"
JUGADOR = "O"
INF = float('inf')

tablero = [["_", "_", "_", "_"],
           ["_", "_", "_", "_"],
           ["_", "_", "_", "_"],
           ["_", "_", "_", "_"]]


# Ejemplo de patron para ganar:

# tablero = [["_", "_", "_", "_"],
#           ["_", "X", "_", "_"],
#           ["_", "X", "X", "_"],
#           ["_", "_", "_", "_"]]


def hay_ganador(tablero_actual, jugador):
    for indice_1, fila in enumerate(tablero_actual):
        if indice_1 != 3:
            for indice_2, casilla in enumerate(fila):
                if indice_2 != 3 and casilla == jugador:
                    if tablero_actual[indice_1+1][indice_2] == jugador and tablero_actual[indice_1+1][indice_2+1] == jugador:
                        return True
    return False


def minimax(tablero_actual, jugador, alpha, beta):
    celdas_vacias = buscar_celdas_vacias(tablero_actual)

    if hay_ganador(tablero_actual, JUGADOR):
        return -1
    elif hay_ganador(tablero_actual, MAQUINA):
        return 1
    elif len(celdas_vacias) == 0:
        return 0

    if jugador == MAQUINA:
        max_eval = -INF
        for celda in celdas_vacias:
            tablero_actual[celda[0]][celda[1]] = MAQUINA
            eval = minimax(tablero_actual, JUGADOR, alpha, beta)
            tablero_actual[celda[0]][celda[1]] = "_"
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = INF
        for celda in celdas_vacias:
            tablero_actual[celda[0]][celda[1]] = JUGADOR
            eval = minimax(tablero_actual, MAQUINA, alpha, beta)
            tablero_actual[celda[0]][celda[1]] = "_"
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval


def realizar_mejor_jugada(tablero_actual):
    best_eval = -INF
    best_move = None
    alpha = -INF
    beta = INF

    celdas_vacias = buscar_celdas_vacias(tablero_actual)

    for celda in celdas_vacias:
        tablero_actual[celda[0]][celda[1]] = MAQUINA
        eval = minimax(tablero_actual, JUGADOR, alpha, beta)
        tablero_actual[celda[0]][celda[1]] = "_"
        if eval > best_eval:
            best_eval = eval
            best_move = celda

    return best_move


print("TRIQUI\n")
while True:
    for fila in tablero:
        print("  ".join(fila))

    print("\nTurno del jugador")
    fila = int(input("\nFila: "))
    col = int(input("Columna: "))

    if fila > 3 or col > 3:
        print("Fuera de rango\n")
        continue

    if tablero[fila][col] == MAQUINA or tablero[fila][col] == JUGADOR:
        print("NO PODES JUGAR EN ESA POSICION\n")
        continue

    else:
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

    celdas_vacias = buscar_celdas_vacias(tablero)

    if len(celdas_vacias) == 15:
        maquina_fila = random.randint(0, 3)
        maquina_columna = random.randint(0, 3)
        tablero[maquina_fila][maquina_columna] = MAQUINA

    else:
        maquina_fila, maquina_columna = realizar_mejor_jugada(tablero)
        tablero[maquina_fila][maquina_columna] = MAQUINA

        # Verificar si la máquina ha ganado
        if hay_ganador(tablero, MAQUINA):
            print("MAQUINA >>>> HUMANO\n")
            for fila in tablero:
                print("  ".join(fila))
            break

        # Verificar si hay empate
        if len(buscar_celdas_vacias(tablero)) == 0:
            print("¡Es un empate!\n")
            for fila in tablero:
                print("  ".join(fila))
            break

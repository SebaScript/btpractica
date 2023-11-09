import random
import numpy as np


MAQUINA = "X"
HUMANO = "O"
CELDA_VACIA = "_"
INF = float('inf')
TAM_TABLERO = 4

tablero = np.full((TAM_TABLERO, TAM_TABLERO), CELDA_VACIA)


def buscar_celdas_vacias(tablero_actual):
    l_celdas_vacias = []
    for indice_1, fila in enumerate(tablero_actual):
        for indice_2, casilla in enumerate(fila):
            if casilla != MAQUINA and casilla != HUMANO:
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
    puntaje = 0
    if hay_ganador(tablero, MAQUINA) and not hay_ganador(tablero, HUMANO):
        puntaje += INF
    elif not hay_ganador(tablero, MAQUINA) and hay_ganador(tablero, HUMANO):
        puntaje -= INF

    return puntaje


def mejor_jugada(tablero_actual):
    max_eval = -INF
    alpha = -INF
    beta = INF

    celdas_vacias = buscar_celdas_vacias(tablero_actual)

    for celda in celdas_vacias:
        tablero_actual[celda[0]][celda[1]] = MAQUINA
        eval = minimax(tablero_actual, HUMANO, alpha, beta, 5)
        tablero_actual[celda[0]][celda[1]] = CELDA_VACIA
        if eval > max_eval:
            max_eval = eval
            mejor_mov = celda

    return mejor_mov


def minimax(tablero_actual, jugador, alpha, beta, profundidad):
    if profundidad == 0 or hay_ganador(tablero_actual, HUMANO) or hay_ganador(tablero_actual, MAQUINA):
        return evaluar(tablero_actual)

    celdas_vacias = buscar_celdas_vacias(tablero_actual)

    if jugador == MAQUINA:
        max_eval = -INF
        for celda in celdas_vacias:
            tablero_actual[celda[0]][celda[1]] = MAQUINA
            eval = minimax(tablero_actual, HUMANO, alpha, beta, profundidad - 1)
            tablero_actual[celda[0]][celda[1]] = CELDA_VACIA
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if alpha >= beta:
                break

        return max_eval

    else:
        min_eval = INF
        for celda in celdas_vacias:
            tablero_actual[celda[0]][celda[1]] = HUMANO
            eval = minimax(tablero_actual, MAQUINA, alpha, beta, profundidad - 1)
            tablero_actual[celda[0]][celda[1]] = CELDA_VACIA
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if alpha >= beta:
                break

        return min_eval


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
        elif tablero[fila][col] == MAQUINA or tablero[fila][col] == HUMANO:
            print("\nNO PODES JUGAR EN ESA POSICION\n")
            continue
        else:
            break

    tablero[fila][col] = HUMANO

    if hay_ganador(tablero, HUMANO):
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

    if len(buscar_celdas_vacias(tablero)) == 15:
        while True:
            maquina_fila = random.randint(0, 3)
            maquina_columna = random.randint(0, 3)
            if tablero[maquina_fila][maquina_columna] == HUMANO:
                continue
            break
        tablero[maquina_fila][maquina_columna] = MAQUINA

        for fila in tablero:
            print("  ".join(fila))

    else:
        maquina_fila, maquina_columna = mejor_jugada(tablero)
        tablero[maquina_fila][maquina_columna] = MAQUINA

        if hay_ganador(tablero, MAQUINA):
            print("MAQUINA >>>> HUMANO\n")
            for fila in tablero:
                print("  ".join(fila))
            break

        if len(buscar_celdas_vacias(tablero)) == 0:
            print("EMPATE\n")
            for fila in tablero:
                print("  ".join(fila))
            break

        for fila in tablero:
            print("  ".join(fila))

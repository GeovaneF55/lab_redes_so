# -*- coding: utf-8 -*- 

from functools import reduce
import json
import numpy as np
import socket
import struct

import util

def check_board(board):
    winner = check_rows(board)
    if winner == util.Player.NONE.value:
        winner = check_cols(board)

        if winner == util.Player.NONE.value:
            winner = check_diags(board)

    return winner

def check_rows(board):
    winner = util.Player.NONE

    for i in range(len(board)):
        player1 = board[i].count('X')

        if player1 == 3:
            winner = util.Player.ONE
        else:
            player2 = board[i].count('O')
            
            if player2 == 3:
                winner = util.Player.TWO

    return winner.value     

def check_cols(board):
    winner = util.Player.NONE
    cols = [[row[i] for row in board] for i in range(len(board[0]))]

    for i in range(len(cols)):

        player1 = cols[i].count('X')

        if player1 == 3:
            winner = util.Player.ONE
        else:

            player2 = cols[i].count('O')
            
            if player2 == 3:
                winner = util.Player.TWO

    return winner.value

def check_diags(board):
    winner = util.Player.NONE
    principal = np.diag(board)
    secondary = np.diag(np.fliplr(board))

    unique, counts = np.unique(principal, return_counts=True)
    principal = dict(zip(unique, counts))

    unique, counts = np.unique(secondary, return_counts=True)
    secondary = dict(zip(unique, counts))

    p1_princ = principal['X'] if 'X' in principal else 0
    p1_sec = secondary['X'] if 'X' in secondary else 0

    if p1_princ == 3 or p1_sec == 3:
        winner = util.Player.ONE
    else:
        p2_princ = principal['O'] if 'O' in principal else 0
        p2_sec = secondary['O'] if 'O' in secondary else 0
        
        if p2_princ == 3 or p2_sec == 3:
            winner = util.player.TWO

    return winner.value

def mark_board(board, player_id, x, y):
    if player_id == util.Player.ONE.value:
        board[x][y] = 'X'
    else: 
        board[x][y] = 'O'

    return board[x][y]

def prepare_game(conn1, conn2):
    """ Realiza todos os preparativos necessários para
    o início de um novo jogo (e.g criação da matriz).

    @param conn conexão.
    @param client endereço.
    """

    # Tabuleiro de jogo referente ao servidor.
    board = [[' ' for _ in range(3)] for _ in range(3)]

    # Jogador atual
    current = util.Player.ONE.value

    # Envia para ambos os jogadores um parâmetro indicando quem é o jogador.
    conn1.send(struct.pack('!I', util.Player.ONE.value))
    conn2.send(struct.pack('!I', util.Player.TWO.value))

    # Iniciar novo jogo.
    start_game(conn1, conn2, board, current)
    
def start_game(conn1, conn2, board, current):
    winner = util.Player.NONE.value

    while winner is util.Player.NONE.value:
        # Envia para ambos os jogadores um parâmetro indicando qual o jogador
        # atual.
        conn1.send(struct.pack('!I', current))
        conn2.send(struct.pack('!I', current))

        # Sequência de mensagens caso o Jogador atual seja o primeiro
        if current == util.Player.ONE.value:

            length, = struct.unpack('!I', conn1.recv(4))
            move = json.loads(conn1.recv(length).decode())

            mark_board(board, current, move['x'], move['y'])

            data = json.dumps({
                'x': move['x'], 
                'y': move['y']
            }).encode()

            conn2.send(struct.pack('!I', len(data)))
            conn2.send(data)

            # Altera o jogador atual
            current = util.Player.TWO.value

        # Sequência de mensagens caso o Jogador atual seja o segundo
        else:

            length, = struct.unpack('!I', conn2.recv(4))
            move = json.loads(conn2.recv(length).decode())

            mark_board(board, current, move['x'], move['y'])

            data = json.dumps({
                'x': move['x'], 
                'y': move['y']
            }).encode()

            conn1.send(struct.pack('!I', len(data)))
            conn1.send(data)

            # Altera o jogador atual
            current = util.Player.ONE.value

        # Envia mensagem aos jogadores se houver vencedor
        winner = check_board(board)

        conn1.send(struct.pack('!I', winner))
        conn2.send(struct.pack('!I', winner))


def create_room(i):
    """ Criação de uma nova sala, que irá aceitar 2 conexões por vez.

    @param i <int> identificador da sala (sala nº i). 
    """

    host = util.get_address()

    # Cria o socket do servnameor, declarando a família do protocolo através do
    # parâmetro AF_INET, bem como o protocolo TCP, através do parâmetro
    # SOCKET_STREAM.
    room = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    room.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    room.bind((host, 0))
    port = room.getsockname()[1]

    # Define um limite de 2 conexões simultâneas esperando na fila.
    # Uma sala permite apenas dois jogadores.
    room.listen(2)

    print('Sala {}: Aguardando conexões...'.format(i))
    print('Sala {}: Host: {}\t Porta: {}\n'.format(i, host, port))

    while True:
        # Jogador 1.
        conn1, client = room.accept()
        print('Sala {}: Jogador 1 ({}): conectado.'.format(i, client[0]))
        
        # Jogador 2.
        conn2, client = room.accept()
        print('Sala {}: Jogador 2 ({}): conectado.'.format(i, client[0]))
        print('Sala {}: Preparando novo jogo...'.format(i))

        # Preparar jogo.
        prepare_game(conn1, conn2)

        print('Sala {}: Jogo finalizado...'.format(i))

        # Jogo finalizado, fechando conexões para possibilitar novos jogadores.
        conn1.close()
        conn2.close()

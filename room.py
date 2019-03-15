# -*- coding: utf-8 -*- 

from functools import reduce
import json
import numpy as np
import socket
import struct

import util

def check_board(board):
    winner = check_rows(board)
    if winner == None:
        winner = check_cols(board)

        if winner == None:
            winner = check_diags(board)

    return winner

def check_rows(board):
    winner = None
    i = 0

    while not winner:
        player1 = reduce(lambda acc, el: acc + (el == 'x'), board[i], 0)

        if player1 == 3:
            winner = 'player1'
        else:
            player2 = reduce(lambda acc, el: acc + (el == 'o'), board[i], 0)
            
            if player2 == 3:
                winner = 'player2'

        i += 1

    return winner       

def check_cols(board):
    cols = np.transpose(board)
    winner = None
    i = 0

    while not winner:
        player1 = reduce(lambda acc, el: acc + (el == 'x'), cols[i], 0)

        if player1 == 3:
            winner = 'player1'
        else:
            player2 = reduce(lambda acc, el: acc + (el == 'o'), cols[i], 0)
            
            if player2 == 3:
                winner = 'player2'

        i += 1

    return winner

def check_diags(board):
    principal = np.diag(board)
    secondary = np.diag(np.fliplr(board))
    winner = None

    p1_princ = reduce(lambda acc, el: acc + (el == 'x'), principal, 0)
    p1_sec = reduce(lambda acc, el: acc + (el == 'x'), secondary, 0)

    if p1_princ == 3 or p1_sec == 3:
        winner = 'player1'
    else:
        p2_princ = reduce(lambda acc, el: acc + (el == '0'), principal, 0)
        p2_sec = reduce(lambda acc, el: acc + (el == 'o'), secondary, 0)
        
        if p2_princ == 3 or p2_sec == 3:
            winner = 'player2'

    return winner

def prepare_game(conn1, conn2):
    """ Realiza todos os preparativos necessários para
    o início de um novo jogo.

    @param conn conexão.
    @param client endereço.
    """

    # Parâmetros do jogo.
    board_size = 3

    # Tabuleiro de jogo referente ao servidor.
    board = [[' ' for _ in range(board_size)] for _ in range(board_size)]

    # Enviando dados iniciais para cliente.
    
    # data = json.dumps(board).encode()
    # length = len(data)

    # conn1.send(struct.pack('!I', length))
    # conn1.send(data)

    # conn2.send(struct.pack('!I', length))
    # conn2.send(data)

    start_game(conn1, conn2, board)

    
def start_game(conn1, conn2, board):
    pass
    # pos, = struct.unpack('!I', conn1.recv(4))
    
def create_room():
    host = util.get_address()

    # Cria o socket do servnameor, declarando a família do protocolo
    # através do parâmetro AF_INET, bem como o protocolo TCP,
    # através do parâmetro SOCKET_STREAM.
    room = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    room.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    room.bind((host, 0))
    port = room.getsockname()[1]

    # Define um limite de 2 conexões simultâneas esperando
    # na fila.
    room.listen(2)

    print('Servidor iniciado. Aguardando conexões...')
    print('Host: {}\t Porta: {}\n'.format(host, port))

    while True:
        # Jogador 1.
        conn1, client = room.accept()
        print('Jogador 1 ({}): conectado.'.format(client[0]))
        
        # Jogador 2.
        conn2, client = room.accept()
        print('Jogador 2 ({}): conectado. Preparando novo jogo...'.format(client[0]))
        
        # Iniciar jogo.
        prepare_game(conn1, conn2)

        # Possíveis implementações: quer continuar jogando? N PODE TROXA!
        conn1.close()
        conn2.close()
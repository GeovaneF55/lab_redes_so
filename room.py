# -*- coding: utf-8 -*- 

import json
import socket
import struct

import util

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
    # conn.send(struct.pack('!I', board_size))

    # length, = struct.unpack('!I', conn.recv(4))

    start_game(conn1, conn2, board)

    
def start_game(conn1, conn2, board):
    pass
    
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
        print('{} conectado. Preparando novo jogo...'.format(client[0]))
        
        # Jogador 2.
        conn2, client = room.accept()
        print('{} conectado. Preparando novo jogo...'.format(client[0]))
        
        # Iniciar jogo.
        prepare_game(conn1, conn2)

        # Possíveis implementações: quer continuar jogando? N PODE TROXA!
        conn1.close()
        conn2.close()
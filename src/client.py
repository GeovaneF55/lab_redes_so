# -*- coding: utf-8 -*- 

import json
import socket
import struct

import util

def prepare_game():
    """ Inicializa conexão com o servidor, para iniciar novo jogo. """
    
    print('{} Jogo da Velha {}\n'.format('=' * 30, '=' * 30))
    host = input('Insira o IP do servidor: ')
    port = int(input('Insira a porta para conexão: '))

    # Cria o socket do servnameor, declarando a família do protocolo
    # através do parâmetro AF_INET, bem como o protocolo TCP,
    # através do parâmetro SOCKET_STREAM.
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect((host, port))

    board = [[' ' for _ in range(3)] for _ in range(3)]

    # Identificando qual o nº do jogador.
    data, = struct.unpack('!I', conn.recv(4))
    player_id = util.Player(data)

    # Identificando qual o jogador que iniciará.
    data, = struct.unpack('!I', conn.recv(4))
    current = util.Player(data)

    print('\n\nJogo iniciado!')
    start_game(conn, board, player_id, current)


def start_game(conn, board, player_id, current):
    print('Eu sou o jogador: {}'.format(player_id))
    print('O jogador {} iniciará o jogo.'.format(current))


if __name__ == '__main__':
    prepare_game()

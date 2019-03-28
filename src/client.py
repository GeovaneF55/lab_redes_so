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

    print('\n\nJogo iniciado!')
    start_game(conn, board, player_id)

# Imprimir o tabuleiro do jogo da velha
def print_board(board):

    w = []
    p_row = []
    c = (' ___' *  3 )
    f = ('|___' *  3 + '|')

    for row in board:
        for cell in row:
            p_row.append(cell)
        w.append('| ' + ' | '.join(p_row) + ' |')
        p_row = []

    print('\n'.join((c, w[0], f, w[1], f, w[2], f, )))

# Verifica se as coordenadas escolhidas são válidas
def isValid(board, x, y):
    valid = True

    if x >= 0 and x < 3 and y >= 0 and y < 3:
        if board[x][y] != ' ':
            valid = False
    else:
        valid = False
    
    return valid

# Marca a opção do jogador no tabuleiro
def mark_board(board, player_id, x, y):
    if player_id.value == util.Player.ONE.value:
        board[x][y] = 'X'
    else: 
        board[x][y] = 'O'

    return board[x][y]

def start_game(conn, board, player_id):
    print('Eu sou o jogador: {}'.format(player_id))

    # Enquanto ninguém venceu
    winner = util.Player.NONE

    while winner.value is util.Player.NONE.value:

        # Identificando qual o jogador que iniciará.
        data, = struct.unpack('!I', conn.recv(4))
        current = util.Player(data)

        if current == player_id:
            valid_choice = False
            x = y = 0

            print('Sua rodada Jogador {}'.format(current))

            # Obriga o jogador a escolher uma casa válida
            while not valid_choice:
                print_board(board)
                x = int(input('Escolha a linha (1, 2 ou 3): ')) - 1
                y = int(input('Escolha a coluna (1, 2 ou 3): ')) - 1
                valid_choice = isValid(board, x, y)

                if not valid_choice:
                    print('Valores incorretos. Escolha novamente!')

            marker = mark_board(board, current, x, y)

            # Envia a opção marcada para o servidor
            data = json.dumps({
                'x': x, 
                'y': y,
                'marker': marker
            }).encode()

            conn.send(struct.pack('!I', len(data)))
            conn.send(data)
        else:
            print('Rodada do oponente o Jogador {}'.format(current))

            print_board(board)
            print('Aguarde...')

            length, = struct.unpack('!I', conn.recv(4))
            data = json.loads(conn.recv(length).decode())

            marker = mark_board(board, current, data['x'], data['y'])

            print_board(board)

        data, = struct.unpack('!I', conn.recv(4))
        winner = util.Player(data)

        if winner.value is not util.Player.NONE.value:
            if winner.value is player_id.value:
                print_board(board)
                print('Você venceu!')
            else:
                print('Você perdeu!')

if __name__ == '__main__':
    prepare_game()

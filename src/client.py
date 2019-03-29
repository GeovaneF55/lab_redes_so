# -*- coding: utf-8 -*- 

import json
import socket
import struct

import util

def prepare_game():
    """ Inicializa conexão com o servidor, para preparar e iniciar
    novo jogo. 
    """
    
    print('{} Jogo da Velha {}\n'.format('=' * 30, '=' * 30))
    host = input('Insira o IP do servidor: ')
    port = int(input('Insira a porta para conexão: '))

    # Cria o socket do servnameor, declarando a família do protocolo
    # através do parâmetro AF_INET, bem como o protocolo TCP,
    # através do parâmetro SOCKET_STREAM.
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect((host, port))

    print('\nConectado em {}:{}'.format(host, port))

    board = [[' ' for _ in range(3)] for _ in range(3)]

    # Identificando qual o nº do jogador.
    data, = struct.unpack('!I', conn.recv(4))
    player_id = data

    print('\n\nJogo iniciado!')
    start_game(conn, board, player_id)


def print_board(board):
    """ Imprimir o tabuleiro do jogo da velha.

    @param board Tabuleiro do jogo.
    """

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


def is_valid(board, x, y):
    """ Verifica se as coordenadas escolhidas são válidas.

    @param board Tabuleiro do jogador.
    @param x Coordenada <x> do tabuleiro.
    @param y Coordenada <y> do tabuleiro.
    """
    
    valid = True

    if x >= 0 and x < 3 and y >= 0 and y < 3:
        if board[x][y] != ' ':
            valid = False
    else:
        valid = False
    
    return valid


def start_game(conn, board, player_id):
    """ Inicia um novo jogo na máquina do cliente.

    @param conn Conexão com servidor.
    @param board Tabuleiro do jogo.
    @param player_id Identificador do jogador.
    """

    print('Eu sou o jogador: {}'.format(util.Player(player_id)))

    # Enquanto ninguém venceu
    winner_id = util.Player.NONE.value

    while winner_id is util.Player.NONE.value:

        # Identificando qual o jogador da rodada.
        data, = struct.unpack('!I', conn.recv(4))
        current_id = data

        if current_id == player_id:
            valid_choice = False
            x = y = 0

            print('\nSua rodada Jogador {}'.format(util.Player(current_id)))

            # Obriga o jogador a escolher uma casa válida
            while not valid_choice:
                print_board(board)
                x = int(input('Escolha a linha (1, 2 ou 3): ')) - 1
                y = int(input('Escolha a coluna (1, 2 ou 3): ')) - 1
                valid_choice = is_valid(board, x, y)

                if not valid_choice:
                    print('\nValores incorretos. Escolha novamente!')

            util.mark_board(board, current_id, x, y)

            # Envia a opção marcada para o servidor
            data = json.dumps({
                'x': x, 
                'y': y
            }).encode()

            conn.send(struct.pack('!I', len(data)))
            conn.send(data)
        else:

            print('\nRodada do oponente o Jogador {}'.format(util.Player(current_id)))
            print_board(board)
            print('Aguarde...\n')

            length, = struct.unpack('!I', conn.recv(4))
            data = json.loads(conn.recv(length).decode())

            util.mark_board(board, current_id, data['x'], data['y'])

            print_board(board)

        data, = struct.unpack('!I', conn.recv(4))
        winner_id = data

        # Verifica se houve ganhandores, caso houver mostra os resultados
        if winner_id is not util.Player.NONE.value:
            if winner_id is player_id:
                print_board(board)
                print('VOCÊ VENCEU!')
            else:
                print('VOCÊ PERDEU!')


if __name__ == '__main__':
    prepare_game()

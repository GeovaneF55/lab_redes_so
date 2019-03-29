# -*- coding: utf-8 -*- 

import socket
import enum

Player = enum.Enum('Player', 'NONE ONE TWO')

def get_address():
    """ Retorna o endereço IP local da máquina . """

    try:
        address = socket.gethostbyname(socket.gethostname())
    except:
        address = None
    finally:
        # Caso ocorra uma exceção, ou o endereço retornado seja
        # seja o endereço de loopback (127.x.x.x), conectar a
        # uma rede externa para que se utilize a interface correta.
        if not address or address.startswith("127."):
            host = "8.8.8.8"
            port = 80
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.connect((host, port))

            address = sock.getsockname()[0]

            sock.close()

        return address


def mark_board(board, player_id, x, y):
    """ Marca a opção do jogador no tabuleiro. 
    
    @param board Tabuleiro do jogo.
    @param player_id Identificador do jogador.
    @param x Coordenada <x> do tabuleiro.
    @param y Coordenada <y> do tabuleiro.
    """

    if Player(player_id) == Player.ONE:
        board[x][y] = 'X'
    else: 
        board[x][y] = 'O'

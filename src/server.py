# -*- coding: utf-8 -*- 

import random
import time
import threading

from room import create_room

def init_server():
    """ Função auxiliar para criar novas salas de jogos. """

    # Quantidade de salas (threads).
    n = 3

    for i in range(n):
        # Cada sala é criada como uma nova thread.
        threading.Thread(target=create_room, args=(i + 1, )).start()
        time.sleep(0.1)

if __name__ == '__main__':
    init_server()

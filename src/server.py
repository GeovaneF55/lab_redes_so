# -*- coding: utf-8 -*- 

import random
import time
import threading

from room import create_room

def init_server():
    """ Função auxiliar para criar novas salas de jogos. """

    # Quantidade de salas (threads).
    n = 3

    for i in range(1, n):
        # Cada sala é criada como uma nova thread.
        threading.Thread(target=create_room, args=(i, )).start()
        time.sleep(0.1)

if __name__ == '__main__':
    init_server()

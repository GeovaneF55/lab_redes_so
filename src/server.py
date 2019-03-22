# -*- coding: utf-8 -*- 

import random
import time
import threading

from room import create_room

if __name__ == '__main__':
    # Quantidade de salas (threads).
    n = 3

    for i in range(1, n):
        # Cada sala é criada como uma nova thread.
        threading.Thread(target=create_room).start()
        time.sleep(0.1)

# -*- coding: utf-8 -*- 

import random
import time
import threading

from room import create_room

if __name__ == '__main__':
    # Sala 1.
    threading.Thread(target=create_room).start()
    
    # Sala 2.
    time.sleep(0.1)
    threading.Thread(target=create_room).start()
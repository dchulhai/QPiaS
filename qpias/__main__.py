#!/usr/bin/env python3

from qpias.run import Start_Game

if __name__ == '__main__':
    try:
        Start_Game()
    except KeyboardInterrupt:
        exit(1)

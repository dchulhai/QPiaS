#!/usr/bin/env python3

from .qpias import start_game

if __name__ == '__main__':
    try:
        start_game()
    except KeyboardInterrupt:
        exit(1)

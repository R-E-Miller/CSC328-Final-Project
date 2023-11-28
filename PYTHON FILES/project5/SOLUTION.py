#!/usr/bin/env python3

import socket
import sys

def really_read(s, n):

    bytes = b''
    while len(bytes) != n:
        bytes += s.recv(n - len(bytes))
        if len(bytes) == 0:
            break
    return bytes

def main():

    if len(sys.argv) != 3:
        exit('Usage: <host> <port>')

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(sys.argv[1], int(sys.argv[2]))
            while True:
                word_length = int.from_bytes(really_read(s, 2), 'big')
                if word_length == 0:
                    break
                word = really_read(word_length)
                print(word.decode())

    except OSError as e:
        exit(f'{e}')

if __name__ == "__main__":
    main()

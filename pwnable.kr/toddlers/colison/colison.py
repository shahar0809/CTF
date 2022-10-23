from pwn import *

conn = remote('localhost', 9007)
print(conn.recv().decode())

def send_indexes(indexes):
    indexes = [str(x) for x in indexes]
    client_str = ' '.join(indexes)
    #print(client_str)
    conn.sendline(client_str)
    resp = conn.recvline().decode()
    #print("[Response] {}".format(resp))
    return int(resp)


def get_coin(start, end_seq, counter=0):
    if end_seq - start == 1:
        res1 = send_indexes([start])

        if res1 % 10 == 0:
            return start + 1, counter
        else:
            return start, counter
    elif end_seq - start == 0:
        return start
    elif end_seq - start == 2:
        res1 = send_indexes([start, start + 1])

        if res1 % 10 != 0:
            return get_coin(start, start + 1, counter + 1)
        else:
            return start + 2, counter
    else:
        length = end_seq - start + 1
        res1 = send_indexes(list(range(start, start + int(length / 2))))
        if res1 % 10 != 0:
            return get_coin(start, start + int(length / 2) - 1, counter + 1)
        else:
            return get_coin(start + int(length / 2), end_seq, counter + 1)


for i in range(100):
    # Get N and C
    data = conn.recvline().decode()
    N, C = data.split(" ")
    N = int(N[2:])
    C = int(C[2:len(C) - 1])

    #print("[N] {} | [C] {}".format(N, C))

    coin, counter = get_coin(0, N - 1)
    #print("DONE {}".format(i))
    #print(counter)

    for j in range(C - counter - 1):
        conn.sendline("0")
        conn.recvline()

    conn.sendline(str(coin))

    print(conn.recv().decode())
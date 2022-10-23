def rev_hex(s):
    s = s[2:]
    st = [s[x:x+2] for x in range(0, len(s), 2)]
    return ''.join(st[::-1])

hexes = [
	0x2e585055,
    0x203f2e2e,
    0x6e756f73,
    0x6c207364,
    0x20656b69,
    0x65642061,
    0x6576696c,
    0x73207972,
    0x69767265,
    0x3a206563,
    0x2e585055,
    0x203f2e2e,
    0x6e756f73,
    0x6c207364,
    0x20656b69,
    0x65642061,
    0x6576696c,
    0x73207972,
    0x69767265,
    0x3a206563
]

out = [rev_hex(hex(x)) for x in hexes]
out += [hex(0x29)[2:]]

out = [bytearray.fromhex(x).decode() for x in out]
print(len(out))
print(''.join(out))

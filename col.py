from pwn import *
import struct

# col
host = 'pwnable.kr'
user = 'col'
password = 'guest'
port = 2222

# Notes
#  * Hash function is simply sum of the (little endian) words of the password
#    modulo 0x100000000
#  * Cracked it through trial and error (binary search)

def attack():
  s = ssh(host=host, user=user, password=password, port=port)
  p = s.process(['./col', 'zWAbzzeizzzyNzzz0CAb'])
  print p.recvall()

if __name__ == '__main__':
  attack()

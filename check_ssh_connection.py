#!/usr/bin/env python3
# vim: fdm=marker fdl=0

"""
 The script tests ssh connection given a range of IP address and username. One successfull ssh connection means given an username and an IP address, you can successfully login that remote without password. It requires that one of your ssh public keys are authorized by the remote, so that you can ssh to the remote machine without password.

 Prerequisites:
 - one of your host ssh public keys are authorized by the remote, so that you can ssh to the remote machine without password.

 If you cannot ssh to a remote machine without password, you can run the following command to set up a non-password ssh.

  ssh-copy-id -i ~/.ssh/rice_rsa.pub username@remote_ip
"""

import subprocess
import os

def make_ip(chunk1, chunk2, chunk3, chunk4):# {{{
  """
  connect chunk1.chunk2.chunk3.chunk4 to make a syntax-valid ip address
  """

  ip = []
  for i1 in chunk1:
    for i2 in chunk2:
      for i3 in chunk3:
        for i4 in chunk4:
          ip += [str(i1) + '.' + str(i2) + '.' + str(i3) + '.' + str(i4)]
  return ip
# }}}
def connect(ip_list):# {{{
  """
  tssh-copy-id -i ~/.ssh/rice_rsa.pub username@remote_ipry ssh connection for each ip in ip_list
  return: a list of IP that can be successfully sshed
  """

  fnull    = open(os.devnull, 'w')
  valid_ip = []
  for ip in ip_list:
    try:
      print('connecting %s ... ' % ip, flush=True, end="")
      subprocess.check_call(["ssh", "-q",
          "-o", "UserKnownHostsFile=/dev/null",
          "-o", "StrictHostKeyChecking=no",
          "-o", "ConnectTimeout=2",
          "-o", "BatchMode=yes",
          "%s@%s" % (username, ip),
          "exit"],
          stderr=fnull)
      valid_ip.append(ip)
      print('OK')
    except subprocess.CalledProcessError:
      print('failed', flush=True)

  fnull.close()
# }}}

if __name__ == '__main__':
  username = 'rice'
  chunk1   = ["101"]
  chunk2   = ["6"]
  chunk3   = ["240", "241"]
  chunk4   = range(1, 255)

  ip_list  = make_ip(chunk1, chunk2, chunk3, chunk4)
  valid_ip = connect(ip_list)

  print("\nvalid ip:", valid_ip)

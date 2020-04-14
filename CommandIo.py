r"""A collection of classes to communicate with child processes.

This module allows you to spawn child processes,
connect to their stdin/stdout/stderr and communicate with them
for multiple times until they exit.
"""

__author__ = "Takashi SASAKI <takashi316@gmail.com>"
__date__ = "2020/04/13"
__version__ ="0.0.1.20200413"

import subprocess, select,sys

class CommandIo(object):
  __slots__ = ["_popen", "_stdinPoll", "_stdoutPoll", "_stderrPoll"]

  """
  class CommandIo is an alternative to subprocess.Popen.
  It provides communicate() method to get line-by-line output of the child process.
  """
  def __init__(self, args: list):
    """
    :param args: list of strings representing command line
    """
    self._popen = subprocess.Popen(args, 
    					stdin=subprocess.PIPE, 
					stdout=subprocess.PIPE,
					stderr=subprocess.PIPE)
    self._stdinPoll = select.poll()
    self._stdinPoll.register(self._popen.stdin, select.POLLOUT)
    self._stdoutPoll = select.poll()
    self._stdoutPoll.register(self._popen.stdout, select.POLLIN)
    self._stderrPoll = select.poll()
    self._stderrPoll.register(self._popen.stderr, select.POLLIN)
    
  def communicate(self, inBytes :bytes  = None, timeout :int = 0):
    """
    :param inBytes: data fed to stdin of the child process
    :param timeout: timeout milliseconds to wait for the response of child process
    :return outs, errs: list of bytes read line-by-line from stdout and stderr of the child process by readline()
    """
    if inBytes is not None:
      if len(self._stdinPoll.poll(timeout)) > 0:
        self._popen.stdin.write(inBytes)
        self._popen.stdin.flush()
      
    #print("reading from stdout")
    readFromStdout = []
    while len(self._stdoutPoll.poll(timeout)) > 0:
      line = self._popen.stdout.readline()
      if line == b"": break
      readFromStdout.append(line)

    #print("reading from stderr")
    readFromStderr = []
    while len(self._stderrPoll.poll(timeout)) > 0:
      line = self._popen.stderr.readline()
      if line == b"": break
      readFromStderr.append(line)
    
    return (readFromStdout, readFromStderr)

  def write(self, b:bytes, timeout:int = 100):
    if len(self._stdinPoll.poll(timeout)) > 0:
      self._popen.stdin.write(b)
      self._popen.stdin.flush()
    else:
      raise RuntimeError("Failed to write bytes to stdin of the child process.")

  def readlines(self, nLines: int, timeout:int):
    """
    :param nLines: the number of lines to wait for at least.
    :param timeout: max milliseconds to wait for the first line.
    :return : list of bytes read line-by-line from stdout of the child process.
    """
    currentTimeout = 1
    readFromStdout = []

    while True:
      #print("CommandIo.read: ", currentTimeout)
      pollResult = self._stdoutPoll.poll(currentTimeout)
      #print("CommandIo.read: ", pollResult)
      if len(pollResult) == 0:
        if currentTimeout >= timeout:
          return readFromStdout
        currentTimeout = min(timeout, currentTimeout*2)
        continue
      line = self._popen.stdout.readline()
      #print("CommandIo.read: ", line)
      if line == b"": 
        return readFromStdout
      readFromStdout.append(line)
      if len(readFromStdout) >= nLines:
        return readFromStdout

  def communicateRead(self, inBytes :bytes = None, timeout :int = 0):
    """
    :param inBytes: data fed to stdin of the child process
    :param timeout: timeout milliseconds to wait for the response of child process
    :return outs, errs: list of bytes read from stdout and stderr of the child process by readlines()
    """
    if inBytes is not None:
      if len(self._stdinPoll.poll(timeout)) > 0:
        self._popen.stdin.write(inBytes)
        self._popen.stdin.flush()
      
    #print("reading from stdout")
    readFromStdout = []
    if len(self._stdoutPoll.poll(timeout)) > 0:
      readFromStdout = self._popen.stdout.read()

    #print("reading from stderr")
    readFromStderr = []
    if len(self._stderrPoll.poll(timeout)) > 0:
      readFromStderr = self._popen.stderr.read()
    
    return (readFromStdout, readFromStderr)

  def communicatePopen(self, inBytes :bytes  = None, timeout :int = 0):
    """
    alias for Popen.communicate().
    :param inBytes: data fed to stdin of the child process
    :param timeout: timeout milliseconds to wait for the response of child process
    :return outs, errs: return values of Popen.communicate()
    """
    return self._popen.communicate(inBytes, timeout)

if __name__ == "__main__":
  commandIo = CommandIo(["cat"])
  out = commandIo.readlines(1, 100)
  print(out)

  commandIo = CommandIo(["ls"])
  out, err = commandIo.communicate(None, 100)
  print(out)

  commandIo = CommandIo(["ls"])
  out, err = commandIo.communicateRead(None, 100)
  print(out)

  commandIo = CommandIo(["ls"])
  out, err  = commandIo.communicatePopen(None, 100)
  print(out)

  commandIo = CommandIo(["locate", "id_rsa.pub"])
  out, err = commandIo.communicate(timeout = 100)
  print(out)

  commandIo = CommandIo(["telnet", "www.example.com", "80"])
  out = commandIo.readlines(10, timeout = 1000)
  print(out)
  commandIo.write(b'GET /\n')
  out = commandIo.readlines(10, timeout = 1000)
  print(out)


import subprocess, select,sys

class CommandIo:
  def __init__(self, args):
    self.popen = subprocess.Popen(args, 
    					stdin=subprocess.PIPE, 
					stdout=subprocess.PIPE,
					stderr=subprocess.PIPE)
    self.stdinPoll = select.poll()
    self.stdinPoll.register(self.popen.stdin, select.POLLOUT)
    self.stdoutPoll = select.poll()
    self.stdoutPoll.register(self.popen.stdout, select.POLLIN)
    self.stderrPoll = select.poll()
    self.stderrPoll.register(self.popen.stderr, select.POLLIN)
    
  def communicate(self, inBytes = None, timeout = 0):
    if inBytes is not None:
      if len(self.stdinPoll.poll(timeout)) > 0:
        self.popen.stdin.write(inBytes)
        self.popen.stdin.flush()
      
    #print("reading from stdout")
    readFromStdout = []
    while len(self.stdoutPoll.poll(timeout)) > 0:
      line = self.popen.stdout.readline()
      if line == b"": break
      readFromStdout.append(line)

    #print("reading from stderr")
    readFromStderr = []
    while len(self.stderrPoll.poll(timeout)) > 0:
      line = self.popen.stderr.readline()
      if line == b"": break
      readFromStderr.append(line)
    
    return (readFromStdout, readFromStderr)

  def communicateRead(self, inBytes = None, timeout = 0):
    if inBytes is not None:
      if len(self.stdinPoll.poll(timeout)) > 0:
        self.popen.stdin.write(inBytes)
        self.popen.stdin.flush()
      
    #print("reading from stdout")
    readFromStdout = []
    if len(self.stdoutPoll.poll(timeout)) > 0:
      readFromStdout = self.popen.stdout.read()

    #print("reading from stderr")
    readFromStderr = []
    if len(self.stderrPoll.poll(timeout)) > 0:
      readFromStderr = self.popen.stderr.read()
    
    return (readFromStdout, readFromStderr)

  def communicatePopen(self, inBytes = None, timeout = 0):
    return self.popen.communicate(inBytes, timeout)

if __name__ == "__main__":
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
  out, err = commandIo.communicate(None, timeout = 1000)
  print(out)
  out, err = commandIo.communicate(b'GET /\n', timeout = 1000)
  print(out)


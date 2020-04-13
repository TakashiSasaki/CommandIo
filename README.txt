Help on module CommandIo:

NAME
    CommandIo

CLASSES
    builtins.object
        CommandIo
    
    class CommandIo(builtins.object)
     |  Methods defined here:
     |  
     |  __init__(self, args:list)
     |      :param args: list of strings representing command line
     |  
     |  communicate(self, inBytes:bytes=None, timeout:int=0)
     |      :param inBytes: data fed to stdin of the child process
     |      :param timeout: timeout milliseconds to wait for the response of child process
     |      :return outs, errs: list of bytes read line-by-line from stdout and stderr of the child process by readline()
     |  
     |  communicatePopen(self, inBytes:bytes=None, timeout:int=0)
     |      alias for Popen.communicate().
     |      :param inBytes: data fed to stdin of the child process
     |      :param timeout: timeout milliseconds to wait for the response of child process
     |      :return outs, errs: return values of Popen.communicate()
     |  
     |  communicateRead(self, inBytes:bytes=None, timeout:int=0)
     |      :param inBytes: data fed to stdin of the child process
     |      :param timeout: timeout milliseconds to wait for the response of child process
     |      :return outs, errs: list of bytes read from stdout and stderr of the child process by readlines()

DATE
    2020/04/13

AUTHOR
    Takashi SASAKi <takashi316@gmail.com>

FILE
    /home/mobaxterm/command-io/CommandIo.py



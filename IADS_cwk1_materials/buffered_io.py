
# Inf2-IADS Coursework 1, October 2019
# Python source file: buffered_io.py

# Classes for buffered file IO, very similar (though not identical)
# to those in Python Lab Sheet 3


MemoryAllowance = 1000000  # bytes
# goal is to see how to process 'large' files using 'small' working memory

class BufferedInput:
    def __init__(self,filename,memoryShare):
        global MemoryAllowance
        self.reader = open(filename,'r',encoding='utf-8')
        self.maxSize = int(MemoryAllowance * memoryShare)
        self.buffer = self.reader.readlines(self.maxSize-500)
                      # to allow for lines of length <= 500
        self.pos = 0
    def readline(self):
        if self.buffer == []:
            return ''
        else:
            result = self.buffer[self.pos]
            self.pos += 1
            if self.pos == len(self.buffer):
                self.buffer = self.reader.readlines(self.maxSize-500)
                self.pos = 0
            return result
    def readchunk(self): # returns entire buffer contents
        currBuffer = self.buffer
        self.buffer = self.reader.readlines(self.maxSize-500)
        self.pos = 0
        return currBuffer
    def close(self):
        self.reader.close()
	
class BufferedOutput:
    def __init__(self,filename,memoryShare):
        global MemoryAllowance
        self.writer = open(filename,'w',encoding='utf-8')
        self.maxSize = int(MemoryAllowance * memoryShare)
        self.buffer = [''] * (self.maxSize // 10)
        # at most this many output lines will fit, as each line has length >= 10
        self.pos = 0        # next free position in buffer
        self.currSize = 0   # number of bytes used so far (estimate)
    def writeline(self,str):
        newSize = self.currSize + len(str) + 4
                  # allow overhead of 4 bytes per string (estimate)
        if newSize > self.maxSize:
            self.writer.writelines(self.buffer[:self.pos])
            newSize = len(str) + 4
            self.pos = 0
        self.buffer[self.pos] = str
        self.pos += 1
        self.currSize = newSize
    def flush(self): # flushes buffer and closes file
        self.writer.writelines(self.buffer[:self.pos])
        self.writer.close()

# End of file

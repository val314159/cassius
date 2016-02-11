from errno import ENOENT
from time import time
from fuse import FUSE, FuseOSError, Operations

class ReadOps(Operations):
    def ropen(self, path, flags):
        print "ROPEN", path, flags
        self.fd += 1
        return self.fd
    def getattr(self, path, fh=None):
        print "GETATTR", path, fh
        if path not in self.files:
            raise FuseOSError(ENOENT)
        return self.files[path]
    def read(self, path, size, offset, fh):
        print "READ", path, size, offset, fh
        return self.data[path][offset:offset + size]
    def readdir(self, path, fh):
        print "READDIR", path, fh
        return ['.', '..'] + [x[1:] for x in self.files if x != '/']
    def readlink(self, path):
        print "READLINK", path
        return self.data[path]

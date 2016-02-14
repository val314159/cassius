from errno import ENOENT
from time import time
from fuse import FUSE, FuseOSError, Operations
from cass import Exec
class ReadOps(Operations):
    def ropen(self, path, flags):
        print "ROPEN", path, flags
        self.fd += 1
        return self.fd
    def getattr(self, path, fh=None):
        print "GETATTR", path, fh
        meta = {}
        for x in Exec("SELECT meta FROM inodes WHERE pathname=%s", (self.pfx+'/'+path,)):
            meta = x.meta
        if not meta:
            raise FuseOSError(ENOENT)
        return meta
    def read(self, path, size, offset, fh):
        print "READ", path, size, offset, fh
        data = self._read_all(path, fh)
        return data[offset:offset + size]
    def readdir(self, path, fh):
        print "READDIR", path, fh
        files = []
        for x in Exec("SELECT pathname FROM inodes"):
            name = x.pathname[len(self.pfx)+2:]
            if name:
                files.append( name )
        return ['.', '..'] + files#[x[1:] for x in self.files if x != '/']
    def readlink(self, path):
        print "READLINK", path
        return self._read_all(path, None)

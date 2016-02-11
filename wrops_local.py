from errno import ENOENT
from time import time
from fuse import FUSE, FuseOSError, Operations
import os
class LocalWriteOps(Operations):
    def chmod(self, path, mode):
        print "CHMOD", path, mode
        os.chmod(self.pfx+path, mode)
    def chown(self, path, uid, gid):
        print "CHOWN", path, uid, gid
        os.chown(self.pfx+path, uid, gid)
    def utimens(self, path, times=None):
        print "UTIMENS", path, times
        os.utime(self.pfx+path, times)
    def rename(self, path, new):
        print "RENAME", path, new
        os.rename(self.pfx+path, self.pfx+new)
    def rmdir(self, path):
        print "RMDIR", path
        os.rmdir(self.pfx+path)
    def truncate(self, path, length, fh=None):
        print "TRUNC", path, length, fh
        with open(self.pfx+path,'w+') as f:
            f.truncate(length)
    def unlink(self, path):
        print "UNLINK", path
        os.unlink(self.pfx+path)
    def symlink(self, path, source):
        print "SYMLINK", path, source
        os.symlink(self.pfx+source, self.pfx+path)
    def mkdir(self, path, mode):
        print "MKDIR", path, mode
        os.mkdir(self.pfx+path, mode)
    def create(self, path, mode):
        print "CREATE", path, mode
        os.open(self.pfx+path,
                os.O_WRONLY|os.O_CREAT, mode)
        return self.fd
    def wopen(self, path, flags):
        print "WOPEN", path, flags        
        return self.fd
    def write(self, path, data, offset, fh):
        print "WRITE", path, data, offset, fh
        with open(self.pfx+path,'w+') as f:
            f.seek(offset, 0)
            ret = f.write(fh, data)
        return ret


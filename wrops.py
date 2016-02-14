from errno import ENOENT
from time import time
from fuse import FUSE, FuseOSError, Operations
import os
class WriteOps(Operations):
    def chmod(self, path, mode):
        print "CHMOD", path, mode
        self.files[path]['st_mode'] &= 0770000
        self.files[path]['st_mode'] |= mode
        #os.chmod(self.pfx+path, mode)
    def chown(self, path, uid, gid):
        print "CHOWN", path, uid, gid
        self.files[path]['st_uid'] = uid
        self.files[path]['st_gid'] = gid
        #os.chown(self.pfx+path, uid, gid)
    def utimens(self, path, times=None):
        print "UTIMENS", path, times
        now = time()
        atime, mtime = times if times else (now, now)
        self.files[path]['st_atime'] = atime
        self.files[path]['st_mtime'] = mtime
        #os.utime(self.pfx+path, times)
    def rename(self, path, new):
        print "RENAME", path, new
        self.files[new] = self.files.pop(path)
        #os.rename(self.pfx+path, self.pfx+new)
    def rmdir(self, path):
        print "RMDIR", path
        self.files.pop(path)
        self.files['/']['st_nlink'] -= 1
        #os.rmdir(self.pfx+path)
    def truncate(self, path, length, fh=None):
        print "TRUNC", path, length, fh
        self.data[path] = self.data[path][:length]
        self.files[path]['st_size'] = length
        #with open(self.pfx+path,'w+') as f:
        #    f.truncate(length)
    def unlink(self, path):
        print "UNLINK", path
        self.files.pop(path)
        #os.unlink(self.pfx+path)
    def symlink(self, path, source):
        print "SYMLINK", path, source
        self.mk_node(path,'L', sz=len(source))
        self.data[path] = source
        #os.symlink(self.pfx+source, self.pfx+path)
    def mkdir(self, path, mode):
        print "MKDIR", path, mode
        self.mk_node(path,'D',mode)
        self.files['/']['st_nlink'] += 1
        #os.mkdir(self.pfx+path, mode)
    def create(self, path, mode):
        print "CREATE", path, mode
        self.mk_node(path,'F',mode)
        self.fd += 1
        #os.open(self.pfx+path,
        #        os.O_WRONLY|os.O_CREAT, mode)
        return self.fd
    def wopen(self, path, flags):
        print "WOPEN", path, flags        
        self.fd += 1
        return self.fd
    def write(self, path, data, offset, fh):
        print "WRITE", path, data, offset, fh
        self.data[path] = self.data[path][:offset] + data
        self.files[path]['st_size'] = len(self.data[path])
        #with open(self.pfx+path,'w+') as f:
        #    f.seek(offset, 0)
        #    ret = f.write(fh, data)
        return len(data)

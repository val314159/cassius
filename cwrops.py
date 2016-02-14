from errno import ENOENT
from time import time
from fuse import FUSE, FuseOSError, Operations
import os
from cass import Exec
class WriteOps(Operations):
    def chmod(self, path, mode):
        print "CHMOD", path, mode
        self.files[path]['st_mode'] &= 0770000
        self.files[path]['st_mode'] |= mode
        Exec("UPDATE inodes SET meta['st_mode']=%s WHERE pathname=%s", (mode, self.pfx+'/'+path))
    def chown(self, path, uid, gid):
        print "CHOWN", path, uid, gid
        self.files[path]['st_uid'] = uid
        self.files[path]['st_gid'] = gid
        Exec("UPDATE inodes SET meta['st_uid']=%s WHERE pathname=%s", (uid, self.pfx+'/'+path))
        Exec("UPDATE inodes SET meta['st_gid']=%s WHERE pathname=%s", (gid, self.pfx+'/'+path))
    def utimens(self, path, times=None):
        print "UTIMENS", path, times
        now = time()
        atime, mtime = times if times else (now, now)
        self.files[path]['st_atime'] = atime
        self.files[path]['st_mtime'] = mtime
        atime = int(atime)
        mtime = int(mtime)
        Exec("UPDATE inodes SET meta['st_atime']=%s WHERE pathname=%s", (atime, self.pfx+'/'+path))
        Exec("UPDATE inodes SET meta['st_mtime']=%s WHERE pathname=%s", (mtime, self.pfx+'/'+path))
    def rename(self, path, new):
        print "RENAME", path, new
        self.files[new] = self.files.pop(path)
        #os.rename(self.pfx+path, self.pfx+new)
    def rmdir(self, path):
        print "RMDIR", path
        self.files.pop(path)
        self.files['/']['st_nlink'] -= 1
        Exec("DELETE FROM inodes WHERE pathname=%s", (self.pfx+'/'+path,))
    def unlink(self, path):
        print "UNLINK", path
        self.files.pop(path)
        Exec("DELETE FROM  inodes  WHERE pathname=%s", (self.pfx+'/'+path,))
        Exec("DELETE FROM filedata WHERE pathname=%s", (self.pfx+'/'+path,))
    def symlink(self, path, source):
        print "SYMLINK", path, source
        self.mk_node(path,'L', sz=len(source))
        self.data[path] = source
        Exec("INSERT INTO filedata data=%s WHERE pathname=%s", (source, self.pfx+'/'+path,))
    def mkdir(self, path, mode):
        print "MKDIR", path, mode
        self.mk_node(path,'D',mode)
        self.files['/']['st_nlink'] += 1
    def create(self, path, mode):
        print "CREATE", path, mode
        self.mk_node(path,'F',mode)
        self.fd += 1
        Exec("INSERT INTO filedata (pathname,data) VALUES (%s,%s)", (self.pfx+'/'+path,''))
        return self.fd
    def wopen(self, path, flags):
        print "WOPEN", path, flags        
        self.fd += 1
        return self.fd
    def truncate(self, path, length, fh=None):
        print "TRUNC", path, length, fh
        self.data[path] = self.data[path][:length]
        self.files[path]['st_size'] = length
        data = self._read_all(path, fh)
        data = data[:length]
        return self._write_all(path, data)
    def write(self, path, data, offset, fh):
        print "WRITE", path, data, offset, fh
        self.data[path] = self.data[path][:offset] + data
        self.files[path]['st_size'] = len(self.data[path])
        data = self._read_all(path, fh)
        data = data[:offset] + data
        return self._write_all(path, data)
    def _read_all(self, path, fh):
        print "123"
        rs = Exec("SELECT data FROM filedata WHERE pathname=%s", (self.pfx+'/'+path,))
        print "123x"
        data = ''
        print "123y"
        for x in rs: data = x.data
        return data
    def _write_all(self, path, data):
        Exec("UPDATE  inodes  SET meta['st_size']=%s WHERE pathname=%s", (len(data), self.pfx+'/'+path,))
        Exec("UPDATE filedata SET data=%s            WHERE pathname=%s", (data, self.pfx+'/'+path,))
        return len(data)

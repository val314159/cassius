from errno import ENOENT
from time import time
from fuse import FUSE, FuseOSError, Operations
from cass import Exec
class WriteOps(Operations):
    def chmod(self, path, mode):
        print "CHMOD", path, mode
        Exec("UPDATE inodes SET meta['st_mode']=%s WHERE pathname=%s", (mode, self.pfx+'/'+path))
    def chown(self, path, uid, gid):
        print "CHOWN", path, uid, gid
        Exec("UPDATE inodes SET meta['st_uid']=%s WHERE pathname=%s", (uid, self.pfx+'/'+path))
        Exec("UPDATE inodes SET meta['st_gid']=%s WHERE pathname=%s", (gid, self.pfx+'/'+path))
    def utimens(self, path, times=None):
        print "UTIMENS", path, times
        now = time()
        atime, mtime = times if times else (now, now)
        atime = int(atime)
        mtime = int(mtime)
        Exec("UPDATE inodes SET meta['st_atime']=%s WHERE pathname=%s", (atime, self.pfx+'/'+path))
        Exec("UPDATE inodes SET meta['st_mtime']=%s WHERE pathname=%s", (mtime, self.pfx+'/'+path))
    def rename(self, path, new):
        print "RENAME", path, new
    def rmdir(self, path):
        print "RMDIR", path
        Exec("DELETE FROM inodes WHERE pathname=%s", (self.pfx+'/'+path,))
    def unlink(self, path):
        print "UNLINK", path
        Exec("DELETE FROM  inodes  WHERE pathname=%s", (self.pfx+'/'+path,))
        Exec("DELETE FROM filedata WHERE pathname=%s", (self.pfx+'/'+path,))
    def symlink(self, path, source):
        print "SYMLINK", path, source
        self.mk_node(path,'L', sz=len(source))
    def mkdir(self, path, mode):
        print "MKDIR", path, mode
        self.mk_node(path,'D',mode)
    def create(self, path, mode):
        print "CREATE", path, mode
        self.mk_node(path,'F',mode)
        self.fd += 1
        return self.fd
    def wopen(self, path, flags):
        print "WOPEN", path, flags        
        self.fd += 1
        return self.fd
    def truncate(self, path, length, fh=None):
        print "TRUNC", path, length, fh
        old_data = self._read_all(path, fh)
        old_data = old_data[:length]
        self._write_all(path, old_data)
    def write(self, path, data, offset, fh):
        print "WRITE", path, data, offset, fh
        endp = offset+len(data)
        old_data = self._read_all(path, fh)
        old_data = old_data[:offset] + data + old_data[endp:]
        self._write_all(path, old_data)
        return len(data)
    def _read_all(self, path, fh):
        rs = Exec("SELECT data FROM filedata WHERE pathname=%s", (self.pfx+'/'+path,))
        data = ''
        for x in rs: data = x.data
        return data
    def _write_all(self, path, data):
        Exec("UPDATE  inodes  SET meta['st_size']=%s WHERE pathname=%s", (len(data), self.pfx+'/'+path,))
        Exec("UPDATE filedata SET data=%s            WHERE pathname=%s", (data, self.pfx+'/'+path,))
        return len(data)

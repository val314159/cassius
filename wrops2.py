from errno import ENOENT
from time import time
from fuse import FUSE, FuseOSError, Operations
from cass import Exec
from uuid import uuid1, uuid4
class WriteOps(Operations):
    def chmod(self, path, mode):
        print "CHMOD", path, mode
        branch, name = self._split_path(path)
        Exec("UPDATE inodes SET meta['st_mode']=%s WHERE path=%s AND name=%s", (self.pfx+'/'+branch,name))
    def chown(self, path, uid, gid):
        print "CHOWN", path, uid, gid
        branch, name = self._split_path(path)
        Exec("UPDATE inodes SET meta['st_uid']=%s WHERE path=%s AND name=%s", (uid, self.pfx+'/'+branch,name))
        Exec("UPDATE inodes SET meta['st_gid']=%s WHERE path=%s AND name=%s", (gid, self.pfx+'/'+branch,name))
    def utimens(self, path, times=None):
        print "UTIMENS", path, times
        branch, name = self._split_path(path)
        atime, mtime = times if times else (time(),)*2
        Exec("UPDATE inodes SET meta['st_atime']=%s WHERE path=%s AND name=%s", (int(atime), self.pfx+'/'+branch,name))
        Exec("UPDATE inodes SET meta['st_mtime']=%s WHERE path=%s AND name=%s", (int(mtime), self.pfx+'/'+branch,name))
    def rename(self, path, new):
        print "RENAME", path, new
        branch, name = self._split_path(path)
    def rmdir(self, path):
        print "RMDIR", path
        branch, name = self._split_path(path)
        Exec("DELETE FROM inodes WHERE path=%s AND name=%s", (self.pfx+'/'+branch,name))
    def unlink(self, path):
        print "UNLINK", path
        branch, name = self._split_path(path)
        Exec("DELETE FROM  inodes  WHERE path=%s AND name=%s", (self.pfx+'/'+branch,name))
        Exec("DELETE FROM filedata WHERE path=%s AND name=%s", (self.pfx+'/'+branch,name))
    def symlink(self, path, source):
        print "SYMLINK", path, source
        branch, name = self._split_path(path)
        self.mk_node(path,'L', sz=len(source))
    def mkdir(self, path, mode):
        print "MKDIR", path, mode
        branch, name = self._split_path(path)
        self.mk_node(path,'D',mode)
    def create(self, path, mode):
        print "CREATE", path, mode
        branch, name = self._split_path(path)
        self.mk_node(path,'F',mode)
        self.fd += 1
        return self.fd
    def wopen(self, path, flags):
        print "WOPEN", path, flags        
        branch, name = self._split_path(path)
        self.fd += 1
        return self.fd
    def truncate(self, path, length, fh=None):
        print "TRUNC", path, length, fh
        branch, name = self._split_path(path)
        old_data = self._read_all(path, fh)
        self._write_all(path, old_data[:length])
    def write(self, path, data, offset, fh):
        branch, name = self._split_path(path)
        print "WRITE", path, data, offset, fh
        branch, name = self._split_path(path)
        endp = offset+len(data)
        old_data = self._read_all(path, fh)
        self._write_all(path, old_data[:offset] + data + old_data[endp:])
        return len(data)
    def _write_all(self, path, data):
        branch, name = self._split_path(path)
        Exec("UPDATE  inodes  SET meta['st_size']=%s WHERE path=%s AND name=%s", (len(data), self.pfx+'/'+branch,name))
        Exec("UPDATE filedata SET data=%s            WHERE path=%s AND name=%s", (    data , self.pfx+'/'+branch,name))
        return len(data)
    def _split_path(self, path): return path.rsplit('/',1)
    def _save_node(self, path, meta):
        branch, name = self._split_path(path)
        Exec("INSERT into inodes (iid,path,name,meta) VALUES (%s,%s,%s,%s) IF NOT EXISTS", (uuid1(), self.pfx+'/'+branch, name, meta))

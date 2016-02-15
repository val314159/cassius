from errno import ENOENT
from time import time
from fuse import FUSE, FuseOSError, Operations
from cassius.schema import Exec
from uuid import uuid1, uuid4
class WriteOps(Operations):
    def _write_all(self, path, data):
        branch, name = self._split_path(path)
        meta = self.getattr(path)
        print "META", meta
        Exec("UPDATE  inodes  SET meta['st_size']=%s WHERE path=%s AND name=%s", (len(data), self.pfx+'/'+branch,name))
        Exec("UPDATE filedata SET data=%s           WHERE iid=%s", (data , meta['iid']))
        return len(data)
    def _save_node(self, path, meta):
        branch, name = self._split_path(path)
        print " *****1 SAVENODE: PATH BRANCH NAME", repr((path, branch, name))
        pid = None
        if name:
            bbranch, bname = self._split_path(branch)
            parent = self.getattr(branch)
            print " *****2 PARENT", repr((path, branch, name, parent))
            pid = parent['iid']
            Exec("UPDATE inodes SET meta['st_nlink']=%s WHERE path=%s AND name=%s",
                 (parent['st_nlink']+1, self.pfx+'/'+bbranch, bname))
            pass
        Exec("INSERT into inodes (iid,pid,path,name,meta) VALUES (%s,%s,%s,%s,%s) IF NOT EXISTS", (uuid1(), pid, self.pfx+'/'+branch, name, meta))
    def _del_node(self, path):
        branch, name = self._split_path(path)
        meta = self.getattr(path)
        Exec("DELETE FROM filedata WHERE iid=%s", (meta['iid'],))
        Exec("DELETE FROM  inodes  WHERE path=%s AND name=%s", (self.pfx+'/'+branch,name))
    def _set_attr(self, path, attr, mode):
        branch, name = self._split_path(path)
        Exec("UPDATE inodes SET meta[%s]=%s WHERE path=%s AND name=%s", (attr,self.pfx+'/'+branch,name))

    def chmod(self, path, mode):
        print "CHMOD", path, mode
        branch, name = self._split_path(path)
        self._set_attr(path, "st_mode", mode)
    def chown(self, path, uid, gid):
        print "CHOWN", path, uid, gid
        branch, name = self._split_path(path)
        self._set_attr(path, "st_uid", uid)
        self._set_attr(path, "st_gid", gid)
    def utimens(self, path, times=None):
        print "UTIMENS", path, times
        branch, name = self._split_path(path)
        atime, mtime = times if times else (time(),)*2
        self._set_attr(path, "st_atime", atime)
        self._set_attr(path, "st_mtime", mtime)
    def rename(self, path, new):
        print "RENAME", path, new
        branch, name = self._split_path(path)
    def rmdir(self, path):
        print "RMDIR", path
        branch, name = self._split_path(path)
        self._del_node(path)
    def unlink(self, path):
        print "UNLINK", path
        branch, name = self._split_path(path)
        self._del_node(path)
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
        self._write_all(path, self._read_all(path, fh)[:length])
    def write(self, path, data, offset, fh):
        print "WRITE", path, data, offset, fh
        branch, name = self._split_path(path)
        endp = offset+len(data)
        old_data = self._read_all(path, fh)
        self._write_all(path, old_data[:offset] + data + old_data[endp:])
        return len(data)

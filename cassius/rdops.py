from errno import ENOENT
from time import time
from fuse import FUSE, FuseOSError, Operations
from cassius.schema import Exec
class ReadOps(Operations):
    def ropen(self, path, flags):
        print "ROPEN", path, flags
        branch, name = self._split_path(path)
        self.fd += 1
        return self.fd
    def getattr(self, path, fh=None):
        path = path or '/'
        print "GETATTR", path, fh
        branch, name = self._split_path(path)
        return self._getattr( path, fh )
    def read(self, path, size, offset, fh):
        print "READ", path, size, offset, fh
        branch, name = self._split_path(path)
        endp = None if size is None else offset + size
        return self._read_all(path, fh)[offset:endp]
    def readlink(self, path):
        print "READLINK", path
        branch, name = self._split_path(path)
        return self._read_all(path, None)
    def readdir(self, path, fh):
        print "READDIR", path, fh
        branch, name = self._split_path(path)
        return ['.', '..'] + self._getlist(path, fh)

    def _getattr(self, path, fh=None):
        path = path or '/'
        print "GETATTR", path, fh
        branch, name = self._split_path(path)
        for x in Exec("SELECT iid,meta FROM inodes WHERE path=%s AND name=%s", (self.pfx+'/'+branch,name)):
            meta = dict(x.meta)
            meta['iid'] = x.iid
            return meta
        raise FuseOSError(ENOENT)
    def _getlist(self, path, fh):
        branch = self._get_branch(path)
        #branch, name = self._split_path(path)
        rs = Exec("SELECT name FROM inodes WHERE path=%s", (self.pfx+'/'+branch,))
        return [ x.name for x in rs if x.name ]
    def _read_all(self, path, fh):
        branch = self._get_branch(path)
        #branch, name = self._split_path(path)
        meta = self.getattr(path)
        print "META", meta
        for x in Exec("SELECT data FROM filedata WHERE iid=%s", (meta['iid'],)):
            return x.data
        return ''
    def _get_branch(self, path):
        branch, name = self._split_path(path)
        return branch
    def _get_branch2(self, path):
        branch, name = self._split_path(path)
        return branch

from errno import ENOENT
from stat import S_IFDIR, S_IFLNK, S_IFREG
from fuse import FUSE, FuseOSError, Operations, LoggingMixIn
class XReadOps(Operations):
    def getxattr(self, path, name, position=0):
        print "GETXATTR", path, name, position
        attrs = self.files[path].get('attrs', {})
        try:
            return attrs[name]
        except KeyError:
            return ''       # Should return ENOATTR
    def listxattr(self, path):
        print "LIST XATTR", path
        attrs = self.files[path].get('attrs', {})
        return attrs.keys()
class XWriteOps(Operations):
    def removexattr(self, path, name):
        print "REM XATTR", path, name
        attrs = self.files[path].get('attrs', {})
        try:
            del attrs[name]
        except KeyError:
            pass        # Should return ENOATTR
    def setxattr(self, path, name, value, options, position=0):
        print "SETXATTR", path, name, value, options, position
        # Ignore options
        attrs = self.files[path].setdefault('attrs', {})
        attrs[name] = value

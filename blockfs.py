#!/usr/bin/env python
import logging, os
from collections import defaultdict
from errno import ENOENT
from stat import S_IFDIR, S_IFLNK, S_IFREG
from sys import argv, exit
from time import time
from fuse import FUSE, FuseOSError, LoggingMixIn
from rdops import ReadOps
from wrops import WriteOps
from xops import XReadOps, XWriteOps

if not hasattr(__builtins__, 'bytes'):
    bytes = str

class BlockFS(LoggingMixIn, ReadOps, WriteOps):
    def __init__(self):
        print "INIT"
        self.fd, self.files = 0, {}
        self.data = defaultdict(bytes)
        self.mnt_pt = os.path.realpath('.')
        print "MNT PT:", self.mnt_pt
        self.pfx = 'mnt2/'
        return self.mk_node('/','D', 0755)
    def access(self, path, mode):       print "ACCESS", path, mode
    def release(self, path, fh):        print "RELEASE", path, fh
    def mk_node(self,  path, typ, mode=0777, sz=0):
        print "MK__NODE",path, typ, mode, sz
        if   typ in (S_IFLNK,'l','L'): typ = S_IFLNK ; nlinks = 1
        elif typ in (S_IFREG,'f','F'): typ = S_IFREG ; nlinks = 1
        elif typ in (S_IFDIR,'d','D'): typ = S_IFDIR ; nlinks = 2
        else: raise "HELL"
        self.files[path]=dict(st_mode=typ|mode,st_nlink=nlinks,st_size=sz)
        pass
    def statfs(self, path):
        print "STATFS", path
        return dict(f_bsize=512, f_blocks=4096, f_bavail=2048)
    def init   (self, path):  print " --  INIT --", path
    def destroy(self, path):  print " -- DESTROY --", path

if __name__ == '__main__':
    if len(argv) != 2:
        print('usage: %s <mountpoint>' % argv[0])
        exit(1)
    #logging.getLogger().setLevel(logging.DEBUG)
    fuse = FUSE(BlockFS(), argv[1], foreground=True, nothreads=True)

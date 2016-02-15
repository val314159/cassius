import cassandra
from cassandra.cluster import Cluster
cluster = cassandra.cluster.Cluster()
session = cluster.connect()
Exec = session.execute
try:
    session.execute('USE ks')
except cassandra.InvalidRequest,e:
    print "Keyspace does not exist, creating . . ."
    session.execute('''CREATE KEYSPACE IF NOT EXISTS ks WITH
       replication={'class':'SimpleStrategy','replication_factor':1}''')
    session.execute('USE ks')
    pass

def create_schema():
    print "CREATE SCHEMA"
    Exec('''CREATE TYPE IF NOT EXISTS address (
  street text,
  city text,
  qwert uuid,
  zip_code int,
  phones set<text>
)''')
    Exec('''CREATE TABLE IF NOT EXISTS inodes (
  pid uuid,
  iid uuid,
  path text,
  name text,
  meta map<text, int>,
  fid uuid,
PRIMARY KEY (path,name)
)''')
    Exec('''CREATE INDEX IF NOT EXISTS inodes_iid ON ks.inodes (iid)''')
    Exec('''CREATE INDEX IF NOT EXISTS inodes_pid ON ks.inodes (pid)''')

    Exec('''CREATE TABLE IF NOT EXISTS inodes2 (
  iid uuid,
  pid uuid,
  path text,
  name text,
  pathname frozen<tuple<text,text,text>>,
  meta map<text, int>,
  fid uuid,
PRIMARY KEY (pid,iid)
)''')
    Exec('''CREATE INDEX IF NOT EXISTS inodes2_iid ON ks.inodes2(iid)''')

    Exec('''CREATE TABLE IF NOT EXISTS filedata (
  iid uuid,
  fid uuid,
  version int,
  data text,
PRIMARY KEY (fid)
)''')
    Exec('''CREATE INDEX IF NOT EXISTS filedata_iid ON ks.filedata(iid)''')

def test():
    print "Running tests!"
    for x in Exec('''SELECT * FROM filedata WHERE iid=6E6EDD14-59E2-4DE2-9D64-210316827C2A;'''):
        print "X", x
    for x in Exec('''SELECT * FROM filedata WHERE fid=6E6EDD14-59E2-4DE2-9D64-210316827C2A;'''):
        print "X", x
    for x in Exec('''SELECT * FROM inodes2 WHERE pid=6E6EDD14-59E2-4DE2-9D64-210316827C2A;'''):
        print "X", x
    for x in Exec('''SELECT * FROM inodes2 WHERE pid=6E6EDD14-59E2-4DE2-9D64-210316827C2A AND
        iid=6E6EDD14-59E2-4DE2-9D64-210316827C2A;'''):
        print "X", x
    for x in Exec('''SELECT * FROM inodes2 WHERE iid=6E6EDD14-59E2-4DE2-9D64-210316827C2A;'''):
        print "X", x

create_schema()

if __name__=='__main__': test()

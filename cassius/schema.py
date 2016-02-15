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
Exec('''CREATE TABLE IF NOT EXISTS inodes (
  iid uuid,
  pid uuid,
  path text,
  name text,
  meta map<text, int>,
PRIMARY KEY (path,name)
)''')
Exec('''CREATE INDEX ON ks.inodes (iid)''')
Exec('''CREATE INDEX ON ks.inodes (pid)''')
Exec('''CREATE TABLE IF NOT EXISTS filedata (
  iid uuid,
  version int,
  data text,
PRIMARY KEY (iid)
)''')

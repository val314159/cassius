#!/usr/bin/env python
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
  pathname text PRIMARY KEY,
  meta map<text, int>
)''')
Exec('''CREATE TABLE IF NOT EXISTS filedata (
  pathname text PRIMARY KEY,
  version int,
  data text
)''')
Exec('''CREATE TABLE IF NOT EXISTS blocks (
  pathname text PRIMARY KEY,
  block_num int,
  block_data text
)''')

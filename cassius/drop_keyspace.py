#!/usr/bin/env python
import cassandra
from cassandra.cluster import Cluster
cluster = cassandra.cluster.Cluster()
session = cluster.connect()

session.execute('''DROP KEYSPACE IF EXISTS ks''')

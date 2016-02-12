Cassius - A Cassandra-Backed Filesystem
==

# Quickstart

```
# get the source
git clone https://github.com/val314159/cassius
cd cassius

# make it go
mkdir mnt
python blockfs.py mnt
```

# Install cassandra

OSX: brew install cassandra
Ubuntu: apt-get install cassandra
CentOS: *No one liner.  use google to figure this out*

# Run cassandra

`cassandra -f`
- this runs it in the foreground

# Install python cassandra driver

`pip install cassandra-driver`

# Create/find a mount point

`mkdir mnt`

# Run it

`python cassius.py mnt`

#!/bin/bash -e
echo == START ==
mkdir -p mnt/d1/d2/d3/d4
rmdir mnt/d1/d2/d3/d4
touch mnt/d1/d2/d3/f1
echo qwert yuiop1 >mnt/d1/d2/d3/f1
echo qwert yuiop2 >>mnt/d1/d2/d3/f2
echo qwert yuiop3 >>mnt/d1/d2/d3/f2
echo qwert yuiop4 >mnt/d1/d2/d3/f3
echo qwert yuiop5 >>mnt/d1/d2/d3/f3
cat mnt/d1/d2/d3/f1
cat mnt/d1/d2/d3/f2
cat mnt/d1/d2/d3/f2
cat mnt/d1/d2/d3/f3
cat mnt/d1/d2/d3/f3
ls mnt
rm mnt/d1/d2/d3/f3
ls -la mnt
touch mnt/d1/d2/d3/f1
touch mnt/d1/d2/d3/f2
echo == FINISH ==
echo 'select * from inodes;' | cqlsh -kks
echo 'select * from filedata;' | cqlsh -kks
echo == FINISH2 ==

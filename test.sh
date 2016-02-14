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
ls -la mnt
touch mnt/d1/d2/d3/f1
touch mnt/d1/d2/d3/f2
rm mnt/d1/d2/d3/f3
echo == FINISH ==

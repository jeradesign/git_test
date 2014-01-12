#!python

import koans

print "Hello Koan Test"
koans.sys_reset()
out = koans.koan_1('test',answers=['git init ./work'])
print out
out = koans.koan_2('test',answers=['touch foo','git add foo'])
print out

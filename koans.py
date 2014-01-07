#!python

__author__ = 'joelbremson'
__date__ = "1/7/14"

import os
import readline

#Test file for git koans

def reset():
    print ("Resetting koans to initial state...")
    # make this safer
    os.system("rm -rf ../git_koans/work/")
    os.system("mkdir ../git_koans/work/")


def koan_1():
    out =  raw_input("Koan 1: Init git in the /work directory... (hint: git init ./work)\n>>")
    retval = os.system(out)

    # check to see if there is a .git dir in work...

    if(os.path.isdir("./work/.git")):
        print ("Init enlightenment attained. On to the next koan.")
    else:
        print ("Try it again.")
        koan_1();


print "Welcome to git-koans..."
reset()
koan_1()

#git --git-dir=/Users/joelbremson/code/git_koans/.git --work-tree=./git_koans/ status



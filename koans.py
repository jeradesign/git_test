#!python

__author__ = 'joelbremson'
__date__ = "1/7/14"

import os
import subprocess

#Test file for git koans

def reset():
    print ("Resetting koans to initial state...")
    # make this safer
    subprocess.check_output("rm -rf ../git_test/work/",stderr=subprocess.STDOUT,shell=True)
    subprocess.check_output("mkdir ../git_test/work/",stderr=subprocess.STDOUT, shell=True)
    subprocess.check_output("touch ../git_test/work/.empty",stderr=subprocess.STDOUT, shell=True)


def koan_1():
    out =  raw_input("Koan 1: Init git in the /work directory... (hint: git init ./work)\n>>")
    retval = subprocess.check_output(out,shell=True)

    # check to see if there is a .git dir in work...

    if(os.path.isdir("./work/.git")):
        print ("\n\nInit enlightenment attained. On to the next koan! \n\n")
    else:
        print ("\n\nThrough failure learning is achieved. Try it again.\n\n")
        koan_1();


print "Welcome to git-koans..."
reset()
koan_1()

#git --git-dir=/Users/joelbremson/code/git_koans/.git --work-tree=./git_koans/ status



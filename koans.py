#!python

__author__ = 'joelbremson'
__date__ = "1/7/14"

import os
import subprocess
import re

#Test file for git koans

def reset():
    print ("Resetting koans to initial state...")
    # make this safer
    cmd("rm -rf ../git_test/work/")
    cmd("mkdir ../git_test/work/")
    cmd("touch ../git_test/work/.empty")

def cmd(cmd):
    """Calls subprocess.check_output with 'shell=True' and stderr redirection. Returns
    return val from subprocess. Short cut."""
    proc = subprocess.Popen([cmd],stdout=subprocess.PIPE,stderr=subprocess.STDOUT, shell=True);
    out = ""
    while True:
        line = proc.stdout.readline()
        if line != '':
            out += " " + line.rstrip()
        else:
            break
    return out
    #return subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=False);


def koan_1():
    out =  raw_input("Koan 1: Init git in the /work directory... (hint: git init ./work)\n>>")
    retval = cmd(out)

    # check to see if there is a .git dir in work...

    if(os.path.isdir("./work/.git")):
        print ("\n\nInit enlightenment attained. On to the next koan! \n\n")
    else:
        print ("\n\nThrough failure learning is achieved. Try it again.\n\n")
        koan_1();

def koan_2():
    cwd = os.getcwd()
    final =  cwd.split("/")[-1]
    if not final == "work":
        os.chdir("./work")
    out = raw_input("Koan 2: Now we will add a file to the 'work' repo. First create " +
                    "an empty file called 'foo' (hint: touch foo)\n>>");
    retval = cmd(out)
    if os.path.isfile("./foo"):
        out = raw_input("\n\n. Good. Now add the file to git with 'git add foo'\n>>")
        ret = cmd(out)
        git_status = cmd("git status")
        out = re.search("new file:\s+foo",git_status)
        if out==None:
            print "\n\nTry again.\n\n"
            koan_2()
        print " File added to the repo. Now we will go to commit it in Koan 3.\n\n"

    else:
        print "Try again.\n\n"
        koan_2()



print "Welcome to git-koans..."
reset()
# this should store state so user doesn't have to repeat with restart.
# iterate over koans using the symbol table
koan_1()
koan_2()

#git --git-dir=/Users/joelbremson/code/git_koans/.git --work-tree=./git_koans/ status



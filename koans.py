#!python

__author__ = 'joelbremson'
__date__ = "1/7/14"

import os
import pickle
import subprocess
import re

#Test file for git koans

class State:


    state = {}

    def __init__(self):
        """Set up koan system. Check for prior use so user can continue without
        restart. This will only work if the user hasn't altered the archive state."""


        try:
            f = open("../git_test/.koans_state")
            state = pickle.load(f)

        except (AttributeError,IOError):
            # not prior state to return to.
            print "In exception of __init__"
            state['counter']=1

            f = open("../git_test/.koans_state","w")
            pickle.dump(self.state,f)
            f.close()

    @classmethod
    def inc_counter(cls):
        cls.state['counter'] += 1
        cls.update_state('counter', cls.state['counter'])

    @classmethod
    def update_state(cls,key,val):
        """Increment the counter state."""
        cls.state[key]=val
        f = open("../git_test/.koans_state","w")
        pickle.dump(cls.state,f)
        f.close()

    @classmethod
    def get_counter(cls):
        """Returns the value of counter."""
        return cls.state['counter']

    def __getattr__(self, name):
        """Pass through calls to State to the 'state' dict handlers."""
        def handler_function(*args,**kwargs):
            print name
            return getattr(self.state,name,args)()
        return handler_function
        

def reset():
    print ("Resetting koans to initial state...")
    # make this safer
    cmd("rm -rf ../git_test/work/")
    cmd("rm -rf ../git_test/.koans_state")
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
        State.inc_counter()
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
        os.chdir("..")
        State.inc_counter()

    else:
        print "Try again.\n\n"
        koan_2()



print "Welcome to git-koans..."
print State.get_counter()


# this should store state so user doesn't have to repeat with restart.
# iterate over koans using the symbol table
koans = [k for k in dir() if 'koan_' in k]

for koan in koans:
    locals()[koan]()


#git --git-dir=/Users/joelbremson/code/git_koans/.git --work-tree=./git_koans/ status



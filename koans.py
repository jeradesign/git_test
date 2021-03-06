#!python

__author__ = 'joelbremson'
__date__ = "1/7/14"

"""How to write a koan.

1. Start the koan with the @koan decorator. This will print a header for you and keep track of the koan state.
2. Name your koan 'koan_<int>' where <int> is the sequence number of your koan.
3. Do your work in the koan and clean up so that cwd is in the right place when you exit.
4. If the koan is passed return True, otherwise return False.

To start fresh rm the .koan_state file in ./git_test  .
"""

import os
import pickle
import subprocess
import re
from collections import deque

#Test file for git koans

class State:
    """Set up koan system. Check for prior use so user can continue without
    restart. This will only work if the user hasn't altered the archive state."""

    keep = {'counter':1}
    workdir = "../git_test/work"


    print "Init called.\n"
    try:
        f = open("../git_test/.koans_state","r")
        inval = pickle.load(f)
        keep['counter'] = inval['counter']

    except (AttributeError,IOError):
        # no prior state to return to.
        print "In exception of __init__"

        f = open("../git_test/.koans_state","w")
        pickle.dump(keep,f)
        f.close()


    @classmethod
    def inc_counter(cls):
        cls.keep['counter'] += 1
        cls.save_state()

    @classmethod
    def reset_counter(cls):
        cls.keep['counter'] = 1
        cls.save_state()

    @classmethod
    def save_state(cls):
        f = open("../git_test/.koans_state","w")
        pickle.dump(cls.keep,f)
        f.close()

    @classmethod
    def get_counter(cls):
        """Returns the value of counter."""
        return cls.keep['counter']


def sys_reset():
    print ("Resetting koans to initial state...")
    # make this safer
    cmd("rm -rf ../git_test/work/")
    #cmd("rm -rf ../git_test/.koans_state")
    State.reset_counter()
    cmd("mkdir ../git_test/work/")
    cmd("touch ../git_test/work/.empty")

def cmd(cmd,verbose=False):
    """Calls subprocess.check_output with 'shell=True' and stderr redirection. Returns
    return val from subprocess. 'verbose' flag is a boolean. Set to true for debugging info. Short cut."""
    proc = subprocess.Popen([cmd],stdout=subprocess.PIPE,stderr=subprocess.STDOUT, shell=True);
    out = ""
    while True:
        line = proc.stdout.readline()
        if verbose:
            print line
        if line != '':
            out += " " + line.rstrip()
        else:
            break
    return out
    #return subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=False);

def koan(fxn):
    """Prints koan header and increments state counter (given the koan is passed)."""
    def new_fxn(*args,**kwargs):
        header = kwargs.get('header',True)
        test,answers = test_vals(*args,**kwargs)
        if header:
            print "\n\n********  Koan " + str(State.get_counter()) + "  ********\n\n"
        success = fxn(*args,**kwargs)
        if success: # success
            print "\n\nEnlightenment Achieved!"
            State.inc_counter()
        else: # failed
            print ("\n\nThrough failure learning is achieved. Try it again.\n\n")
            if not test:
                # something in here?? ::w

                globals()[fxn.__name__](header=False)
        return success
    return new_fxn

def test_vals(*args, **kwargs):
    """Return vals in args and kwargs used for testing. Returns <bool test>,<list answers>."""
    test = 'test' in args
    answers = deque(kwargs.get('answers',[]))
    return test, answers

@koan
def koan_1(*args,**kwargs):
    """Init the first repo."""
    retval = False
    test,answers = test_vals(*args,**kwargs)
    if test:
        cmd_ret = cmd(answers.popleft())
    else:
        out =  raw_input("Koan 1: Init git in the /work directory... (hint: git init ./work)\n>>")
        cmd_ret = cmd(out)

    # check to see if there is a .git dir in work...

    if(os.path.isdir("./work/.git")):
        retval = True
    return retval

@koan
def koan_2(*args,**kwargs):
    """Add a file."""
    test,answers = test_vals(*args,**kwargs)
    cwd = os.getcwd()
    ret_val = False
    final =  cwd.split("/")[-1]
    if not final == "work":
        os.chdir("../git_test/work")
    if test:
        out = answers.popleft()
    else:
        out = raw_input("Koan 2: Now we will add a file to the 'work' repo. First create " +
                    "an empty file called 'foo' (hint: touch foo)\n>>");

    retval = cmd(out)
    if os.path.isfile("./foo"):
        if test:
            out = answers.popleft()
        else:
            print """\n\nYou have now created what git calls an 'untracked file'. Next we
will make it tracked by officially adding it to the repository."""
            out = raw_input("\n\n. Add the file to git with 'git add foo'\n>>")
        ret = cmd(out)
        git_status = cmd("git status")
        out = re.search("new file:\s+foo",git_status)

        try:
            if out.group():
                ret_val = True
                print """The file has been added. It is now a 'tracked file.' The add command does
more than just add to the repo though, as we will see later."""
                print "\n\nNext we will learn about basic commits.\n\n"
                os.chdir("..")
        except AttributeError:
            os.chdir("..")
            pass
    return ret_val

@koan
def koan_3(*args,**kwargs):
    """Commit file."""
    test,answers = test_vals(*args,**kwargs)
    ret_val = False
    loc = os.getcwd()
    os.chdir("../git_test/work")
    if test:
        out = answers.popleft()
    else:
        out = raw_input("Now commit your changes with the 'git commit -a' command. Note that\nyou" +
"are in your repo directory 'work'. Also, you will need to add a message to your commit. How?\n./work >>")
    rv = cmd(out)
    print rv
    out = re.search("\[master \(root\-commit\)", rv )
    try:
        if out.group():
            ret_val = True
    except AttributeError:
        pass
    os.chdir("..")
    return ret_val

@koan
def koan_4(*args,**kwargs):
    """.gitignore koan."""
    test,answers=test_vals(*args,**kwargs)
    retval = False
    print """For this koan you will need to open another shell window. When you are ready
I will check your work for you."""

    print """\n\nThis koan is about the '.gitignore' file feature. Sometimes you have files
you don't want git to ever track.\n\n.In your /work repo create a .gitignore
file that does 1) ignores files called 'baz' and 2) ignores any files that match *.a ."""
    os.chdir(State.workdir)
    if not test:
        raw_input("Press any key when you are done.")
    out = cmd("echo 'text' > baz")
    out = cmd("echo 'text' > dfsdf.a")

    out = cmd("git add baz" )
    match1 = re.search(".*ignored.*baz",out)
    print out


    out = cmd("git add dfsdf.a" )
    match2 = re.search(".*ignored.*dfsdf.a",out)
    print out
    try:
        if match1.group():
            print "\n\nFile 'baz' ignored."
        if match2.group():
            print "File 'dfsdf.a ignored.\n\n"
        retval = True
        print "*** Koan Success! ***\n"
    except AttributeError:
        out = cmd("git status")
        print out
        out = cmd("git reset HEAD baz")
        print out
        out = cmd("git reset HEAD dfsdf.a")
        print out
        out = cmd("git status")
        print out
        pass

    os.chdir("..")
    return retval

def koan_5(*args,**kwargs):
	"""This koan is a small puzzle in which the user is asked to figure out which file has been 
modified since staging. The answer can be found with diff."""



	return True # so it passes the test for now.

if __name__ == "__main__":
    print "Welcome to git-koans...\n"
    print """\n\nThese koans cover the basic concepts from Pro Git by Scott Chacon (http://git-scm.com/book).
See chapter 2 for assistance - http://git-scm.com/book/en/Git-Basics ."""


    if State.get_counter()==1 or raw_input("reset?")=="y":
        sys_reset()
    else:
        print "\n\nContinuing from koan " + str(State.get_counter()) + "\n\n"


    # this should store state so user doesn't have to repeat with restart.
    # iterate over koans using the symbol table
    koans = [k for k in dir() if 'koan_' in k]

    for koan in sorted(koans):
        out = re.search("\d+$",koan)
        
        if int(out.group(0)) < State.get_counter():
            continue
        locals()[koan]()


    #git --git-dir=/Users/joelbremson/code/git_koans/.git --work-tree=./git_koans/ status



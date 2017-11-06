#!/usr/bin/python

import sys, inspect

def called_from_main():
    stack = inspect.stack()
    if len(stack)<3: return False
    callerframe = stack[2][0]
    callerhash = dict(inspect.getmembers(callerframe))
    caller_globals = callerhash.get('f_globals', False)
    if caller_globals:
        return caller_globals.get('__name__', None) == '__main__'


from optparse import OptionParser
from itertools import chain

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO



casts = {"int"   : int,
         "float" : float,
         "bool"  : bool,
         "str"   : str} # other??

def is_option(t):
    return t and t.startswith("-") and len(t)>1

def is_posarg(t):
    return t and not is_option(t) 

def is_cast(t):
    return t and t.startswith("(") and t.endswith(")")

def is_choice(t):
    return t and "|" in t

def is_assignment(t):
    return t and (t.find("->") >= 0)


def handle_option(parser, optdef):
    opt, help = (":" in optdef) and optdef.split(":",1) or (optdef,"")
    optstrings =  []
    optatts    =  {"help" : help.strip(), "nargs":0}

    for term in opt.split():
        if is_option(term):
            optstrings.append(term)
        elif is_cast(term):
            optatts["type"] = term[1:-1]
        elif is_assignment(term):
            const, dest = term.split("->")
            optatts["dest"]  = dest
            optatts["const"] = const
        elif is_choice(term):
            optatts["choices"] = term.split("|")
        else:
            optatts["dest"]   = term
            optatts["nargs"]  = 1

    # Set default type
    
    if "type" not in optatts:
        if not optatts["nargs"]:
            optatts["type"] = "int"

    # Eval const

    if "type" in optatts and "const" in optatts:
        optatts["const"] = eval("%(type)s(%(const)s)" % optatts)

    # Set action

    if optatts["nargs"]:
        optatts["action"] = "store"
    else:
        optatts["action"] = "store_const"
        if not "dest" in optatts:
            optatts["const"] = True
        del optatts["type"]
        del optatts["nargs"]
    
    # Finally

    parser.add_option(*(optstrings),**(optatts))
            


def handle_posarg(pargdef):
    parg, help = (":" in pargdef) and pargdef.split(":",1) or (pargdef,"")
    cast = "str"
    name = ""
    for term in parg.split():
        if is_cast(term):
            cast= term[1:-1]
        else:
            name = term

    return (name, cast, help.strip())


def pargs_n_opts(optdefs):

    pargs = [handle_posarg(optdef) for optdef in optdefs if is_posarg(optdef)]

    # based on pargs, build usage string
    
    usage = "%prog [options]"

    if len(pargs)>0:
        usage += " "
        usage += " ".join([parg[0] for parg in pargs])

        # add explanation for pargs if any of them has helptext

        hpargs = filter(lambda parg: str.strip(parg[2]), pargs)

        if hpargs:
            usage += " \n\narguments:"
        
            for (name, type, help) in pargs:
                usage += "\n  %s %s" % (name.ljust(12), help)
            

    # then parse option definitions
    
    parser = OptionParser(usage=usage)

    for optdef in filter(is_option, optdefs):
        handle_option(parser, optdef)

    return pargs, parser



def che(func, optdefs, sysargs=None):

    if not called_from_main(): return

    # to allow semicolons with syntax \;
    
    optdefs = optdefs.replace("\;", "@@@@semicolon@@@@");
    optdefs = optdefs.replace(";","\n")
    optdefs = optdefs.replace("@@@@semicolon@@@@", ";");
    optdefs = optdefs.replace("\r","\n")
    
    lines = [l.strip() for l in optdefs.split("\n")]
    pargs, parser = pargs_n_opts(lines)

    if sysargs==None:
        sysargs = sys.argv[1:]

    opts, cargs = parser.parse_args(sysargs)

    if len(cargs) != len(pargs):
        parser.print_help()
        if cargs:
            sys.exit("\nERROR: wrong number of arguments %s vs. %s"
                     % (cargs, pargs))
        else:
            sys.exit()

    # Now we go through command line args and set up the list of args

    arglist = []

    for carg, (name, cast, help) in zip(cargs, pargs):
        try:
            arglist.append(casts[cast](carg))
        except ValueError:
            parser.print_help()
            sys.exit('\nERROR: invalid type for "%s". "%s" is not %s' \
                     % (name, carg, cast))

    # move opts to dictionary kws 

    kws = {}
    
    optdests = [o.dest
                for o in chain(parser._short_opt.values(),
                               parser._long_opt.values())
                if o.dest]

    for d in optdests:
        val = getattr(opts,d)
        if val != None:
            kws[d.replace("-","_")] = val

    return func(*arglist, **kws)


def teller(*args, **kws): # For debugging purposes
    print("args =", args)
    print("kws  =", kws)

if __name__ == "__main__":
    che(teller, open(sys.argv.pop(1)).read())

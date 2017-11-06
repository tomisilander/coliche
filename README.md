# Coliche

Coliche is a simple Python-module to handle command line arguments.
It tries to make providing command line argument handling support so
easy that one has no excuse not to provide one.

Part of Coliche is built on top of standard optparse-module.

## Overview


I often find standard optparse too heavy to use.
Coliche defines one function, coliche.che, that 
parses a command line definition (a.k.a usage) string and 
calls the main function with proper parameters.

It is designed to be used to call the main function of the program, say:
```
 def main(arg1, arg2, opt1=3, option2=False):
	 print arg1, arg2, opt1, option2
```
by first defining the command line:
```
 cldef = """
 arg1 : first argument
 arg2 : second argument

 -o --option1 opt1 (int) : option number one
 -p --option2            : option number two
 """
```
and then calling main function (or any provided function) via che:
```
 import coliche
 coliche.che(main, cldef)
```

Coliche checks that there are correct number of positional arguments
and that the options provided are legal. It also casts the
arguments and builds the usage string.


## Syntax 

Coliche command line definition syntax is line-based.
There is one definition per line and and the empty lines are skipped.
One can also use semicolons as a definition separator.  
These are replaced by newlines before
processing. Here is an example that tries to show all the features::
```
 coliche.che(main, 
             """arg1; arg2
                arg3  : the third argument
	        -o opt1 (int)             : OPT1 has to be integer, default: 0
                -p --option2              : a boolean option
                -m --mode mode Good|Bad|Ugly : default: Ugly
                -v --verbose
                -q --quiet False->verbose
                --new-pi pi-value (float) : default: 3.14.
                """)
```
and the corresponding main function ::
```
 def main(a1, a2, a3, '
          opt1=0, option2=False, mode="Ugly", verbose=False, pi_value=3.14):
	print a1,a2,a3
	print opt1, option2, mode, verbose, pi_value
```

### Definition of the syntax:

```
While the example above pretty much tells it all,
here is the informal syntax of one definition line:

 <defline>      ::= <posdef> | <optdef>
 <posdef>       ::= just a name of the positional command line argument
 <optdef>       ::= <optionpart> [":" help text to be put in usage string]
 <optionpart>   ::= <flagpart> [<cast>] [<alternatives>] [<assignment>]
 <flagpart>     ::= ["-"letter]["--"long-option][option argument]
 <cast>         ::= "(" ("int"|"bool"|"float"|"str") ")"
 <alternatives> ::= string ("|" string)+
 <assignment>   ::= value "->" argument
```

Definitions are either positional parameter definitions (like arg1 and
arg2 above) or option definitions that start with "-" or "--". Each
definition may also have help text that is separated by the first ":"
in line.  This help text is put to the usage string that is displayed
if there is error in the command line or if the -h option is provided.
The required type is put in parentheses. With no required type the
parameter is not cast but taken to be a string, or if the option has
no arguments, its is considered to be a boolean. One may also provide
a list of allowed parameter values by separating them with "|".  There
is also syntax to set a value of certain argument.


# Licence (just a disclaimer)

You are free to use Coliche any way you like as far as I am not held
responsible for anything.


### Todo

or at least some ideas what could be nice to have:

* support for variable number of arguments ("files...") that would
  gather the arguments to a list or maybe append them to the posargs 
  so that the main could read "def main(a, b, \*rest, f=3):"
* optional support for environment variables and config-files
* possibility to report default values in usage string by inspection
* possibility to infer required type by inspection
* possibility to include argument type to usage string
* syntax to specify obligatory options
* options with more than one argument
* and one can always clean the code

* better exception handling for example

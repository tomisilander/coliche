# This is a way to test coliche

1. Write the command line documentation string to a file (say tst01.def)
2. Run coliche.py giving the file as a first command line argument
   followed by the rest of the arguments

For example running :
```
 python ../coliche.py tst1.def a b c -p
```
gives:
```
 args = ('a', 'b', 'c')
 kws  = {'option2': True}
```

from distutils.core import setup

setup(name          = "coliche",
      version       = "0.1",
      description   = "Command-line checker",
      author        = "Tomi Silander",
      author_email  = "tomi.silander@iki.fi",
      url           = "https://github.com/tomisilander/coliche",
      py_modules    = ["coliche"],

      long_description = """
      
      Coliche is a simple module to handle command line arguments.  Its is
      built on top of standard optparse-module.  The goal has been to make
      providing the command line argument handling support so easy that one
      has no excuse not to do it.

      """

      )
